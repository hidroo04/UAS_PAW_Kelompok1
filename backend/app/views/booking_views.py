"""
Booking views - Book classes, view bookings, cancel bookings
"""
from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy import and_
import json
from datetime import datetime
from ..models import Booking, GymClass, User, Member
from sqlalchemy.orm import joinedload
from ..utils.auth import get_token_from_header, decode_jwt_token
import jwt


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


@view_config(route_name='api_bookings', renderer='json', request_method='GET')
def get_bookings(request):
    """Get all bookings from database"""
    try:
        db = request.dbsession
        
        # Query bookings with relationships
        bookings = db.query(Booking).options(
            joinedload(Booking.gym_class).joinedload(GymClass.trainer),
            joinedload(Booking.member).joinedload(Member.user)
        ).all()
        
        bookings_data = []
        for booking in bookings:
            booking_dict = {
                'id': booking.id,
                'member_id': booking.member_id,
                'class_id': booking.class_id,
                'booking_date': booking.booking_date.isoformat() if booking.booking_date else None,
                'class': {
                    'id': booking.gym_class.id,
                    'name': booking.gym_class.name,
                    'description': booking.gym_class.description,
                    'schedule': booking.gym_class.schedule.isoformat() if booking.gym_class.schedule else None,
                    'capacity': booking.gym_class.capacity,
                    'trainer': {
                        'id': booking.gym_class.trainer.id,
                        'name': booking.gym_class.trainer.name,
                        'email': booking.gym_class.trainer.email
                    } if booking.gym_class.trainer else None
                } if booking.gym_class else None,
                'member': {
                    'id': booking.member.id,
                    'user_id': booking.member.user_id,
                    'user': {
                        'id': booking.member.user.id,
                        'name': booking.member.user.name,
                        'email': booking.member.user.email
                    } if booking.member.user else None
                } if booking.member else None
            }
            bookings_data.append(booking_dict)
        
        return {
            'status': 'success',
            'data': bookings_data,
            'count': len(bookings_data)
        }
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )


@view_config(route_name='api_bookings', renderer='json', request_method='POST')
def create_booking(request):
    """Create new booking in database"""
    try:
        db = request.dbsession
        data = request.json_body
        
        # Validation
        if 'class_id' not in data:
            return Response(
                json.dumps({'status': 'error', 'message': 'class_id is required'}),
                status=400,
                content_type='application/json; charset=utf-8'
            )
        
        class_id = data['class_id']
        
        # Get user_id from token
        user_id = get_authenticated_user_id(request)
        if not user_id:
            return Response(
                json.dumps({'status': 'error', 'message': 'Authentication required'}),
                status=401,
                content_type='application/json; charset=utf-8'
            )
        
        # Find member by user_id
        member = db.query(Member).filter(Member.user_id == user_id).first()
        if not member:
            return Response(
                json.dumps({'status': 'error', 'message': 'Member not found'}),
                status=404,
                content_type='application/json; charset=utf-8'
            )
        
        # Check if class exists
        gym_class = db.query(GymClass).filter(GymClass.id == class_id).first()
        if not gym_class:
            return Response(
                json.dumps({'status': 'error', 'message': 'Class not found'}),
                status=404,
                content_type='application/json; charset=utf-8'
            )
        
        # Check if already booked
        existing_booking = db.query(Booking).filter(
            and_(
                Booking.member_id == member.id,
                Booking.class_id == class_id
            )
        ).first()
        
        if existing_booking:
            return Response(
                json.dumps({'status': 'error', 'message': 'You have already booked this class'}),
                status=400,
                content_type='application/json; charset=utf-8'
            )
        
        # Check capacity
        current_bookings = db.query(Booking).filter(Booking.class_id == class_id).count()
        if current_bookings >= gym_class.capacity:
            return Response(
                json.dumps({'status': 'error', 'message': 'Class is fully booked'}),
                status=400,
                content_type='application/json; charset=utf-8'
            )
        
        # Create booking
        new_booking = Booking(
            member_id=member.id,
            class_id=class_id,
            booking_date=datetime.utcnow()
        )
        
        db.add(new_booking)
        db.flush()  # Get the ID
        
        # Load relationships for response
        db.refresh(new_booking)
        booking_with_relations = db.query(Booking).options(
            joinedload(Booking.gym_class).joinedload(GymClass.trainer),
            joinedload(Booking.member).joinedload(Member.user)
        ).filter(Booking.id == new_booking.id).first()
        
        booking_dict = {
            'id': booking_with_relations.id,
            'member_id': booking_with_relations.member_id,
            'class_id': booking_with_relations.class_id,
            'booking_date': booking_with_relations.booking_date.isoformat(),
            'class': {
                'id': booking_with_relations.gym_class.id,
                'name': booking_with_relations.gym_class.name,
                'schedule': booking_with_relations.gym_class.schedule.isoformat() if booking_with_relations.gym_class.schedule else None,
                'trainer': {
                    'name': booking_with_relations.gym_class.trainer.name
                } if booking_with_relations.gym_class.trainer else None
            }
        }
        
        return {
            'status': 'success',
            'message': 'Class booked successfully',
            'data': booking_dict
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )


