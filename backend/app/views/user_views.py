from pyramid.view import view_config


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
