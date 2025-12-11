"""
Booking views - Book classes, view bookings, cancel bookings
"""
from pyramid.view import view_config
from pyramid.response import Response
import json
from datetime import datetime


# Mock bookings data
mock_bookings = [
    {
        'id': 1,
        'member_id': 1,
        'class_id': 1,
        'booking_date': '2025-12-12T10:00:00',
        'member': {
            'id': 1,
            'user_id': 1,
            'membership_plan': 'Premium',
            'user': {'id': 1, 'name': 'Jane Member', 'email': 'jane@example.com'}
        },
        'class': {
            'id': 1,
            'name': 'Yoga Morning',
            'schedule': '2025-12-15T07:00:00',
            'trainer': {'name': 'John Trainer'}
        }
    }
]


@view_config(route_name='api_bookings', renderer='json', request_method='GET')
def get_bookings(request):
    """Get all bookings (filtered by user role)"""
    try:
        # In real app, filter by authenticated user
        # For trainer: show all bookings for their classes
        # For member: show only their bookings
        
        return {
            'status': 'success',
            'data': mock_bookings,
            'count': len(mock_bookings)
        }
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json'
        )


@view_config(route_name='api_bookings', renderer='json', request_method='POST')
def create_booking(request):
    """Create new booking (Member only)"""
    try:
        data = request.json_body
        
        # Validation
        if 'class_id' not in data:
            return Response(
                json.dumps({'status': 'error', 'message': 'class_id is required'}),
                status=400,
                content_type='application/json'
            )
        
        class_id = data['class_id']
        
        # Check if class exists and has available slots (mock)
        # In real app, query database
        
        # Check if member already booked this class
        existing_booking = next(
            (b for b in mock_bookings if b['member_id'] == 1 and b['class_id'] == class_id),
            None
        )
        
        if existing_booking:
            return Response(
                json.dumps({'status': 'error', 'message': 'You have already booked this class'}),
                status=400,
                content_type='application/json'
            )
        
        # Create booking (mock)
        new_booking = {
            'id': len(mock_bookings) + 1,
            'member_id': 1,  # Mock member ID
            'class_id': class_id,
            'booking_date': datetime.utcnow().isoformat(),
            'member': {
                'id': 1,
                'user_id': 1,
                'membership_plan': 'Premium',
                'user': {'id': 1, 'name': 'Jane Member', 'email': 'jane@example.com'}
            },
            'class': {
                'id': class_id,
                'name': 'Sample Class',
                'schedule': '2025-12-15T10:00:00'
            }
        }
        
        mock_bookings.append(new_booking)
        
        return {
            'status': 'success',
            'message': 'Class booked successfully',
            'data': new_booking
        }
        
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json'
        )


@view_config(route_name='api_booking', renderer='json', request_method='GET')
def get_booking(request):
    """Get single booking by ID"""
    try:
        booking_id = int(request.matchdict['id'])
        
        booking = next((b for b in mock_bookings if b['id'] == booking_id), None)
        
        if not booking:
            return Response(
                json.dumps({'status': 'error', 'message': 'Booking not found'}),
                status=404,
                content_type='application/json'
            )
        
        return {
            'status': 'success',
            'data': booking
        }
        
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json'
        )


@view_config(route_name='api_booking', renderer='json', request_method='DELETE')
def cancel_booking(request):
    """Cancel booking (Member only - own bookings)"""
    try:
        booking_id = int(request.matchdict['id'])
        
        # Find and remove booking
        global mock_bookings
        original_length = len(mock_bookings)
        mock_bookings = [b for b in mock_bookings if b['id'] != booking_id]
        
        if len(mock_bookings) == original_length:
            return Response(
                json.dumps({'status': 'error', 'message': 'Booking not found'}),
                status=404,
                content_type='application/json'
            )
        
        return {
            'status': 'success',
            'message': 'Booking cancelled successfully'
        }
        
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json'
        )


@view_config(route_name='api_my_bookings', renderer='json', request_method='GET')
def get_my_bookings(request):
    """Get bookings for current authenticated member"""
    try:
        # In real app, get user_id from JWT token
        # Filter bookings by member_id
        
        my_bookings = [b for b in mock_bookings if b['member_id'] == 1]  # Mock member ID
        
        return {
            'status': 'success',
            'data': my_bookings,
            'count': len(my_bookings)
        }
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json'
        )
