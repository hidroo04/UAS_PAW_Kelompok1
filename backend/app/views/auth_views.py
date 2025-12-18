"""
Authentication views - Login, Register, Logout
"""
from pyramid.view import view_config
from pyramid.response import Response
import hashlib
import json
from datetime import datetime, timedelta, date
import jwt
from sqlalchemy.orm import Session
from ..models import User, Member, UserRole
from ..config import config
from ..utils.auth import create_jwt_token as create_token_util, hash_password

# Use config from utils/auth for consistency
JWT_SECRET = config.JWT_SECRET_KEY
JWT_ALGORITHM = config.JWT_ALGORITHM
JWT_EXP_DELTA_SECONDS = config.JWT_EXPIRATION_HOURS * 3600

# Use the unified create_jwt_token from utils
create_jwt_token = create_token_util


@view_config(route_name='auth_register', renderer='json', request_method='POST')
def register(request):
    """Register new user"""
    try:
        data = request.json_body
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone')
        role = data.get('role', 'MEMBER')  # default: MEMBER
        
        # Validation
        if not all([name, email, password]):
            return Response(
                json.dumps({'status': 'error', 'message': 'Name, email, and password are required'}),
                status=400,
                content_type='application/json; charset=utf-8'
            )
        
        # Get database session
        db: Session = request.dbsession
        
        # Check if email already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            return Response(
                json.dumps({'status': 'error', 'message': 'Email already registered'}),
                status=400,
                content_type='application/json; charset=utf-8'
            )
        
        # Hash password
        hashed_password = hash_password(password)
        
        # Determine user role and approval status
        user_role = UserRole[role.upper()] if role.upper() in ['ADMIN', 'TRAINER', 'MEMBER'] else UserRole.MEMBER
        
        # Trainers need admin approval
        is_approved = True
        approval_status = 'approved'
        if user_role == UserRole.TRAINER:
            is_approved = False
            approval_status = 'pending'
        
        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            phone=phone,
            role=user_role,
            is_approved=is_approved,
            approval_status=approval_status
        )
        db.add(new_user)
        db.flush()  # Get user ID
        
        # If role is MEMBER, create member profile WITHOUT active membership
        # Member must choose and pay for membership separately
        if user_role == UserRole.MEMBER:
            member_profile = Member(
                user_id=new_user.id,
                membership_plan=None,  # No membership plan by default
                expiry_date=None  # No expiry date until they subscribe
            )
            db.add(member_profile)
        
        db.commit()
        
        # Prepare user data
        user_data = {
            'id': new_user.id,
            'name': new_user.name,
            'email': new_user.email,
            'role': new_user.role.value,
            'is_approved': new_user.is_approved,
            'approval_status': new_user.approval_status
        }
        
        # For trainers pending approval, don't return token
        if user_role == UserRole.TRAINER and not is_approved:
            return {
                'status': 'success',
                'message': 'Trainer registration submitted! Please wait for admin approval before you can login.',
                'data': user_data,
                'pending_approval': True
            }
        
        # Create JWT token for approved users
        token = create_jwt_token(new_user.id, new_user.email, new_user.role.value)
        
        return {
            'status': 'success',
            'message': 'User registered successfully',
            'data': user_data,
            'token': token
        }
        
    except Exception as e:
        db.rollback()
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )


@view_config(route_name='auth_login', renderer='json', request_method='POST')
def login(request):
    """Login user"""
    try:
        data = request.json_body
        email = data.get('email')
        password = data.get('password')
        
        # Validation
        if not all([email, password]):
            return Response(
                json.dumps({'status': 'error', 'message': 'Email and password are required'}),
                status=400,
                content_type='application/json; charset=utf-8'
            )
        
        # Hash password untuk comparison
        hashed_password = hash_password(password)
        
        # Query user from database
        db: Session = request.dbsession
        user = db.query(User).filter(User.email == email).first()
        
        # Check if user exists and password matches
        if not user or user.password != hashed_password:
            return Response(
                json.dumps({'status': 'error', 'message': 'Invalid email or password'}),
                status=401,
                content_type='application/json; charset=utf-8'
            )
        
        # Check if trainer is approved
        if user.role == UserRole.TRAINER:
            if user.approval_status == 'pending':
                return Response(
                    json.dumps({
                        'status': 'error', 
                        'message': 'Your trainer account is pending approval. Please wait for admin to review your application.',
                        'approval_status': 'pending'
                    }),
                    status=403,
                    content_type='application/json; charset=utf-8'
                )
            elif user.approval_status == 'rejected':
                return Response(
                    json.dumps({
                        'status': 'error', 
                        'message': f'Your trainer application was rejected. Reason: {user.rejection_reason or "No reason provided"}',
                        'approval_status': 'rejected'
                    }),
                    status=403,
                    content_type='application/json; charset=utf-8'
                )
        
        # Prepare user data
        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role.value,
            'is_approved': user.is_approved,
            'approval_status': user.approval_status
        }
        
        # Create JWT token
        token = create_jwt_token(user.id, user.email, user.role.value)
        
        return {
            'status': 'success',
            'message': 'Login successful',
            'data': user_data,
            'token': token
        }
        
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )


@view_config(route_name='auth_logout', renderer='json', request_method='POST')
def logout(request):
    """Logout user (client-side akan hapus token)"""
    return {
        'status': 'success',
        'message': 'Logout successful'
    }


@view_config(route_name='auth_me', renderer='json', request_method='GET')
def get_current_user(request):
    """Get current authenticated user info"""
    try:
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return Response(
                json.dumps({'status': 'error', 'message': 'Invalid authorization header'}),
                status=401,
                content_type='application/json; charset=utf-8'
            )
        
        token = auth_header.replace('Bearer ', '')
        
        # Decode JWT token
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        
        # Query user from database
        db: Session = request.dbsession
        user = db.query(User).filter(User.id == payload['user_id']).first()
        
        if not user:
            return Response(
                json.dumps({'status': 'error', 'message': 'User not found'}),
                status=404,
                content_type='application/json; charset=utf-8'
            )
        
        # Prepare user data
        user_data = {
            'id': user.id,
            'email': user.email,
            'role': user.role.value,
            'name': user.name
        }
        
        # Add membership info if user is a member
        if user.role.value == 'member' and user.member:
            user_data['membership_plan'] = user.member.membership_plan
            user_data['membership_status'] = 'active' if user.member.is_active() else 'expired'
            if user.member.expiry_date:
                user_data['membership_expiry'] = user.member.expiry_date.isoformat()
        
        return {
            'status': 'success',
            'data': user_data
        }
        
    except jwt.ExpiredSignatureError:
        return Response(
            json.dumps({'status': 'error', 'message': 'Token expired'}),
            status=401,
            content_type='application/json; charset=utf-8'
        )
    except jwt.InvalidTokenError:
        return Response(
            json.dumps({'status': 'error', 'message': 'Invalid token'}),
            status=401,
            content_type='application/json; charset=utf-8'
        )
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json'
        )
