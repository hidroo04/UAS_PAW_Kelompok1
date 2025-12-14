"""
Authentication Routes
Handles user registration, login, logout, and profile
"""

def includeme(config):
    """Configure authentication routes"""
    
    # Home route
    config.add_route('home', '/')
    
    # Authentication routes
    config.add_route('auth_register', '/api/auth/register')
    config.add_route('auth_login', '/api/auth/login')
    config.add_route('auth_logout', '/api/auth/logout')
    config.add_route('auth_me', '/api/auth/me')
    
    # User management routes
    config.add_route('api_users', '/api/users')
    config.add_route('api_user', '/api/users/{id}')
