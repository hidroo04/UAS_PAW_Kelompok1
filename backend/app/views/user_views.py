from pyramid.view import view_config
from pyramid.response import Response
import json
import jwt
import bcrypt
from datetime import datetime
from ..models import User, UserRole, Member
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


def require_admin(request):
    """Return authenticated admin user or None if unauthorized"""
    user = get_authenticated_user(request)
    if not user or user.role != UserRole.ADMIN:
        request.response.status = 401
        return None
    return user


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


# --- Admin user management endpoints ---

@view_config(route_name='api_user', renderer='json', request_method='GET')
def get_user_by_id(request):
    """Admin: Get a single user by id including membership details"""
    admin = require_admin(request)
    if not admin:
        return {'status': 'error', 'message': 'Unauthorized'}

    try:
        db = request.dbsession
        user_id = int(request.matchdict['id'])
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            request.response.status = 404
            return {'status': 'error', 'message': 'User not found'}

        data = user.to_dict()
        return {'status': 'success', 'data': data}
    except Exception as e:
        request.response.status = 500
        return {'status': 'error', 'message': str(e)}


@view_config(route_name='api_user', renderer='json', request_method='PUT')
def update_user_admin(request):
    """Admin: Update user fields and membership info"""
    admin = require_admin(request)
    if not admin:
        return {'status': 'error', 'message': 'Unauthorized'}

    try:
        db = request.dbsession
        user_id = int(request.matchdict['id'])
        data = request.json_body or {}

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            request.response.status = 404
            return {'status': 'error', 'message': 'User not found'}

        # Update basic fields
        if 'name' in data and data['name']:
            user.name = data['name'].strip()

        if 'email' in data and data['email']:
            new_email = data['email'].strip().lower()
            if new_email != user.email:
                existing = db.query(User).filter(User.email == new_email, User.id != user.id).first()
                if existing:
                    request.response.status = 400
                    return {'status': 'error', 'message': 'Email already in use'}
                user.email = new_email

        # Update membership if applicable
        membership_plan = data.get('membership_plan')
        expiry_date_str = data.get('expiry_date')
        if membership_plan or expiry_date_str is not None:
            # Ensure user is a member
            if user.role != UserRole.MEMBER:
                user.role = UserRole.MEMBER
            if not user.member:
                user.member = Member(user_id=user.id, membership_plan=membership_plan or 'Basic', expiry_date=datetime.utcnow().date())

            if membership_plan:
                user.member.membership_plan = membership_plan

            if expiry_date_str:
                try:
                    # Accept YYYY-MM-DD
                    user.member.expiry_date = datetime.fromisoformat(expiry_date_str).date()
                except Exception:
                    request.response.status = 400
                    return {'status': 'error', 'message': 'Invalid expiry_date format. Use YYYY-MM-DD'}

        user.updated_at = datetime.utcnow()
        db.flush()
        db.commit()

        return {'status': 'success', 'message': 'User updated successfully', 'data': user.to_dict()}
    except Exception as e:
        db.rollback()
        request.response.status = 500
        return {'status': 'error', 'message': str(e)}


@view_config(route_name='api_user', renderer='json', request_method='DELETE')
def delete_user_admin(request):
    """Admin: Delete user by id (cascade removes member/bookings)"""
    admin = require_admin(request)
    if not admin:
        return {'status': 'error', 'message': 'Unauthorized'}

    try:
        db = request.dbsession
        user_id = int(request.matchdict['id'])
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            request.response.status = 404
            return {'status': 'error', 'message': 'User not found'}

        db.delete(user)
        db.commit()
        return {'status': 'success', 'message': 'User deleted successfully'}
    except Exception as e:
        db.rollback()
        request.response.status = 500
        return {'status': 'error', 'message': str(e)}


# ==================== TRAINER APPROVAL ENDPOINTS ====================

