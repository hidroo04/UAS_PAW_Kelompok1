"""
Membership views - Manage membership plans and status
"""
from pyramid.view import view_config
from pyramid.response import Response
import json
from datetime import datetime, timedelta


# Mock membership plans
MEMBERSHIP_PLANS = [
    {
        'name': 'Basic',
        'description': 'Access to basic classes',
        'duration_days': 30,
        'price': 50000
    },
    {
        'name': 'Premium',
        'description': 'Access to all classes + personal training',
        'duration_days': 30,
        'price': 100000
    },
    {
        'name': 'VIP',
        'description': 'Unlimited access + priority booking',
        'duration_days': 30,
        'price': 200000
    }
]


# Mock members
mock_members = [
    {
        'id': 1,
        'user_id': 1,
        'membership_plan': 'Premium',
        'expiry_date': '2026-01-15',
        'user': {
            'id': 1,
            'name': 'Jane Member',
            'email': 'jane@example.com',
            'role': 'member'
        }
    }
]


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
            content_type='application/json'
        )


@view_config(route_name='api_my_membership', renderer='json', request_method='GET')
def get_my_membership(request):
    """Get current user's membership status"""
    try:
        # In real app, get user_id from JWT token
        member = next((m for m in mock_members if m['user_id'] == 1), None)
        
        if not member:
            return Response(
                json.dumps({'status': 'error', 'message': 'Membership not found'}),
                status=404,
                content_type='application/json'
            )
        
        # Check if membership is active
        expiry_date = datetime.strptime(member['expiry_date'], '%Y-%m-%d').date()
        is_active = expiry_date >= datetime.now().date()
        
        member_data = {
            **member,
            'is_active': is_active,
            'days_remaining': (expiry_date - datetime.now().date()).days if is_active else 0
        }
        
        return {
            'status': 'success',
            'data': member_data
        }
        
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json'
        )


@view_config(route_name='api_members', renderer='json', request_method='GET')
def get_members(request):
    """Get all members (Admin only)"""
    try:
        return {
            'status': 'success',
            'data': mock_members,
            'count': len(mock_members)
        }
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json'
        )


@view_config(route_name='api_members', renderer='json', request_method='POST')
def create_membership(request):
    """Create or update membership (Admin only)"""
    try:
        data = request.json_body
        
        # Validation
        required_fields = ['user_id', 'membership_plan']
        if not all(field in data for field in required_fields):
            return Response(
                json.dumps({'status': 'error', 'message': 'user_id and membership_plan are required'}),
                status=400,
                content_type='application/json'
            )
        
        user_id = data['user_id']
        plan_name = data['membership_plan']
        
        # Find plan
        plan = next((p for p in MEMBERSHIP_PLANS if p['name'] == plan_name), None)
        
        if not plan:
            return Response(
                json.dumps({'status': 'error', 'message': 'Invalid membership plan'}),
                status=400,
                content_type='application/json'
            )
        
        # Calculate expiry date
        expiry_date = datetime.now().date() + timedelta(days=plan['duration_days'])
        
        # Create new membership (mock)
        new_member = {
            'id': len(mock_members) + 1,
            'user_id': user_id,
            'membership_plan': plan_name,
            'expiry_date': expiry_date.isoformat(),
            'user': {
                'id': user_id,
                'name': 'New Member',
                'email': 'newmember@example.com',
                'role': 'member'
            }
        }
        
        mock_members.append(new_member)
        
        return {
            'status': 'success',
            'message': 'Membership created successfully',
            'data': new_member
        }
        
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json'
        )
