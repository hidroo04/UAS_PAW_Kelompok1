"""
Payment Views - Payment Gateway untuk Membership
Simulasi payment gateway dengan berbagai metode pembayaran
"""
from pyramid.view import view_config
from pyramid.response import Response
import json
from datetime import datetime, timedelta
import uuid
import random
import string

from ..models import Member, Payment, PaymentStatus, PaymentMethod
from sqlalchemy.orm import joinedload
from ..utils.auth import get_token_from_header, decode_jwt_token
import jwt


# Payment method configurations
PAYMENT_METHODS = [
    {
        'id': 'bank_transfer',
        'name': 'Bank Transfer',
        'description': 'Transfer via Virtual Account',
        'icon': 'bank',
        'banks': [
            {'code': 'bca', 'name': 'BCA', 'admin_fee': 4000},
            {'code': 'bni', 'name': 'BNI', 'admin_fee': 4000},
            {'code': 'bri', 'name': 'BRI', 'admin_fee': 4000},
            {'code': 'mandiri', 'name': 'Mandiri', 'admin_fee': 4000}
        ]
    },
    {
        'id': 'e_wallet',
        'name': 'E-Wallet',
        'description': 'Bayar dengan dompet digital',
        'icon': 'wallet',
        'wallets': [
            {'code': 'gopay', 'name': 'GoPay', 'admin_fee': 0},
            {'code': 'ovo', 'name': 'OVO', 'admin_fee': 0},
            {'code': 'dana', 'name': 'DANA', 'admin_fee': 0},
            {'code': 'shopeepay', 'name': 'ShopeePay', 'admin_fee': 0}
        ]
    },
    {
        'id': 'qris',
        'name': 'QRIS',
        'description': 'Scan QR code untuk bayar',
        'icon': 'qr',
        'admin_fee': 0
    },
    {
        'id': 'credit_card',
        'name': 'Credit Card',
        'description': 'Visa, Mastercard, JCB',
        'icon': 'credit-card',
        'admin_fee': 0
    }
]

# Membership plans (copy from membership_views)
MEMBERSHIP_PLANS = {
    1: {'id': 1, 'name': 'Basic', 'price': 150000, 'duration_days': 30},
    2: {'id': 2, 'name': 'Premium', 'price': 300000, 'duration_days': 30},
    3: {'id': 3, 'name': 'VIP', 'price': 500000, 'duration_days': 30}
}


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