@view_config(route_name='api_booking', renderer='json', request_method='GET')
def get_booking(request):
    """Get single booking by ID from database"""
    try:
        db = request.dbsession
        booking_id = int(request.matchdict['id'])
        
        booking = db.query(Booking).options(
            joinedload(Booking.gym_class).joinedload(GymClass.trainer),
            joinedload(Booking.member).joinedload(Member.user)
        ).filter(Booking.id == booking_id).first()
        
        if not booking:
            return Response(
                json.dumps({'status': 'error', 'message': 'Booking not found'}),
                status=404,
                content_type='application/json; charset=utf-8'
            )
        
        booking_dict = {
            'id': booking.id,
            'member_id': booking.member_id,
            'class_id': booking.class_id,
            'booking_date': booking.booking_date.isoformat() if booking.booking_date else None,
            'class': {
                'id': booking.gym_class.id,
                'name': booking.gym_class.name,
                'description': booking.gym_class.description,
                'schedule': booking.gym_class.schedule.isoformat() if booking.gym_class.schedule else None,
                'capacity': booking.gym_class.capacity,
                'trainer': {
                    'id': booking.gym_class.trainer.id,
                    'name': booking.gym_class.trainer.name
                } if booking.gym_class.trainer else None
            } if booking.gym_class else None,
            'member': {
                'id': booking.member.id,
                'user': {
                    'name': booking.member.user.name,
                    'email': booking.member.user.email
                } if booking.member.user else None
            } if booking.member else None
        }
        
        return {
            'status': 'success',
            'data': booking_dict
        }
        
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )


@view_config(route_name='api_booking', renderer='json', request_method='DELETE')
def cancel_booking(request):
    """Cancel booking from database"""
    try:
        db = request.dbsession
        booking_id = int(request.matchdict['id'])
        
        # Get user_id from token
        user_id = get_authenticated_user_id(request)
        if not user_id:
            return Response(
                json.dumps({'status': 'error', 'message': 'Authentication required'}),
                status=401,
                content_type='application/json; charset=utf-8'
            )
        
        # Find member
        member = db.query(Member).filter(Member.user_id == user_id).first()
        if not member:
            return Response(
                json.dumps({'status': 'error', 'message': 'Member not found'}),
                status=404,
                content_type='application/json; charset=utf-8'
            )
        
        # Find booking
        booking = db.query(Booking).filter(
            and_(
                Booking.id == booking_id,
                Booking.member_id == member.id  # Ensure member owns this booking
            )
        ).first()
        
        if not booking:
            return Response(
                json.dumps({'status': 'error', 'message': 'Booking not found'}),
                status=404,
                content_type='application/json; charset=utf-8'
            )
        
        # Delete booking
        db.delete(booking)
        
        return {
            'status': 'success',
            'message': 'Booking cancelled successfully'
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )


@view_config(route_name='api_my_bookings', renderer='json', request_method='GET')
def get_my_bookings(request):
    """Get bookings for current authenticated member from database"""
    try:
        db = request.dbsession
        
        # Get user_id from token
        user_id = get_authenticated_user_id(request)
        if not user_id:
            return Response(
                json.dumps({'status': 'error', 'message': 'Authentication required'}),
                status=401,
                content_type='application/json; charset=utf-8'
            )
        
        # Find member by user_id
        member = db.query(Member).filter(Member.user_id == user_id).first()
        if not member:
            return {
                'status': 'success',
                'data': [],
                'count': 0
            }
        
        # Query bookings for this member
        bookings = db.query(Booking).options(
            joinedload(Booking.gym_class).joinedload(GymClass.trainer),
            joinedload(Booking.member).joinedload(Member.user)
        ).filter(Booking.member_id == member.id).all()
        
        bookings_data = []
        for booking in bookings:
            booking_dict = {
                'id': booking.id,
                'member_id': booking.member_id,
                'class_id': booking.class_id,
                'booking_date': booking.booking_date.isoformat() if booking.booking_date else None,
                'class': {
                    'id': booking.gym_class.id,
                    'name': booking.gym_class.name,
                    'description': booking.gym_class.description,
                    'schedule': booking.gym_class.schedule.isoformat() if booking.gym_class.schedule else None,
                    'capacity': booking.gym_class.capacity,
                    'trainer': {
                        'id': booking.gym_class.trainer.id,
                        'name': booking.gym_class.trainer.name,
                        'email': booking.gym_class.trainer.email
                    } if booking.gym_class.trainer else None
                } if booking.gym_class else None
            }
            bookings_data.append(booking_dict)
        
        return {
            'status': 'success',
            'data': bookings_data,
            'count': len(bookings_data)
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )
