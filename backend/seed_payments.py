"""
Seed sample payment data for testing
"""
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import random
import string

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost/gym_booking_db')

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Check if we have members
from app.models import Member, Payment, PaymentStatus, PaymentMethod

members = session.query(Member).all()
if not members:
    print("No members found. Please seed members first.")
    exit()

print(f"Found {len(members)} members")

# Generate sample payments
plans = [
    {'name': 'Basic', 'price': 150000, 'duration': 30},
    {'name': 'Premium', 'price': 300000, 'duration': 30},
    {'name': 'VIP', 'price': 500000, 'duration': 30}
]

statuses = ['success', 'success', 'success', 'pending', 'failed', 'expired']
methods = ['bank_transfer', 'e_wallet', 'qris', 'credit_card']

# Create payments
payments_to_add = []
for i in range(15):  # Create 15 sample payments
    member = random.choice(members)
    plan = random.choice(plans)
    status = random.choice(statuses)
    method = random.choice(methods)
    
    # Generate order ID
    timestamp = (datetime.utcnow() - timedelta(days=random.randint(0, 30))).strftime('%Y%m%d%H%M%S')
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    order_id = f"FZ-{timestamp}-{random_str}"
    
    # Check if order_id already exists
    existing = session.query(Payment).filter(Payment.order_id == order_id).first()
    if existing:
        continue
    
    admin_fee = 4000 if method == 'bank_transfer' else 0
    amount = plan['price'] + admin_fee
    
    created_at = datetime.utcnow() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
    
    payment = Payment(
        member_id=member.id,
        order_id=order_id,
        amount=amount,
        payment_method=method,
        status=status,
        membership_plan=plan['name'],
        duration_days=plan['duration'],
        va_number=f"1234{random.randint(10000000, 99999999)}" if method == 'bank_transfer' else None,
        created_at=created_at,
        updated_at=created_at,
        expired_at=created_at + timedelta(hours=24)
    )
    
    if status == 'success':
        payment.paid_at = created_at + timedelta(minutes=random.randint(5, 120))
        payment.transaction_id = f"TXN-{''.join(random.choices(string.ascii_uppercase + string.digits, k=12))}"
    
    payments_to_add.append(payment)
    print(f"Created payment {order_id} - {plan['name']} - {status} - Rp {amount:,.0f}")

session.add_all(payments_to_add)
session.commit()

print(f"\n✓ Successfully created {len(payments_to_add)} sample payments")
session.close()
