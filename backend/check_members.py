from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Member, User

engine = create_engine('postgresql://postgres:123140197@localhost/gym_booking_db')
Session = sessionmaker(bind=engine)
session = Session()

print("=== CHECKING MEMBERS TABLE ===\n")

members = session.query(Member).all()
print(f"Total members: {len(members)}\n")

# Count membership plans
basic_count = 0
premium_count = 0
vip_count = 0

for member in members:
    user = session.query(User).filter(User.id == member.user_id).first()
    print(f"Member ID: {member.id}")
    print(f"  User ID: {member.user_id}")
    print(f"  Membership Plan: {member.membership_plan}")
    print(f"  Expiry Date: {member.expiry_date}")
    print(f"  Is Active: {member.is_active()}")
    if user:
        print(f"  User Name: {user.name}")
        print(f"  User Email: {user.email}")
        print(f"  User Role: {user.role}")
    
    # Count plans
    if member.membership_plan:
        plan_lower = member.membership_plan.lower()
        if plan_lower == 'basic':
            basic_count += 1
        elif plan_lower == 'premium':
            premium_count += 1
        elif plan_lower == 'vip':
            vip_count += 1
    
    print()

print("\n=== MEMBERSHIP DISTRIBUTION ===")
print(f"Basic Members: {basic_count}")
print(f"Premium Members: {premium_count}")
print(f"VIP Members: {vip_count}")
print(f"Total: {basic_count + premium_count + vip_count}")

session.close()
