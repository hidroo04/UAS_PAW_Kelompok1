"""
Attendance views - Mark attendance, view attendance history
Merekap kehadiran dari semua class bookings
"""
from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.orm import joinedload
import json
from datetime import datetime

from ..models import Attendance, Booking, GymClass, Member, User
from ..models.user import UserRole
from ..utils.auth import get_token_from_header, decode_jwt_token
import jwt


def get_authenticated_user(request):
    """Get authenticated user from JWT token"""
    token = get_token_from_header(request)
    if not token:
        return None
    
    try:
        payload = decode_jwt_token(token)
        user_id = payload.get('user_id')
        if user_id:
            db = request.dbsession
            return db.query(User).filter(User.id == user_id).first()
        return None
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def get_authenticated_user_id(request):
    """Extract user_id from JWT token"""
    token = get_token_from_header(request)
    if not token:
        return None
    
    try:
        payload = decode_jwt_token(token)
        return payload.get('user_id')
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


@view_config(route_name='api_attendance', renderer='json', request_method='GET')
def get_attendance(request):
    """
    Get attendance records - merekap semua bookings dengan status kehadiran
    Menampilkan semua booking dan statusnya (hadir/tidak hadir/belum dicatat)
    """
    try:
        db = request.dbsession
        
        # Filter parameters
        class_id = request.params.get('class_id')
        date_filter = request.params.get('date')
        
        # Query semua bookings dengan relasi
        query = db.query(Booking).options(
            joinedload(Booking.member).joinedload(Member.user),
            joinedload(Booking.gym_class),
            joinedload(Booking.attendance)
        )
        
        # Filter by class
        if class_id:
            query = query.filter(Booking.class_id == int(class_id))
        
        bookings = query.all()
        
        # Build attendance data dari bookings
        attendance_data = []
        for booking in bookings:
            # Filter by date jika ada
            if date_filter:
                class_date = booking.gym_class.schedule.strftime('%Y-%m-%d') if booking.gym_class and booking.gym_class.schedule else None
                if class_date != date_filter:
                    continue
            
            attendance_record = {
                'id': booking.attendance.id if booking.attendance else None,
                'booking_id': booking.id,
                'attended': booking.attendance.attended if booking.attendance else None,
                'attendance_date': booking.attendance.date.isoformat() if booking.attendance and booking.attendance.date else None,
                'member': {
                    'id': booking.member.id if booking.member else None,
                    'name': booking.member.user.name if booking.member and booking.member.user else 'Unknown',
                    'email': booking.member.user.email if booking.member and booking.member.user else None
                },
                'class': {
                    'id': booking.gym_class.id if booking.gym_class else None,
                    'name': booking.gym_class.name if booking.gym_class else 'Unknown',
                    'schedule': booking.gym_class.schedule.isoformat() if booking.gym_class and booking.gym_class.schedule else None
                },
                'booking_date': booking.booking_date.isoformat() if booking.booking_date else None
            }
            attendance_data.append(attendance_record)
        
        # Sort by class schedule (newest first)
        attendance_data.sort(key=lambda x: x['class']['schedule'] or '', reverse=True)
        
        # Calculate statistics
        total = len(attendance_data)
        present = sum(1 for a in attendance_data if a['attended'] is True)
        absent = sum(1 for a in attendance_data if a['attended'] is False)
        not_marked = sum(1 for a in attendance_data if a['attended'] is None)
        
        return {
            'status': 'success',
            'data': attendance_data,
            'count': total,
            'statistics': {
                'total': total,
                'present': present,
                'absent': absent,
                'not_marked': not_marked
            }
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )


@view_config(route_name='api_attendance', renderer='json', request_method='POST')
def mark_attendance(request):
    """Mark atau update attendance untuk booking - HANYA TRAINER"""
    try:
        db = request.dbsession
        
        # Check if user is trainer
        user = get_authenticated_user(request)
        if not user:
            return Response(
                json.dumps({'status': 'error', 'message': 'Authentication required'}),
                status=401,
                content_type='application/json; charset=utf-8'
            )
        
        if user.role != UserRole.TRAINER:
            return Response(
                json.dumps({'status': 'error', 'message': 'Only trainers can mark attendance'}),
                status=403,
                content_type='application/json; charset=utf-8'
            )
        
        data = request.json_body
        
        # Validation
        if 'booking_id' not in data:
            return Response(
                json.dumps({'status': 'error', 'message': 'booking_id is required'}),
                status=400,
                content_type='application/json; charset=utf-8'
            )
        
        booking_id = data['booking_id']
        attended = data.get('attended', True)
        
        # Check booking exists
        booking = db.query(Booking).options(
            joinedload(Booking.gym_class)
        ).filter(Booking.id == booking_id).first()
        
        if not booking:
            return Response(
                json.dumps({'status': 'error', 'message': 'Booking not found'}),
                status=404,
                content_type='application/json; charset=utf-8'
            )
        
        # Verify trainer owns this class
        if booking.gym_class and booking.gym_class.trainer_id != user.id:
            return Response(
                json.dumps({'status': 'error', 'message': 'You can only mark attendance for your own classes'}),
                status=403,
                content_type='application/json; charset=utf-8'
            )
        
        # Check if attendance already exists
        existing = db.query(Attendance).filter(Attendance.booking_id == booking_id).first()
        
        if existing:
            # Update existing attendance
            existing.attended = attended
            existing.date = datetime.utcnow()
            db.commit()
            
            return {
                'status': 'success',
                'message': 'Attendance updated successfully',
                'data': existing.to_dict()
            }
        else:
            # Create new attendance
            new_attendance = Attendance(
                booking_id=booking_id,
                attended=attended,
                date=datetime.utcnow()
            )
            db.add(new_attendance)
            db.commit()
            
            return {
                'status': 'success',
                'message': 'Attendance marked successfully',
                'data': new_attendance.to_dict()
            }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )


@view_config(route_name='api_my_attendance', renderer='json', request_method='GET')
def get_my_attendance(request):
    """Get attendance history untuk member yang login"""
    try:
        db = request.dbsession
        
        # Get user from token
        user_id = get_authenticated_user_id(request)
        if not user_id:
            return Response(
                json.dumps({'status': 'error', 'message': 'Authentication required'}),
                status=401,
                content_type='application/json; charset=utf-8'
            )
        
        # Get member
        member = db.query(Member).filter(Member.user_id == user_id).first()
        if not member:
            return Response(
                json.dumps({'status': 'error', 'message': 'Member not found'}),
                status=404,
                content_type='application/json; charset=utf-8'
            )
        
        # Get bookings for this member dengan attendance
        bookings = db.query(Booking).options(
            joinedload(Booking.gym_class),
            joinedload(Booking.attendance)
        ).filter(Booking.member_id == member.id).all()
        
        attendance_data = []
        for booking in bookings:
            attendance_record = {
                'id': booking.attendance.id if booking.attendance else None,
                'booking_id': booking.id,
                'attended': booking.attendance.attended if booking.attendance else None,
                'date': booking.attendance.date.isoformat() if booking.attendance and booking.attendance.date else None,
                'class': {
                    'id': booking.gym_class.id if booking.gym_class else None,
                    'name': booking.gym_class.name if booking.gym_class else 'Unknown',
                    'schedule': booking.gym_class.schedule.isoformat() if booking.gym_class and booking.gym_class.schedule else None
                }
            }
            attendance_data.append(attendance_record)
        
        return {
            'status': 'success',
            'data': attendance_data,
            'count': len(attendance_data)
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )
