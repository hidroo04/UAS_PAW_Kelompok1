"""
Membership views - Manage membership plans and status
"""
from pyramid.view import view_config
from pyramid.response import Response
import json
from datetime import datetime, timedelta, date
from ..models import Member, User, Booking
from sqlalchemy.orm import joinedload
from ..utils.auth import get_token_from_header, decode_jwt_token
import jwt


# Membership plans dengan ID untuk referensi
# class_limit: -1 = unlimited, angka positif = max kelas per bulan
MEMBERSHIP_PLANS = [
    {
        'id': 1,
        'name': 'Basic',
        'description': 'Akses ke 5 kelas per bulan dan fasilitas gym standar',
        'duration_days': 30,
        'price': 150000,
        'features': [
            'Akses gym equipment',
            'Max 5 kelas per bulan',
            'Locker room access',
            'Free water dispenser'
        ],
        'class_limit': 5,
        'is_popular': False
    },
    {
        'id': 2,
        'name': 'Premium',
        'description': 'Akses ke 10 kelas per bulan dengan benefit tambahan',
        'duration_days': 30,
        'price': 300000,
        'features': [
            'Akses gym equipment',
            'Max 10 kelas per bulan',
            'Locker room + towel',
            'Personal trainer consultation',
            'Nutrition guide'
        ],
        'class_limit': 10,
        'is_popular': True
    },
    {
        'id': 3,
        'name': 'VIP',
        'description': 'Pengalaman fitness terbaik dengan unlimited kelas',
        'duration_days': 30,
        'price': 500000,
        'features': [
            'Semua benefit Premium',
            'Unlimited kelas',
            'Priority booking',
            'Private locker',
            '2x Personal training session',
            'Spa & sauna access',
            'Free protein shake'
        ],
        'class_limit': -1,
        'is_popular': False
    }
]


def get_authenticated_user_id(request):
    """Extract user_id from JWT token"""
    token = get_token_from_header(request)
    if not token:
        return None
    
    try:
        payload = decode_jwt_token(token)
        return payload.get('user_id')
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


@view_config(route_name='api_membership_plans', renderer='json', request_method='GET')
def get_membership_plans(request):
    """Get all available membership plans"""
    try:
        return {
            'status': 'success',
            'data': MEMBERSHIP_PLANS
        }
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )


@view_config(route_name='api_my_membership', renderer='json', request_method='GET')
def get_my_membership(request):
    """Get current user's membership status from database"""
    try:
        db = request.dbsession
        
        # Get user_id from JWT token
        user_id = get_authenticated_user_id(request)
        if not user_id:
            return Response(
                json.dumps({'status': 'error', 'message': 'Authentication required'}),
                status=401,
                content_type='application/json; charset=utf-8'
            )
        
        # Find member by user_id
        member = db.query(Member).options(joinedload(Member.user)).filter(Member.user_id == user_id).first()
        
        if not member:
            return Response(
                json.dumps({'status': 'error', 'message': 'Member profile not found'}),
                status=404,
                content_type='application/json; charset=utf-8'
            )
        
        # Check if membership is expired and clear it
        if member.expiry_date and member.expiry_date < datetime.now().date():
            # Membership expired - clear it
            member.membership_plan = None
            member.expiry_date = None
            db.commit()
        
        member_data = {
            'id': member.id,
            'user_id': member.user_id,
            'membership_plan': member.membership_plan,
            'expiry_date': member.expiry_date.isoformat() if member.expiry_date else None,
            'is_active': member.is_active(),
            'days_remaining': member.days_remaining(),
            'user': {
                'id': member.user.id,
                'name': member.user.name,
                'email': member.user.email,
                'role': member.user.role.value if member.user.role else 'member'
            } if member.user else None
        }
        
        # Tambahkan info plan dan class usage jika ada membership aktif
        if member.membership_plan:
            plan = next((p for p in MEMBERSHIP_PLANS if p['name'] == member.membership_plan), None)
            if plan:
                member_data['plan_details'] = plan
                member_data['class_limit'] = plan['class_limit']
                
                # Hitung booking bulan ini
                today = date.today()
                first_day_of_month = today.replace(day=1)
                
                monthly_bookings = db.query(Booking).filter(
                    Booking.member_id == member.id,
                    Booking.booking_date >= first_day_of_month
                ).count()
                
                member_data['monthly_bookings'] = monthly_bookings
                
                if plan['class_limit'] == -1:
                    member_data['remaining_classes'] = -1  # unlimited
                    member_data['class_limit_text'] = 'Unlimited'
                else:
                    remaining = max(0, plan['class_limit'] - monthly_bookings)
                    member_data['remaining_classes'] = remaining
                    member_data['class_limit_text'] = f"{monthly_bookings}/{plan['class_limit']} kelas"
        
        return {
            'status': 'success',
            'data': member_data
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )


