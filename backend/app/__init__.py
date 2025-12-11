from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker


def cors_tween_factory(handler, registry):
    """CORS tween to add headers to all responses"""
    def cors_tween(request):
        response = handler(request)
        response.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Max-Age': '3600'
        })
        return response
    return cors_tween


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    config = Configurator(settings=settings)
    
    # Add CORS tween
    config.add_tween('app.cors_tween_factory')
    
    # Database configuration
    engine = engine_from_config(settings, 'sqlalchemy.')
    session_factory = sessionmaker(bind=engine)
    
    def get_db(request):
        session = session_factory()
        def cleanup(request):
            session.close()
        request.add_finished_callback(cleanup)
        return session
    
    config.add_request_method(get_db, 'dbsession', reify=True)
    
    # CORS OPTIONS route (catch-all for preflight)
    config.add_route('options', '/*path', request_method='OPTIONS')
    
    # Routes - Authentication
    config.add_route('home', '/')
    config.add_route('auth_register', '/api/auth/register')
    config.add_route('auth_login', '/api/auth/login')
    config.add_route('auth_logout', '/api/auth/logout')
    config.add_route('auth_me', '/api/auth/me')
    
    # Routes - Classes
    config.add_route('api_classes', '/api/classes')
    config.add_route('api_class', '/api/classes/{id}')
    config.add_route('api_class_participants', '/api/classes/{id}/participants')
    
    # Routes - Bookings
    config.add_route('api_bookings', '/api/bookings')
    config.add_route('api_booking', '/api/bookings/{id}')
    config.add_route('api_my_bookings', '/api/bookings/my')
    
    # Routes - Attendance
    config.add_route('api_attendance', '/api/attendance')
    config.add_route('api_my_attendance', '/api/attendance/my')
    
    # Routes - Membership
    config.add_route('api_membership_plans', '/api/membership/plans')
    config.add_route('api_my_membership', '/api/membership/my')
    config.add_route('api_members', '/api/members')
    
    # Scan views
    config.scan('.views')
    
    return config.make_wsgi_app()
