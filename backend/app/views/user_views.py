from pyramid.view import view_config
from pyramid.response import Response
import json
import jwt
import bcrypt
from datetime import datetime
from ..models import User, UserRole
from ..config import JWT_SECRET


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
            user_data = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role.value if user.role else None
            }
            
            # Include membership data for members
            if user.role == UserRole.MEMBER and user.member:
                user_data['membership_plan'] = user.member.membership_plan
                user_data['membership_expiry'] = user.member.expiry_date.isoformat() if user.member.expiry_date else None
                user_data['membership_status'] = 'Active' if user.member.is_active() else 'Expired'
                user_data['is_active'] = user.member.is_active()
            
            users_data.append(user_data)
        
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


def get_authenticated_user(request):
    """Get authenticated user from JWT token"""
    auth_header = request.headers.get('Authorization', '')
    
    if not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.replace('Bearer ', '')
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user_id = payload.get('user_id')
        
        if not user_id:
            return None
        
        db = request.dbsession
        user = db.query(User).filter(User.id == user_id).first()
        
        return user
    except jwt.InvalidTokenError:
        return None


@view_config(route_name='api_get_profile', renderer='json', request_method='GET')
def get_profile(request):
    """Get user profile"""
    user = get_authenticated_user(request)
    
    if not user:
        request.response.status = 401
        return {
            'status': 'error',
            'message': 'Unauthorized'
        }
    
    return {
        'status': 'success',
        'data': user.to_dict()
    }


@view_config(route_name='api_update_profile', renderer='json', request_method='PUT')
def update_profile(request):
    """Update user profile (name, email, phone, address)"""
    user = get_authenticated_user(request)
    
    if not user:
        request.response.status = 401
        return {
            'status': 'error',
            'message': 'Unauthorized'
        }
    
    try:
        data = request.json_body
        db = request.dbsession
        
        # Update name if provided
        if 'name' in data and data['name']:
            user.name = data['name'].strip()
        
        # Update email if provided and not already taken
        if 'email' in data and data['email']:
            new_email = data['email'].strip().lower()
            if new_email != user.email:
                # Check if email already exists
                existing_user = db.query(User).filter(
                    User.email == new_email,
                    User.id != user.id
                ).first()
                
                if existing_user:
                    request.response.status = 400
                    return {
                        'status': 'error',
                        'message': 'Email already in use'
                    }
                
                user.email = new_email
        
        # Update phone if provided
        if 'phone' in data:
            user.phone = data['phone'].strip() if data['phone'] else None
        
        # Update address if provided
        if 'address' in data:
            user.address = data['address'].strip() if data['address'] else None
        
        # Update avatar_url if provided
        if 'avatar_url' in data:
            user.avatar_url = data['avatar_url'].strip() if data['avatar_url'] else None
        
        user.updated_at = datetime.utcnow()
        db.flush()
        db.commit()
        
        return {
            'status': 'success',
            'message': 'Profile updated successfully',
            'data': user.to_dict()
        }
    
    except Exception as e:
        db.rollback()
        request.response.status = 500
        return {
            'status': 'error',
            'message': str(e)
        }


@view_config(route_name='api_change_password', renderer='json', request_method='PUT')
def change_password(request):
    """Change user password"""
    user = get_authenticated_user(request)
    
    if not user:
        request.response.status = 401
        return {
            'status': 'error',
            'message': 'Unauthorized'
        }
    
    try:
        data = request.json_body
        db = request.dbsession
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            request.response.status = 400
            return {
                'status': 'error',
                'message': 'Current password and new password are required'
            }
        
        # Verify current password
        if not bcrypt.checkpw(current_password.encode('utf-8'), user.password.encode('utf-8')):
            request.response.status = 400
            return {
                'status': 'error',
                'message': 'Current password is incorrect'
            }
        
        # Validate new password
        if len(new_password) < 6:
            request.response.status = 400
            return {
                'status': 'error',
                'message': 'New password must be at least 6 characters'
            }
        
        # Hash and update password
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        user.password = hashed_password.decode('utf-8')
        user.updated_at = datetime.utcnow()
        
        db.flush()
        db.commit()
        
        return {
            'status': 'success',
            'message': 'Password changed successfully'
        }
    
    except Exception as e:
        db.rollback()
        request.response.status = 500
        return {
            'status': 'error',
            'message': str(e)
        }