def generate_order_id():
    """Generate unique order ID"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"FZ-{timestamp}-{random_str}"


def generate_va_number(bank_code):
    """Generate Virtual Account number"""
    prefix = {
        'bca': '1234',
        'bni': '8810',
        'bri': '0023',
        'mandiri': '8900'
    }
    return f"{prefix.get(bank_code, '9999')}{random.randint(10000000, 99999999)}"


@view_config(route_name='api_payment_methods', renderer='json', request_method='GET')
def get_payment_methods(request):
    """Get available payment methods"""
    return {
        'status': 'success',
        'data': PAYMENT_METHODS
    }


@view_config(route_name='api_payment_all', renderer='json', request_method='GET')
def get_all_payments(request):
    """Get all payments (Admin only)"""
    try:
        db = request.dbsession
        
        # Get all payments with member info
        payments = db.query(Payment).options(
            joinedload(Payment.member).joinedload(Member.user)
        ).order_by(Payment.created_at.desc()).all()
        
        result = []
        for payment in payments:
            payment_dict = payment.to_dict()
            if payment.member:
                payment_dict['member'] = {
                    'id': payment.member.id,
                    'user': {
                        'id': payment.member.user.id,
                        'name': payment.member.user.name,
                        'email': payment.member.user.email
                    } if payment.member.user else None
                }
            result.append(payment_dict)
        
        return {
            'status': 'success',
            'data': result,
            'count': len(result)
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )


@view_config(route_name='api_payment_create', renderer='json', request_method='POST')
def create_payment(request):
    """Create a new payment for membership subscription"""
    try:
        db = request.dbsession
        data = request.json_body
        
        # Get user_id from token
        user_id = get_authenticated_user_id(request)
        if not user_id:
            return Response(
                json.dumps({'status': 'error', 'message': 'Authentication required'}),
                status=401,
                content_type='application/json; charset=utf-8'
            )
        
        # Validate required fields
        plan_id = data.get('plan_id')
        payment_method = data.get('payment_method')
        payment_detail = data.get('payment_detail')  # bank code, wallet code, etc
        
        if not plan_id or not payment_method:
            return Response(
                json.dumps({'status': 'error', 'message': 'plan_id and payment_method are required'}),
                status=400,
                content_type='application/json; charset=utf-8'
            )
        
        # Get plan info
        plan = MEMBERSHIP_PLANS.get(plan_id)
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
                json.dumps({'status': 'error', 'message': 'Member not found'}),
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
        
        # Check for pending payment
        pending_payment = db.query(Payment).filter(
            Payment.member_id == member.id,
            Payment.status == 'pending'  # Use string instead of enum
        ).first()
        
        if pending_payment:
            # Return existing pending payment
            return {
                'status': 'success',
                'message': 'You have a pending payment',
                'data': pending_payment.to_dict()
            }
        
        # Calculate amount with admin fee
        amount = plan['price']
        admin_fee = 0
        
        if payment_method == 'bank_transfer' and payment_detail:
            for bank in PAYMENT_METHODS[0]['banks']:
                if bank['code'] == payment_detail:
                    admin_fee = bank['admin_fee']
                    break
        
        total_amount = amount + admin_fee
        
        # Generate order ID and VA number
        order_id = generate_order_id()
        va_number = None
        
        if payment_method == 'bank_transfer' and payment_detail:
            va_number = generate_va_number(payment_detail)
        
        # Create payment - using string values for status and method
        payment = Payment(
            member_id=member.id,
            order_id=order_id,
            amount=total_amount,
            payment_method=payment_method,  # Store as string
            status='pending',  # Store as string
            membership_plan=plan['name'],
            duration_days=plan['duration_days'],
            va_number=va_number,
            expired_at=datetime.utcnow() + timedelta(hours=24)  # 24 hour expiry
        )
        
        db.add(payment)
        db.commit()
        
        # Prepare response data
        response_data = payment.to_dict()
        response_data['plan'] = plan
        response_data['admin_fee'] = admin_fee
        response_data['subtotal'] = amount
        response_data['total'] = total_amount
        
        # Add payment instructions
        if payment_method == 'bank_transfer':
            response_data['instructions'] = [
                f"Transfer ke Virtual Account: {va_number}",
                f"Bank: {payment_detail.upper() if payment_detail else 'N/A'}",
                f"Jumlah: Rp {total_amount:,.0f}",
                "Pembayaran akan diverifikasi otomatis dalam 5 menit",
                "Batas waktu pembayaran: 24 jam"
            ]
        elif payment_method == 'e_wallet':
            response_data['instructions'] = [
                f"Buka aplikasi {payment_detail.title() if payment_detail else 'E-Wallet'} Anda",
                "Scan QR Code atau masukkan nomor transaksi",
                f"Konfirmasi pembayaran sebesar Rp {total_amount:,.0f}",
                "Pembayaran akan diverifikasi otomatis"
            ]
        elif payment_method == 'qris':
            response_data['instructions'] = [
                "Buka aplikasi e-wallet atau mobile banking Anda",
                "Pilih menu Scan QR / QRIS",
                "Scan QR Code yang ditampilkan",
                f"Konfirmasi pembayaran sebesar Rp {total_amount:,.0f}"
            ]
            response_data['qr_code'] = f"data:image/png;base64,QRIS_PLACEHOLDER_{order_id}"
        
        return {
            'status': 'success',
            'message': 'Payment created successfully',
            'data': response_data
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )


@view_config(route_name='api_payment_status', renderer='json', request_method='GET')
def get_payment_status(request):
    """Get payment status by order_id"""
    try:
        db = request.dbsession
        order_id = request.matchdict.get('order_id')
        
        # Get user_id from token
        user_id = get_authenticated_user_id(request)
        if not user_id:
            return Response(
                json.dumps({'status': 'error', 'message': 'Authentication required'}),
                status=401,
                content_type='application/json; charset=utf-8'
            )
        
        # Find payment
        payment = db.query(Payment).options(
            joinedload(Payment.member)
        ).filter(Payment.order_id == order_id).first()
        
        if not payment:
            return Response(
                json.dumps({'status': 'error', 'message': 'Payment not found'}),
                status=404,
                content_type='application/json; charset=utf-8'
            )
        
        # Check if expired
        if payment.status == 'pending' and payment.expired_at:
            if datetime.utcnow() > payment.expired_at:
                payment.status = 'expired'
                db.commit()
        
        return {
            'status': 'success',
            'data': payment.to_dict()
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )


@view_config(route_name='api_payment_simulate', renderer='json', request_method='POST')
def simulate_payment(request):
    """
    Simulate payment completion (for testing)
    In production, this would be replaced by actual payment gateway callback
    """
    try:
        db = request.dbsession
        order_id = request.matchdict.get('order_id')
        data = request.json_body
        
        # Get action: success or failed
        action = data.get('action', 'success')
        
        # Find payment
        payment = db.query(Payment).options(
            joinedload(Payment.member)
        ).filter(Payment.order_id == order_id).first()
        
        if not payment:
            return Response(
                json.dumps({'status': 'error', 'message': 'Payment not found'}),
                status=404,
                content_type='application/json; charset=utf-8'
            )
        
        if payment.status != 'pending':
            return Response(
                json.dumps({'status': 'error', 'message': f'Payment already {payment.status}'}),
                status=400,
                content_type='application/json; charset=utf-8'
            )
        
        if action == 'success':
            # Update payment status
            payment.status = 'success'
            payment.paid_at = datetime.utcnow()
            payment.transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
            
            # Activate membership
            member = payment.member
            member.membership_plan = payment.membership_plan
            member.expiry_date = (datetime.utcnow() + timedelta(days=payment.duration_days)).date()
            
            db.commit()
            
            return {
                'status': 'success',
                'message': 'Payment successful! Membership activated.',
                'data': {
                    'payment': payment.to_dict(),
                    'membership': {
                        'plan': member.membership_plan,
                        'expiry_date': member.expiry_date.isoformat(),
                        'is_active': member.is_active()
                    }
                }
            }
        else:
            # Payment failed
            payment.status = 'failed'
            db.commit()
            
            return {
                'status': 'success',
                'message': 'Payment marked as failed',
                'data': payment.to_dict()
            }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )


@view_config(route_name='api_payment_callback', renderer='json', request_method='POST')
def payment_callback(request):
    """
    Payment gateway callback handler
    This would be called by the actual payment gateway (Midtrans, Xendit, etc.)
    """
    try:
        db = request.dbsession
        data = request.json_body
        
        order_id = data.get('order_id')
        transaction_status = data.get('transaction_status')
        transaction_id = data.get('transaction_id')
        
        if not order_id:
            return Response(
                json.dumps({'status': 'error', 'message': 'order_id is required'}),
                status=400,
                content_type='application/json; charset=utf-8'
            )
        
        # Find payment
        payment = db.query(Payment).options(
            joinedload(Payment.member)
        ).filter(Payment.order_id == order_id).first()
        
        if not payment:
            return Response(
                json.dumps({'status': 'error', 'message': 'Payment not found'}),
                status=404,
                content_type='application/json; charset=utf-8'
            )
        
        # Update payment based on status
        if transaction_status in ['capture', 'settlement', 'success']:
            payment.status = 'success'
            payment.paid_at = datetime.utcnow()
            payment.transaction_id = transaction_id
            
            # Activate membership
            member = payment.member
            member.membership_plan = payment.membership_plan
            member.expiry_date = (datetime.utcnow() + timedelta(days=payment.duration_days)).date()
            
        elif transaction_status in ['deny', 'cancel', 'expire', 'failed']:
            if transaction_status == 'expire':
                payment.status = 'expired'
            else:
                payment.status = 'failed'
                
        elif transaction_status == 'pending':
            payment.status = 'processing'
        
        db.commit()
        
        return {
            'status': 'success',
            'message': 'Callback processed',
            'data': payment.to_dict()
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )


@view_config(route_name='api_payment_history', renderer='json', request_method='GET')
def get_payment_history(request):
    """Get payment history for current user"""
    try:
        db = request.dbsession
        
        # Get user_id from token
        user_id = get_authenticated_user_id(request)
        if not user_id:
            return Response(
                json.dumps({'status': 'error', 'message': 'Authentication required'}),
                status=401,
                content_type='application/json; charset=utf-8'
            )
        
        # Find member
        member = db.query(Member).filter(Member.user_id == user_id).first()
        if not member:
            return Response(
                json.dumps({'status': 'error', 'message': 'Member not found'}),
                status=404,
                content_type='application/json; charset=utf-8'
            )
        
        # Get payments
        payments = db.query(Payment).filter(
            Payment.member_id == member.id
        ).order_by(Payment.created_at.desc()).all()
        
        return {
            'status': 'success',
            'data': [p.to_dict() for p in payments],
            'count': len(payments)
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )


@view_config(route_name='api_payment_report', renderer='json', request_method='GET')
def get_payment_report(request):
    """Get payment report with statistics for admin"""
    try:
        from sqlalchemy import func, cast, Date
        from ..models import User, UserRole
        
        db = request.dbsession
        
        # Check admin authentication
        user_id = get_authenticated_user_id(request)
        if not user_id:
            return Response(
                json.dumps({'status': 'error', 'message': 'Authentication required'}),
                status=401,
                content_type='application/json; charset=utf-8'
            )
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user or user.role != UserRole.ADMIN:
            return Response(
                json.dumps({'status': 'error', 'message': 'Admin access required'}),
                status=403,
                content_type='application/json; charset=utf-8'
            )
        
        # Get query parameters
        start_date = request.params.get('start_date')
        end_date = request.params.get('end_date')
        status_filter = request.params.get('status')
        plan_filter = request.params.get('plan')
        
        # Base query
        query = db.query(Payment).options(
            joinedload(Payment.member).joinedload(Member.user)
        )
        
        # Apply filters
        if start_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d')
                query = query.filter(Payment.created_at >= start)
            except:
                pass
        
        if end_date:
            try:
                end = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
                query = query.filter(Payment.created_at < end)
            except:
                pass
        
        if status_filter and status_filter != 'all':
            query = query.filter(Payment.status == status_filter)
        
        if plan_filter and plan_filter != 'all':
            query = query.filter(Payment.membership_plan == plan_filter)
        
        # Get payments
        payments = query.order_by(Payment.created_at.desc()).all()
        
        # Calculate statistics
        total_payments = len(payments)
        total_amount = sum(float(p.amount) for p in payments)
        successful_amount = sum(float(p.amount) for p in payments if p.status == 'success')
        
        # Count by status
        status_counts = {
            'pending': 0,
            'processing': 0,
            'success': 0,
            'failed': 0,
            'expired': 0,
            'refunded': 0
        }
        for p in payments:
            if p.status:
                status_counts[p.status] = status_counts.get(p.status, 0) + 1
        
        # Count by plan
        plan_counts = {}
        plan_revenue = {}
        for p in payments:
            plan = p.membership_plan
            plan_counts[plan] = plan_counts.get(plan, 0) + 1
            if p.status == 'success':
                plan_revenue[plan] = plan_revenue.get(plan, 0) + float(p.amount)
        
        # Count by payment method
        method_counts = {}
        for p in payments:
            if p.payment_method:
                method = p.payment_method
                method_counts[method] = method_counts.get(method, 0) + 1
        
        # Daily revenue (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        daily_revenue = db.query(
            func.date(Payment.paid_at).label('date'),
            func.sum(Payment.amount).label('total')
        ).filter(
            Payment.status == 'success',
            Payment.paid_at >= thirty_days_ago
        ).group_by(func.date(Payment.paid_at)).order_by(func.date(Payment.paid_at)).all()
        
        daily_revenue_data = [
            {'date': str(row.date), 'total': float(row.total)} 
            for row in daily_revenue if row.date
        ]
        
        # Build payment list with member info
        payment_list = []
        for payment in payments:
            payment_dict = payment.to_dict()
            if payment.member:
                payment_dict['member'] = {
                    'id': payment.member.id,
                    'name': payment.member.user.name if payment.member.user else 'Unknown',
                    'email': payment.member.user.email if payment.member.user else 'Unknown'
                }
            payment_list.append(payment_dict)
        
        return {
            'status': 'success',
            'data': {
                'payments': payment_list,
                'statistics': {
                    'total_payments': total_payments,
                    'total_amount': total_amount,
                    'successful_amount': successful_amount,
                    'status_counts': status_counts,
                    'plan_counts': plan_counts,
                    'plan_revenue': plan_revenue,
                    'method_counts': method_counts,
                    'daily_revenue': daily_revenue_data
                }
            }
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )
