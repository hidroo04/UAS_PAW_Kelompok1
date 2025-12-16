"""
Authentication utilities
Provides JWT token management and password hashing
"""
import jwt
import hashlib
from datetime import datetime, timedelta
from functools import wraps
from pyramid.response import Response
import json
from ..config import config


def hash_password(password: str) -> str:
    """
    Hash password using SHA256
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if plain password matches hashed password
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to compare against
        
    Returns:
        True if passwords match, False otherwise
    """
    return hash_password(plain_password) == hashed_password


def create_jwt_token(user_id: int, email: str, role: str) -> str:
    """
    Create JWT token for authenticated user
    
    Args:
        user_id: User ID
        email: User email
        role: User role (ADMIN, TRAINER, MEMBER)
        
    Returns:
        JWT token string
    """
    payload = {
        'user_id': user_id,
        'email': email,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=config.JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    return token


def decode_jwt_token(token: str) -> dict:
    """
    Decode and verify JWT token
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded payload dictionary
        
    Raises:
        jwt.ExpiredSignatureError: If token has expired
        jwt.InvalidTokenError: If token is invalid
    """
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError("Token has expired")
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError("Invalid token")


def get_token_from_header(request) -> str:
    """
    Extract JWT token from Authorization header
    
    Args:
        request: Pyramid request object
        
    Returns:
        JWT token string or None
    """
    # Pyramid/WebOb uses environ for HTTP headers
    # HTTP_AUTHORIZATION is the CGI-style header name
    auth_header = request.environ.get('HTTP_AUTHORIZATION', '')
    
    if not auth_header:
        # Fallback to request.headers
        auth_header = request.headers.get('Authorization', '')
    
    if auth_header.startswith('Bearer ') or auth_header.startswith('bearer '):
        parts = auth_header.split(' ', 1)
        if len(parts) == 2:
            return parts[1]
    
    return None


def require_auth(allowed_roles=None):
    """
    Decorator to require authentication for views
    
    Args:
        allowed_roles: List of allowed roles (optional)
        
    Usage:
        @require_auth(['ADMIN', 'TRAINER'])
        @view_config(route_name='my_route')
        def my_view(request):
            # request.user will contain authenticated user info
            pass
    """
    if allowed_roles is None:
        allowed_roles = []
    
    def decorator(func):
        @wraps(func)
        def wrapper(request):
            token = get_token_from_header(request)
            
            if not token:
                return Response(
                    json.dumps({'status': 'error', 'message': 'Authentication required'}),
                    status=401,
                    content_type='application/json'
                )
            
            try:
                payload = decode_jwt_token(token)
                request.user = payload
                
                # Check role if specified
                if allowed_roles and payload.get('role') not in allowed_roles:
                    return Response(
                        json.dumps({'status': 'error', 'message': 'Insufficient permissions'}),
                        status=403,
                        content_type='application/json'
                    )
                
                return func(request)
                
            except jwt.ExpiredSignatureError:
                return Response(
                    json.dumps({'status': 'error', 'message': 'Token has expired'}),
                    status=401,
                    content_type='application/json'
                )
            except jwt.InvalidTokenError:
                return Response(
                    json.dumps({'status': 'error', 'message': 'Invalid token'}),
                    status=401,
                    content_type='application/json'
                )
        
        return wrapper
    return decorator