@view_config(route_name='api_pending_trainers', renderer='json', request_method='GET')
def get_pending_trainers(request):
    """Admin: Get all trainers pending approval"""
    admin = require_admin(request)
    if not admin:
        return Response(
            json.dumps({'status': 'error', 'message': 'Admin access required'}),
            status=403,
            content_type='application/json; charset=utf-8'
        )
    
    try:
        db = request.dbsession
        
        # Get filter from query params
        status_filter = request.params.get('status', 'pending')  # pending, approved, rejected, all
        
        query = db.query(User).filter(User.role == UserRole.TRAINER)
        
        if status_filter != 'all':
            query = query.filter(User.approval_status == status_filter)
        
        trainers = query.order_by(User.created_at.desc()).all()
        
        trainers_data = []
        for trainer in trainers:
            trainers_data.append({
                'id': trainer.id,
                'name': trainer.name,
                'email': trainer.email,
                'phone': trainer.phone,
                'is_approved': trainer.is_approved,
                'approval_status': trainer.approval_status,
                'rejection_reason': trainer.rejection_reason,
                'approved_at': trainer.approved_at.isoformat() if trainer.approved_at else None,
                'created_at': trainer.created_at.isoformat() if trainer.created_at else None
            })
        
        # Get counts
        pending_count = db.query(User).filter(
            User.role == UserRole.TRAINER,
            User.approval_status == 'pending'
        ).count()
        
        approved_count = db.query(User).filter(
            User.role == UserRole.TRAINER,
            User.approval_status == 'approved'
        ).count()
        
        rejected_count = db.query(User).filter(
            User.role == UserRole.TRAINER,
            User.approval_status == 'rejected'
        ).count()
        
        return {
            'status': 'success',
            'data': trainers_data,
            'counts': {
                'pending': pending_count,
                'approved': approved_count,
                'rejected': rejected_count,
                'total': pending_count + approved_count + rejected_count
            }
        }
        
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )


@view_config(route_name='api_approve_trainer', renderer='json', request_method='POST')
def approve_trainer(request):
    """Admin: Approve a pending trainer"""
    admin = require_admin(request)
    if not admin:
        return Response(
            json.dumps({'status': 'error', 'message': 'Admin access required'}),
            status=403,
            content_type='application/json; charset=utf-8'
        )
    
    try:
        db = request.dbsession
        trainer_id = int(request.matchdict['id'])
        
        trainer = db.query(User).filter(
            User.id == trainer_id,
            User.role == UserRole.TRAINER
        ).first()
        
        if not trainer:
            return Response(
                json.dumps({'status': 'error', 'message': 'Trainer not found'}),
                status=404,
                content_type='application/json; charset=utf-8'
            )
        
        if trainer.approval_status == 'approved':
            return Response(
                json.dumps({'status': 'error', 'message': 'Trainer is already approved'}),
                status=400,
                content_type='application/json; charset=utf-8'
            )
        
        # Approve trainer
        trainer.is_approved = True
        trainer.approval_status = 'approved'
        trainer.approved_at = datetime.utcnow()
        trainer.approved_by = admin.id
        trainer.rejection_reason = None
        
        db.commit()
        
        return {
            'status': 'success',
            'message': f'Trainer {trainer.name} has been approved successfully!',
            'data': {
                'id': trainer.id,
                'name': trainer.name,
                'email': trainer.email,
                'approval_status': trainer.approval_status,
                'approved_at': trainer.approved_at.isoformat()
            }
        }
        
    except Exception as e:
        db.rollback()
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )


@view_config(route_name='api_reject_trainer', renderer='json', request_method='POST')
def reject_trainer(request):
    """Admin: Reject a pending trainer"""
    admin = require_admin(request)
    if not admin:
        return Response(
            json.dumps({'status': 'error', 'message': 'Admin access required'}),
            status=403,
            content_type='application/json; charset=utf-8'
        )
    
    try:
        db = request.dbsession
        trainer_id = int(request.matchdict['id'])
        data = request.json_body
        reason = data.get('reason', 'Application does not meet our requirements')
        
        trainer = db.query(User).filter(
            User.id == trainer_id,
            User.role == UserRole.TRAINER
        ).first()
        
        if not trainer:
            return Response(
                json.dumps({'status': 'error', 'message': 'Trainer not found'}),
                status=404,
                content_type='application/json; charset=utf-8'
            )
        
        if trainer.approval_status == 'rejected':
            return Response(
                json.dumps({'status': 'error', 'message': 'Trainer is already rejected'}),
                status=400,
                content_type='application/json; charset=utf-8'
            )
        
        # Reject trainer
        trainer.is_approved = False
        trainer.approval_status = 'rejected'
        trainer.rejection_reason = reason
        
        db.commit()
        
        return {
            'status': 'success',
            'message': f'Trainer {trainer.name} has been rejected.',
            'data': {
                'id': trainer.id,
                'name': trainer.name,
                'email': trainer.email,
                'approval_status': trainer.approval_status,
                'rejection_reason': trainer.rejection_reason
            }
        }
        
    except Exception as e:
        db.rollback()
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )

