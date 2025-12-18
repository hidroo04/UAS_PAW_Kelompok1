"""
Trainer views - Manage classes and class members
"""
from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy import and_
import json
from datetime import datetime, timedelta
from ..models import Booking, GymClass, User, Member, Attendance
from sqlalchemy.orm import joinedload
from ..utils.auth import get_token_from_header, decode_jwt_token
import jwt


def get_authenticated_trainer_id(request):
    """Extract user_id from JWT token and verify trainer role"""
    token = get_token_from_header(request)
    if not token:
        return None, "Authentication required"
    
    try:
        payload = decode_jwt_token(token)
        user_id = payload.get('user_id')
        role = payload.get('role', '').upper()
        
        if role != 'TRAINER':
            return None, f"Access denied. Trainer role required (got: {role})"
        
        return user_id, None
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        return None, str(e)


def cleanup_expired_classes(db, trainer_id):
    """
    Auto cleanup: Mark absent untuk member yang tidak hadir pada kelas yang sudah lewat,
    lalu hapus kelas tersebut
    """
    now = datetime.utcnow()
    
    # Cari kelas yang sudah lewat jadwalnya
    expired_classes = db.query(GymClass).filter(
        and_(
            GymClass.trainer_id == trainer_id,
            GymClass.schedule < now
        )
    ).all()
    
    cleaned_classes = []
    for gym_class in expired_classes:
        # Get all bookings for this class
        bookings = db.query(Booking).filter(Booking.class_id == gym_class.id).all()
        
        for booking in bookings:
            # Cek apakah attendance sudah ada
            existing = db.query(Attendance).filter(
                Attendance.booking_id == booking.id
            ).first()
            
            if not existing:
                # Jika tidak ada attendance record, otomatis buat sebagai absent
                new_attendance = Attendance(
                    booking_id=booking.id,
                    attended=False,
                    date=now
                )
                db.add(new_attendance)
        
        cleaned_classes.append({
            'id': gym_class.id,
            'name': gym_class.name,
            'schedule': gym_class.schedule.isoformat() if gym_class.schedule else None
        })
        
        # Hapus kelas (cascade akan hapus bookings dan attendance)
        db.delete(gym_class)
    
    if cleaned_classes:
        db.commit()
    
    return cleaned_classes


@view_config(route_name='api_trainer_classes', renderer='json', request_method='GET')
def get_trainer_classes(request):
    """Get all classes taught by the authenticated trainer with member details"""
    try:
        db = request.dbsession
        
        # Get trainer user_id
        trainer_id, error = get_authenticated_trainer_id(request)
        if error:
            return Response(
                json.dumps({'status': 'error', 'message': error}),
                status=401,
                content_type='application/json; charset=utf-8'
            )
        
        # Auto cleanup expired classes first
        cleaned = cleanup_expired_classes(db, trainer_id)
        
        # Get classes taught by this trainer (yang belum expired)
        classes = db.query(GymClass).options(
            joinedload(GymClass.trainer),
            joinedload(GymClass.bookings).joinedload(Booking.member).joinedload(Member.user)
        ).filter(GymClass.trainer_id == trainer_id).all()
        
        classes_data = []
        for gym_class in classes:
            # Get bookings for this class
            bookings = db.query(Booking).options(
                joinedload(Booking.member).joinedload(Member.user)
            ).filter(Booking.class_id == gym_class.id).all()
            
            members_data = []
            for booking in bookings:
                if booking.member and booking.member.user:
                    # Get attendance record (single)
                    attendance = db.query(Attendance).filter(
                        Attendance.booking_id == booking.id
                    ).first()
                    
                    members_data.append({
                        'booking_id': booking.id,
                        'member_id': booking.member.id,
                        'user_id': booking.member.user.id,
                        'name': booking.member.user.name,
                        'email': booking.member.user.email,
                        'booking_date': booking.booking_date.isoformat() if booking.booking_date else None,
                        'membership_plan': booking.member.membership_plan if hasattr(booking.member, 'membership_plan') else 'N/A',
                        'attendance': {
                            'id': attendance.id if attendance else None,
                            'attended': attendance.attended if attendance else False,
                            'date': attendance.date.isoformat() if attendance and attendance.date else None
                        } if attendance else None
                    })
            
            # Hitung apakah class sudah expired
            is_expired = gym_class.schedule < datetime.utcnow() if gym_class.schedule else False
            
            class_dict = {
                'id': gym_class.id,
                'name': gym_class.name,
                'description': gym_class.description,
                'schedule': gym_class.schedule.isoformat() if gym_class.schedule else None,
                'capacity': gym_class.capacity,
                'enrolled_count': len(members_data),
                'available_slots': gym_class.capacity - len(members_data),
                'is_expired': is_expired,
                'members': members_data
            }
            classes_data.append(class_dict)
        
        return {
            'status': 'success',
            'data': classes_data,
            'count': len(classes_data),
            'cleaned_classes': cleaned if cleaned else []
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )


@view_config(route_name='api_trainer_class_members', renderer='json', request_method='GET')
def get_class_members(request):
    """Get all members enrolled in a specific class"""
    try:
        db = request.dbsession
        class_id = int(request.matchdict['class_id'])
        
        # Get trainer user_id
        trainer_id, error = get_authenticated_trainer_id(request)
        if error:
            return Response(
                json.dumps({'status': 'error', 'message': error}),
                status=401,
                content_type='application/json; charset=utf-8'
            )
        
        # Verify this class belongs to the trainer
        gym_class = db.query(GymClass).filter(
            and_(
                GymClass.id == class_id,
                GymClass.trainer_id == trainer_id
            )
        ).first()
        
        if not gym_class:
            return Response(
                json.dumps({'status': 'error', 'message': 'Class not found or access denied'}),
                status=404,
                content_type='application/json; charset=utf-8'
            )
        
        # Get bookings for this class
        bookings = db.query(Booking).options(
            joinedload(Booking.member).joinedload(Member.user)
        ).filter(Booking.class_id == class_id).all()
        
        members_data = []
        for booking in bookings:
            if booking.member and booking.member.user:
                members_data.append({
                    'booking_id': booking.id,
                    'member_id': booking.member.id,
                    'user_id': booking.member.user.id,
                    'name': booking.member.user.name,
                    'email': booking.member.user.email,
                    'booking_date': booking.booking_date.isoformat() if booking.booking_date else None,
                    'membership_plan': booking.member.membership_plan if hasattr(booking.member, 'membership_plan') else 'N/A'
                })
        
        return {
            'status': 'success',
            'data': {
                'class': {
                    'id': gym_class.id,
                    'name': gym_class.name,
                    'schedule': gym_class.schedule.isoformat() if gym_class.schedule else None,
                    'capacity': gym_class.capacity
                },
                'members': members_data,
                'count': len(members_data)
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


@view_config(route_name='api_trainer_remove_member', renderer='json', request_method='DELETE')
def remove_member_from_class(request):
    """Remove a member from a class (delete booking)"""
    try:
        db = request.dbsession
        class_id = int(request.matchdict['class_id'])
        booking_id = int(request.matchdict['booking_id'])
        
        # Get trainer user_id
        trainer_id, error = get_authenticated_trainer_id(request)
        if error:
            return Response(
                json.dumps({'status': 'error', 'message': error}),
                status=401,
                content_type='application/json; charset=utf-8'
            )
        
        # Verify this class belongs to the trainer
        gym_class = db.query(GymClass).filter(
            and_(
                GymClass.id == class_id,
                GymClass.trainer_id == trainer_id
            )
        ).first()
        
        if not gym_class:
            return Response(
                json.dumps({'status': 'error', 'message': 'Class not found or access denied'}),
                status=404,
                content_type='application/json; charset=utf-8'
            )
        
        # Find the booking
        booking = db.query(Booking).filter(
            and_(
                Booking.id == booking_id,
                Booking.class_id == class_id
            )
        ).first()
        
        if not booking:
            return Response(
                json.dumps({'status': 'error', 'message': 'Booking not found'}),
                status=404,
                content_type='application/json; charset=utf-8'
            )
        
        # Get member info before deleting
        member_name = booking.member.user.name if booking.member and booking.member.user else 'Unknown'
        
        # Delete the booking
        db.delete(booking)
        db.commit()
        
        return {
            'status': 'success',
            'message': f'{member_name} has been removed from {gym_class.name}'
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        db.rollback()
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )


@view_config(route_name='api_trainer_mark_attendance', renderer='json', request_method='POST')
def mark_attendance(request):
    """Mark attendance for a member in trainer's class"""
    try:
        db = request.dbsession
        data = request.json_body
        
        class_id = int(request.matchdict['class_id'])
        booking_id = int(request.matchdict['booking_id'])
        attended = data.get('attended', True)
        
        # Get trainer user_id
        trainer_id, error = get_authenticated_trainer_id(request)
        if error:
            return Response(
                json.dumps({'status': 'error', 'message': error}),
                status=401,
                content_type='application/json; charset=utf-8'
            )
        
        # Verify this class belongs to the trainer
        gym_class = db.query(GymClass).filter(
            and_(
                GymClass.id == class_id,
                GymClass.trainer_id == trainer_id
            )
        ).first()
        
        if not gym_class:
            return Response(
                json.dumps({'status': 'error', 'message': 'Class not found or access denied'}),
                status=404,
                content_type='application/json; charset=utf-8'
            )
        
        # Verify booking exists and belongs to this class
        booking = db.query(Booking).filter(
            and_(
                Booking.id == booking_id,
                Booking.class_id == class_id
            )
        ).first()
        
        if not booking:
            return Response(
                json.dumps({'status': 'error', 'message': 'Booking not found'}),
                status=404,
                content_type='application/json; charset=utf-8'
            )
        
        # Check if attendance record already exists
        attendance = db.query(Attendance).filter(
            Attendance.booking_id == booking_id
        ).first()
        
        if attendance:
            # Update existing attendance
            attendance.attended = attended
            attendance.date = datetime.utcnow()
        else:
            # Create new attendance record
            attendance = Attendance(
                booking_id=booking_id,
                attended=attended,
                date=datetime.utcnow()
            )
            db.add(attendance)
        
        db.commit()
        
        member_name = booking.member.user.name if booking.member and booking.member.user else 'Unknown'
        status_text = 'present' if attended else 'absent'
        
        return {
            'status': 'success',
            'message': f'{member_name} marked as {status_text}',
            'data': {
                'attendance_id': attendance.id,
                'booking_id': booking_id,
                'attended': attended,
                'date': attendance.date.isoformat()
            }
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        db.rollback()
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )


@view_config(route_name='api_trainer_create_class', renderer='json', request_method='POST')
def create_class(request):
    """Create a new class by trainer"""
    try:
        db = request.dbsession
        data = request.json_body
        
        # Get trainer user_id
        trainer_id, error = get_authenticated_trainer_id(request)
        if error:
            return Response(
                json.dumps({'status': 'error', 'message': error}),
                status=401,
                content_type='application/json; charset=utf-8'
            )
        
        # Validate required fields
        required_fields = ['name', 'description', 'schedule', 'capacity']
        for field in required_fields:
            if field not in data:
                return Response(
                    json.dumps({'status': 'error', 'message': f'{field} is required'}),
                    status=400,
                    content_type='application/json; charset=utf-8'
                )
        
        # Parse schedule
        try:
            schedule = datetime.fromisoformat(data['schedule'].replace('Z', '+00:00'))
        except ValueError:
            return Response(
                json.dumps({'status': 'error', 'message': 'Invalid schedule format. Use ISO format'}),
                status=400,
                content_type='application/json; charset=utf-8'
            )
        
        # Check if trainer already has a class at the same time (within 1 hour window)
        from datetime import timedelta
        time_window_start = schedule - timedelta(hours=1)
        time_window_end = schedule + timedelta(hours=1)
        
        existing_class = db.query(GymClass).filter(
            and_(
                GymClass.trainer_id == trainer_id,
                GymClass.schedule >= time_window_start,
                GymClass.schedule <= time_window_end
            )
        ).first()
        
        if existing_class:
            return Response(
                json.dumps({
                    'status': 'error', 
                    'message': f'You already have a class "{existing_class.name}" scheduled at {existing_class.schedule.strftime("%Y-%m-%d %H:%M")}. Please choose a different time (at least 1 hour apart).'
                }),
                status=400,
                content_type='application/json; charset=utf-8'
            )
        
        # Create new class
        new_class = GymClass(
            name=data['name'],
            description=data['description'],
            schedule=schedule,
            capacity=int(data['capacity']),
            trainer_id=trainer_id
        )
        
        db.add(new_class)
        db.commit()
        db.refresh(new_class)
        
        return {
            'status': 'success',
            'message': 'Class created successfully',
            'data': {
                'id': new_class.id,
                'name': new_class.name,
                'description': new_class.description,
                'schedule': new_class.schedule.isoformat(),
                'capacity': new_class.capacity,
                'trainer_id': new_class.trainer_id
            }
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        db.rollback()
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )


@view_config(route_name='api_trainer_update_class', renderer='json', request_method='PUT')
def update_class(request):
    """Update an existing class"""
    try:
        db = request.dbsession
        data = request.json_body
        class_id = int(request.matchdict['class_id'])
        
        # Get trainer user_id
        trainer_id, error = get_authenticated_trainer_id(request)
        if error:
            return Response(
                json.dumps({'status': 'error', 'message': error}),
                status=401,
                content_type='application/json; charset=utf-8'
            )
        
        # Verify this class belongs to the trainer
        gym_class = db.query(GymClass).filter(
            and_(
                GymClass.id == class_id,
                GymClass.trainer_id == trainer_id
            )
        ).first()
        
        if not gym_class:
            return Response(
                json.dumps({'status': 'error', 'message': 'Class not found or access denied'}),
                status=404,
                content_type='application/json; charset=utf-8'
            )
        
        # If schedule is being updated, check for conflicts
        if 'schedule' in data:
            try:
                new_schedule = datetime.fromisoformat(data['schedule'].replace('Z', '+00:00'))
                
                # Check for schedule conflict (within 1 hour window, excluding current class)
                from datetime import timedelta
                time_window_start = new_schedule - timedelta(hours=1)
                time_window_end = new_schedule + timedelta(hours=1)
                
                existing_class = db.query(GymClass).filter(
                    and_(
                        GymClass.trainer_id == trainer_id,
                        GymClass.id != class_id,  # Exclude current class
                        GymClass.schedule >= time_window_start,
                        GymClass.schedule <= time_window_end
                    )
                ).first()
                
                if existing_class:
                    return Response(
                        json.dumps({
                            'status': 'error', 
                            'message': f'You already have a class "{existing_class.name}" scheduled at {existing_class.schedule.strftime("%Y-%m-%d %H:%M")}. Please choose a different time (at least 1 hour apart).'
                        }),
                        status=400,
                        content_type='application/json; charset=utf-8'
                    )
                
                gym_class.schedule = new_schedule
            except ValueError:
                return Response(
                    json.dumps({'status': 'error', 'message': 'Invalid schedule format'}),
                    status=400,
                    content_type='application/json; charset=utf-8'
                )
        
        # Update other fields
        if 'name' in data:
            gym_class.name = data['name']
        if 'description' in data:
            gym_class.description = data['description']
        if 'capacity' in data:
            gym_class.capacity = int(data['capacity'])
        
        db.commit()
        db.refresh(gym_class)
        
        return {
            'status': 'success',
            'message': 'Class updated successfully',
            'data': {
                'id': gym_class.id,
                'name': gym_class.name,
                'description': gym_class.description,
                'schedule': gym_class.schedule.isoformat(),
                'capacity': gym_class.capacity
            }
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        db.rollback()
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )


@view_config(route_name='api_trainer_delete_class', renderer='json', request_method='DELETE')
def delete_class(request):
    """Delete a class"""
    try:
        db = request.dbsession
        class_id = int(request.matchdict['class_id'])
        
        # Get trainer user_id
        trainer_id, error = get_authenticated_trainer_id(request)
        if error:
            return Response(
                json.dumps({'status': 'error', 'message': error}),
                status=401,
                content_type='application/json; charset=utf-8'
            )
        
        # Verify this class belongs to the trainer
        gym_class = db.query(GymClass).filter(
            and_(
                GymClass.id == class_id,
                GymClass.trainer_id == trainer_id
            )
        ).first()
        
        if not gym_class:
            return Response(
                json.dumps({'status': 'error', 'message': 'Class not found or access denied'}),
                status=404,
                content_type='application/json; charset=utf-8'
            )
        
        class_name = gym_class.name
        db.delete(gym_class)
        db.commit()
        
        return {
            'status': 'success',
            'message': f'Class "{class_name}" deleted successfully'
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        db.rollback()
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )
