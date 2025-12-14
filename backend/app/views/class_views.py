"""
Class management views - CRUD operations for gym classes
"""
from pyramid.view import view_config
from pyramid.response import Response
import json
from datetime import datetime


# Mock data untuk sementara
mock_classes = [
    {
        'id': 1,
        'trainer_id': 2,
        'name': 'Yoga Morning',
        'description': 'Relaxing yoga session to start your day',
        'schedule': '2025-12-15T07:00:00',
        'capacity': 20,
        'booked_count': 5,
        'available_slots': 15,
        'trainer': {'id': 2, 'name': 'John Trainer', 'email': 'john@example.com'}
    },
    {
        'id': 2,
        'trainer_id': 2,
        'name': 'HIIT Workout',
        'description': 'High intensity interval training',
        'schedule': '2025-12-15T18:00:00',
        'capacity': 15,
        'booked_count': 10,
        'available_slots': 5,
        'trainer': {'id': 2, 'name': 'John Trainer', 'email': 'john@example.com'}
    }
]


@view_config(route_name='api_classes', renderer='json', request_method='GET')
def get_classes(request):
    """Get all classes (with optional filtering)"""
    try:
        # Filter by date if provided
        date_filter = request.params.get('date')
        
        filtered_classes = mock_classes
        if date_filter:
            # Filter logic here
            pass
        
        return {
            'status': 'success',
            'data': filtered_classes,
            'count': len(filtered_classes)
        }
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json'
        )


@view_config(route_name='api_classes', renderer='json', request_method='POST')
def create_class(request):
    """Create new class (Trainer only)"""
    try:
        data = request.json_body
        
        # Validation
        required_fields = ['name', 'description', 'schedule', 'capacity']
        if not all(field in data for field in required_fields):
            return Response(
                json.dumps({'status': 'error', 'message': 'Missing required fields'}),
                status=400,
                content_type='application/json'
            )
        
        # Create new class (mock)
        new_class = {
            'id': len(mock_classes) + 1,
            'trainer_id': 2,  # Mock trainer ID
            'name': data['name'],
            'description': data['description'],
            'schedule': data['schedule'],
            'capacity': data['capacity'],
            'booked_count': 0,
            'available_slots': data['capacity'],
            'trainer': {'id': 2, 'name': 'John Trainer', 'email': 'john@example.com'}
        }
        
        mock_classes.append(new_class)
        
        return {
            'status': 'success',
            'message': 'Class created successfully',
            'data': new_class
        }
        
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json'
        )


@view_config(route_name='api_class', renderer='json', request_method='GET')
def get_class(request):
    """Get single class by ID"""
    try:
        class_id = int(request.matchdict['id'])
        
        # Find class
        gym_class = next((c for c in mock_classes if c['id'] == class_id), None)
        
        if not gym_class:
            return Response(
                json.dumps({'status': 'error', 'message': 'Class not found'}),
                status=404,
                content_type='application/json'
            )
        
        return {
            'status': 'success',
            'data': gym_class
        }
        
    except ValueError:
        return Response(
            json.dumps({'status': 'error', 'message': 'Invalid class ID'}),
            status=400,
            content_type='application/json'
        )
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json'
        )


@view_config(route_name='api_class', renderer='json', request_method='PUT')
def update_class(request):
    """Update class by ID (Trainer only)"""
    try:
        class_id = int(request.matchdict['id'])
        data = request.json_body
        
        # Find class
        gym_class = next((c for c in mock_classes if c['id'] == class_id), None)
        
        if not gym_class:
            return Response(
                json.dumps({'status': 'error', 'message': 'Class not found'}),
                status=404,
                content_type='application/json'
            )
        
        # Update fields
        if 'name' in data:
            gym_class['name'] = data['name']
        if 'description' in data:
            gym_class['description'] = data['description']
        if 'schedule' in data:
            gym_class['schedule'] = data['schedule']
        if 'capacity' in data:
            gym_class['capacity'] = data['capacity']
            gym_class['available_slots'] = data['capacity'] - gym_class['booked_count']
        
        return {
            'status': 'success',
            'message': 'Class updated successfully',
            'data': gym_class
        }
        
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json'
        )


@view_config(route_name='api_class', renderer='json', request_method='DELETE')
def delete_class(request):
    """Delete class by ID (Trainer only)"""
    try:
        class_id = int(request.matchdict['id'])
        
        # Find and remove class
        global mock_classes
        original_length = len(mock_classes)
        mock_classes = [c for c in mock_classes if c['id'] != class_id]
        
        if len(mock_classes) == original_length:
            return Response(
                json.dumps({'status': 'error', 'message': 'Class not found'}),
                status=404,
                content_type='application/json'
            )
        
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
