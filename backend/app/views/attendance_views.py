"""
Attendance views - Mark attendance, view attendance history
"""
from pyramid.view import view_config
from pyramid.response import Response
import json
from datetime import datetime


# Mock attendance data
mock_attendance = [
    {
        'id': 1,
        'booking_id': 1,
        'attended': True,
        'date': '2025-12-12T07:15:00',
        'booking': {
            'id': 1,
            'member': {
                'user': {'name': 'Jane Member'}
            },
            'class': {
                'name': 'Yoga Morning',
                'schedule': '2025-12-12T07:00:00'
            }
        }
    }
]


@view_config(route_name='api_attendance', renderer='json', request_method='GET')
def get_attendance(request):
    """Get all attendance records (Trainer only)"""
    try:
        # Filter by class_id if provided
        class_id = request.params.get('class_id')
        
        filtered_attendance = mock_attendance
        if class_id:
            # Filter by class_id
            pass
        
        return {
            'status': 'success',
            'data': filtered_attendance,
            'count': len(filtered_attendance)
        }
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json'
        )


@view_config(route_name='api_attendance', renderer='json', request_method='POST')
def mark_attendance(request):
    """Mark attendance for a booking (Trainer only)"""
    try:
        data = request.json_body
        
        # Validation
        if 'booking_id' not in data or 'attended' not in data:
            return Response(
                json.dumps({'status': 'error', 'message': 'booking_id and attended are required'}),
                status=400,
                content_type='application/json'
            )
        
        booking_id = data['booking_id']
        attended = data['attended']
        
        # Check if attendance already exists
        existing = next((a for a in mock_attendance if a['booking_id'] == booking_id), None)
        
        if existing:
            # Update existing attendance
            existing['attended'] = attended
            existing['date'] = datetime.utcnow().isoformat()
            
            return {
                'status': 'success',
                'message': 'Attendance updated successfully',
                'data': existing
            }
        else:
            # Create new attendance
            new_attendance = {
                'id': len(mock_attendance) + 1,
                'booking_id': booking_id,
                'attended': attended,
                'date': datetime.utcnow().isoformat(),
                'booking': {
                    'id': booking_id,
                    'member': {'user': {'name': 'Member Name'}},
                    'class': {'name': 'Class Name'}
                }
            }
            
            mock_attendance.append(new_attendance)
            
            return {
                'status': 'success',
                'message': 'Attendance marked successfully',
                'data': new_attendance
            }
        
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json'
        )


@view_config(route_name='api_my_attendance', renderer='json', request_method='GET')
def get_my_attendance(request):
    """Get attendance history for current authenticated member"""
    try:
        # In real app, get member_id from JWT token
        # Filter attendance by member's bookings
        
        my_attendance = mock_attendance  # Mock - show all
        
        return {
            'status': 'success',
            'data': my_attendance,
            'count': len(my_attendance)
        }
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json'
        )