@view_config(route_name='api_membership_subscribe', renderer='json', request_method='POST')
def subscribe_membership(request):
    """Subscribe to a membership plan"""
    try:
        db = request.dbsession
        data = request.json_body
        
        # Get user_id from JWT token
        user_id = get_authenticated_user_id(request)
        if not user_id:
            return Response(
                json.dumps({'status': 'error', 'message': 'Authentication required'}),
                status=401,
                content_type='application/json; charset=utf-8'
            )
        
        # Validate plan_id
        plan_id = data.get('plan_id')
        if not plan_id:
            return Response(
                json.dumps({'status': 'error', 'message': 'plan_id is required'}),
                status=400,
                content_type='application/json; charset=utf-8'
            )
        
        # Find plan
        plan = next((p for p in MEMBERSHIP_PLANS if p['id'] == plan_id), None)
        if not plan:
            return Response(
                json.dumps({'status': 'error', 'message': 'Invalid membership plan'}),
                status=400,
                content_type='application/json; charset=utf-8'
            )
        
        # Find member
        member = db.query(Member).filter(Member.user_id == user_id).first()
        if not member:
            return Response(
                json.dumps({'status': 'error', 'message': 'Member profile not found'}),
                status=404,
                content_type='application/json; charset=utf-8'
            )
        
        # Check if already has active membership
        if member.is_active():
            return Response(
                json.dumps({
                    'status': 'error', 
                    'message': f'You already have an active {member.membership_plan} membership until {member.expiry_date.isoformat()}'
                }),
                status=400,
                content_type='application/json; charset=utf-8'
            )
        
        # Subscribe to plan
        now = datetime.now()
        member.membership_plan = plan['name']
        member.expiry_date = (now + timedelta(days=plan['duration_days'])).date()
        
        db.commit()
        
        return {
            'status': 'success',
            'message': f'Successfully subscribed to {plan["name"]} membership!',
            'data': {
                'membership_plan': member.membership_plan,
                'expiry_date': member.expiry_date.isoformat(),
                'days_remaining': member.days_remaining()
            }
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        db.rollback()
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )


@view_config(route_name='api_members', renderer='json', request_method='GET')
def get_members(request):
    """Get all members (Admin only)"""
    try:
        db = request.dbsession
        members = db.query(Member).options(joinedload(Member.user)).all()
        
        # Auto-expire memberships
        now = datetime.now().date()
        for member in members:
            if member.expiry_date and member.expiry_date < now and member.membership_plan:
                member.membership_plan = None
                member.expiry_date = None
        db.commit()
        
        members_data = []
        for member in members:
            member_data = {
                'id': member.id,
                'user_id': member.user_id,
                'name': member.user.name if member.user else 'Unknown',
                'email': member.user.email if member.user else 'Unknown',
                'membership_plan': member.membership_plan or 'No Plan',
                'expiry_date': member.expiry_date.strftime('%Y-%m-%d') if member.expiry_date else None,
                'is_active': member.is_active(),
                'days_remaining': member.days_remaining()
            }
            members_data.append(member_data)
        
        return {
            'status': 'success',
            'data': members_data,
            'count': len(members_data)
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )


@view_config(route_name='api_members', renderer='json', request_method='POST')
def create_membership(request):
    """Create or update membership (Admin only)"""
    try:
        db = request.dbsession
        data = request.json_body
        
        # Validation
        required_fields = ['user_id', 'membership_plan']
        if not all(field in data for field in required_fields):
            return Response(
                json.dumps({'status': 'error', 'message': 'user_id and membership_plan are required'}),
                status=400,
                content_type='application/json; charset=utf-8'
            )
        
        user_id = data['user_id']
        plan_name = data['membership_plan']
        
        # Find plan
        plan = next((p for p in MEMBERSHIP_PLANS if p['name'] == plan_name), None)
        
        if not plan:
            return Response(
                json.dumps({'status': 'error', 'message': 'Invalid membership plan'}),
                status=400,
                content_type='application/json; charset=utf-8'
            )
        
        # Find or create member
        member = db.query(Member).filter(Member.user_id == user_id).first()
        
        if member:
            # Update existing member
            member.membership_plan = plan_name
            member.expiry_date = (datetime.now() + timedelta(days=plan['duration_days'])).date()
        else:
            # Create new member
            member = Member(
                user_id=user_id,
                membership_plan=plan_name,
                expiry_date=(datetime.now() + timedelta(days=plan['duration_days'])).date()
            )
            db.add(member)
        
        db.commit()
        
        return {
            'status': 'success',
            'message': 'Membership created/updated successfully',
            'data': member.to_dict()
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        db.rollback()
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )
