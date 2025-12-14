"""
Gym Booking System - Backend Application
Modern, professional, and well-structured Pyramid application
"""
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from .config import config as app_config


def cors_tween_factory(handler, registry):
    """
    CORS tween to add headers to all responses
    Enables cross-origin requests from frontend
    """
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
    """
    This function returns a Pyramid WSGI application.
    It configures the application with database, routes, and views.
    """
    config = Configurator(settings=settings)
    
    # Add CORS tween for cross-origin support
    config.add_tween('app.cors_tween_factory')
    
    # Database configuration
    # Use environment variable if available, otherwise use settings
    if 'sqlalchemy.url' not in settings:
        settings['sqlalchemy.url'] = app_config.DATABASE_URL
    
    engine = engine_from_config(settings, 'sqlalchemy.')
    session_factory = sessionmaker(bind=engine)
    
    def get_db(request):
        """
        Database session factory
        Automatically handles session lifecycle
        """
        session = session_factory()
        def cleanup(request):
            session.close()
        request.add_finished_callback(cleanup)
        return session
    
    config.add_request_method(get_db, 'dbsession', reify=True)
    
    # CORS OPTIONS route (catch-all for preflight requests)
    config.add_route('options', '/*path', request_method='OPTIONS')
    
    # Include all routes from modular route files
    from .routes import include_routes
    include_routes(config)
    
    # Scan views to register all view callables
    config.scan('.views')
    
    return config.make_wsgi_app()
