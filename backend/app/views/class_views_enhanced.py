"""
Enhanced Class management views with PostgreSQL integration
"""
from pyramid.view import view_config
from pyramid.response import Response
import json
from datetime import datetime, date
from sqlalchemy import func, or_
from ..models import GymClass, User, Booking
from ..utils.auth import get_token_from_header, decode_jwt_token


@view_config(route_name='api_classes', renderer='json', request_method='GET')
def get_classes(request):
    """Get all classes with filtering and search"""
    try:
        db = request.dbsession
        
        # Base query
        query = db.query(GymClass).join(User, GymClass.trainer_id == User.id)
        
        # Search filter
        search = request.params.get('search')
        if search:
            query = query.filter(
                or_(
                    GymClass.name.ilike(f'%{search}%'),
                    GymClass.description.ilike(f'%{search}%')
                )
            )
        
        # Date filter
        date_filter = request.params.get('date')
        if date_filter:
            try:
                filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
                query = query.filter(func.date(GymClass.schedule) == filter_date)
            except ValueError:
                pass
        
        # Category/Type filter - DISABLED: column doesn't exist in DB
        # class_type = request.params.get('type')
        # if class_type:
        #     query = query.filter(GymClass.class_type == class_type)
        
        # Difficulty filter - DISABLED: column doesn't exist in DB
        # difficulty = request.params.get('difficulty')
        # if difficulty:
        #     query = query.filter(GymClass.difficulty == difficulty)
        
        # Get all classes
        classes = query.order_by(GymClass.schedule).all()
        
        # Format response
        classes_data = []
        for gym_class in classes:
            # Count bookings
            booked_count = db.query(Booking).filter(
                Booking.class_id == gym_class.id
            ).count()
            
            classes_data.append({
                'id': gym_class.id,
                'name': gym_class.name,
                'description': gym_class.description,
                'schedule': gym_class.schedule.isoformat() if gym_class.schedule else None,
                'duration': 60,  # default value since column doesn't exist
                'capacity': gym_class.capacity,
                'booked_count': booked_count,
                'available_slots': gym_class.capacity - booked_count,
                'class_type': 'General',  # default value since column doesn't exist
                'difficulty': 'Intermediate',  # default value since column doesn't exist
                'trainer': {
                    'id': gym_class.trainer.id,
                    'name': gym_class.trainer.name,
                    'email': gym_class.trainer.email
                } if gym_class.trainer else None
            })
        
        return {
            'status': 'success',
            'data': classes_data,
            'count': len(classes_data)
        }
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json'
        )


@view_config(route_name='api_class', renderer='json', request_method='GET')
def get_class(request):
    """Get single class by ID with details"""
    try:
        db = request.dbsession
        class_id = request.matchdict['id']
        
        gym_class = db.query(GymClass).filter(GymClass.id == class_id).first()
        
        if not gym_class:
            return Response(
                json.dumps({'status': 'error', 'message': 'Class not found'}),
                status=404,
                content_type='application/json'
            )
        
        # Count bookings
        booked_count = db.query(Booking).filter(
            Booking.class_id == gym_class.id,
            Booking.status == 'CONFIRMED'
        ).count()
        
        # Get participants
        participants = db.query(User).join(Booking).filter(
            Booking.class_id == gym_class.id,
            Booking.status == 'CONFIRMED'
        ).all()
        
        return {
            'status': 'success',
            'data': {
                'id': gym_class.id,
                'name': gym_class.name,
                'description': gym_class.description,
                'schedule': gym_class.schedule.isoformat() if gym_class.schedule else None,
                'duration': gym_class.duration,
                'capacity': gym_class.capacity,
                'booked_count': booked_count,
                'available_slots': gym_class.capacity - booked_count,
                'class_type': gym_class.class_type if hasattr(gym_class, 'class_type') else 'General',
                'difficulty': gym_class.difficulty if hasattr(gym_class, 'difficulty') else 'Intermediate',
                'trainer': {
                    'id': gym_class.trainer.id,
                    'name': gym_class.trainer.name,
                    'email': gym_class.trainer.email
                } if gym_class.trainer else None,
                'participants': [{'id': p.id, 'name': p.name} for p in participants]
            }
        }
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json'
        )


@view_config(route_name='api_classes', renderer='json', request_method='POST')
def create_class(request):
    """Create new class (Trainer/Admin only)"""
    try:
        # Check authentication
        token = get_token_from_header(request)
        if not token:
            return Response(
                json.dumps({'status': 'error', 'message': 'Authentication required'}),
                status=401,
                content_type='application/json'
            )
        
        payload = decode_jwt_token(token)
        
        # Check role
        if payload.get('role') not in ['ADMIN', 'TRAINER']:
            return Response(
                json.dumps({'status': 'error', 'message': 'Insufficient permissions'}),
                status=403,
                content_type='application/json'
            )
        
        db = request.dbsession
        data = request.json_body
        
        # Validation
        required_fields = ['name', 'description', 'schedule', 'duration', 'capacity']
        if not all(field in data for field in required_fields):
            return Response(
                json.dumps({'status': 'error', 'message': 'Missing required fields'}),
                status=400,
                content_type='application/json'
            )
        
        # Parse schedule
        try:
            schedule = datetime.fromisoformat(data['schedule'].replace('Z', '+00:00'))
        except:
            schedule = datetime.strptime(data['schedule'], '%Y-%m-%d %H:%M:%S')
        
        # Create new class
        new_class = GymClass(
            trainer_id=payload.get('user_id'),
            name=data['name'],
            description=data['description'],
            schedule=schedule,
            duration=data['duration'],
            capacity=data['capacity']
        )
        
        # Optional fields
        if 'class_type' in data and hasattr(GymClass, 'class_type'):
            new_class.class_type = data['class_type']
        if 'difficulty' in data and hasattr(GymClass, 'difficulty'):
            new_class.difficulty = data['difficulty']
        
        db.add(new_class)
        db.commit()
        
        return {
            'status': 'success',
            'message': 'Class created successfully',
            'data': {
                'id': new_class.id,
                'name': new_class.name,
                'schedule': new_class.schedule.isoformat()
            }
        }
        
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json'
        )


@view_config(route_name='api_class', renderer='json', request_method='PUT')
def update_class(request):
    """Update existing class (Trainer/Admin only)"""
    try:
        # Check authentication
        token = get_token_from_header(request)
        if not token:
            return Response(
                json.dumps({'status': 'error', 'message': 'Authentication required'}),
                status=401,
                content_type='application/json'
            )
        
        payload = decode_jwt_token(token)
        
        # Check role
        if payload.get('role') not in ['ADMIN', 'TRAINER']:
            return Response(
                json.dumps({'status': 'error', 'message': 'Insufficient permissions'}),
                status=403,
                content_type='application/json'
            )
        
        db = request.dbsession
        class_id = request.matchdict['id']
        data = request.json_body
        
        # Get class
        gym_class = db.query(GymClass).filter(GymClass.id == class_id).first()
        
        if not gym_class:
            return Response(
                json.dumps({'status': 'error', 'message': 'Class not found'}),
                status=404,
                content_type='application/json'
            )
        
        # Update fields
        if 'name' in data:
            gym_class.name = data['name']
        if 'description' in data:
            gym_class.description = data['description']
        if 'schedule' in data:
            try:
                gym_class.schedule = datetime.fromisoformat(data['schedule'].replace('Z', '+00:00'))
            except:
                gym_class.schedule = datetime.strptime(data['schedule'], '%Y-%m-%d %H:%M:%S')
        if 'duration' in data:
            gym_class.duration = data['duration']
        if 'capacity' in data:
            gym_class.capacity = data['capacity']
        if 'class_type' in data and hasattr(gym_class, 'class_type'):
            gym_class.class_type = data['class_type']
        if 'difficulty' in data and hasattr(gym_class, 'difficulty'):
            gym_class.difficulty = data['difficulty']
        
        db.commit()
        
        return {
            'status': 'success',
            'message': 'Class updated successfully',
            'data': {
                'id': gym_class.id,
                'name': gym_class.name
            }
        }
        
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json'
        )


@view_config(route_name='api_class', renderer='json', request_method='DELETE')
def delete_class(request):
    """Delete class (Admin only)"""
    try:
        # Check authentication
        token = get_token_from_header(request)
        if not token:
            return Response(
                json.dumps({'status': 'error', 'message': 'Authentication required'}),
                status=401,
                content_type='application/json'
            )
        
        payload = decode_jwt_token(token)
        
        # Check role
        if payload.get('role') != 'ADMIN':
            return Response(
                json.dumps({'status': 'error', 'message': 'Admin access required'}),
                status=403,
                content_type='application/json'
            )
        
        db = request.dbsession
        class_id = request.matchdict['id']
        
        # Get class
        gym_class = db.query(GymClass).filter(GymClass.id == class_id).first()
        
        if not gym_class:
            return Response(
                json.dumps({'status': 'error', 'message': 'Class not found'}),
                status=404,
                content_type='application/json'
            )
        
        # Check if there are bookings
        booking_count = db.query(Booking).filter(Booking.class_id == class_id).count()
        if booking_count > 0:
            return Response(
                json.dumps({'status': 'error', 'message': 'Cannot delete class with existing bookings'}),
                status=400,
                content_type='application/json'
            )
        
        db.delete(gym_class)
        db.commit()
        
        return {
            'status': 'success',
            'message': 'Class deleted successfully'
        }
        
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json'
        )


@view_config(route_name='api_class_participants', renderer='json', request_method='GET')
def get_class_participants(request):
    """Get list of participants for a class"""
    try:
        # Check authentication
        token = get_token_from_header(request)
        if not token:
            return Response(
                json.dumps({'status': 'error', 'message': 'Authentication required'}),
                status=401,
                content_type='application/json'
            )
        
        db = request.dbsession
        class_id = request.matchdict['id']
        
        # Get class
        gym_class = db.query(GymClass).filter(GymClass.id == class_id).first()
        
        if not gym_class:
            return Response(
                json.dumps({'status': 'error', 'message': 'Class not found'}),
                status=404,
                content_type='application/json'
            )
        
        # Get participants with bookings
        participants = db.query(User, Booking).join(Booking).filter(
            Booking.class_id == class_id,
            Booking.status == 'CONFIRMED'
        ).all()
        
        participants_data = [{
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'booking_id': booking.id,
            'booking_date': booking.booking_date.isoformat() if booking.booking_date else None
        } for user, booking in participants]
        
        return {
            'status': 'success',
            'data': {
                'class_id': gym_class.id,
                'class_name': gym_class.name,
                'participants': participants_data,
                'total_participants': len(participants_data),
                'capacity': gym_class.capacity,
                'available_slots': gym_class.capacity - len(participants_data)
            }
        }
        
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json'
        )
