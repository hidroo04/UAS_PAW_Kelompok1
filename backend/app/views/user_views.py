from pyramid.view import view_config
from pyramid.response import Response
import json
from ..models import User, UserRole


@view_config(route_name='home', renderer='json')
def home_view(request):
    return {
        'message': 'Welcome to GymBook API',
        'status': 'success',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth/*',
            'classes': '/api/classes',
            'bookings': '/api/bookings',
            'attendance': '/api/attendance',
            'membership': '/api/membership/*'
        }
    }


@view_config(route_name='api_users', renderer='json', request_method='GET')
def get_users(request):
    """Get users with optional role filter"""
    try:
        db = request.dbsession
        query = db.query(User)
        
        # Filter by role if provided
        role = request.params.get('role')
        if role:
            try:
                role_enum = UserRole[role.upper()]
                query = query.filter(User.role == role_enum)
            except KeyError:
                return Response(
                    json.dumps({'status': 'error', 'message': f'Invalid role: {role}'}),
                    status=400,
                    content_type='application/json'
                )
        
        users = query.all()
        
        users_data = []
        for user in users:
            users_data.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role.value if user.role else None
            })
        
        return {
            'status': 'success',
            'data': users_data,
            'count': len(users_data)
        }
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )
