"""
Check member data in database
"""
from app.models import User, Member
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database connection
DATABASE_URL = "postgresql://postgres:123140197@localhost/gym_booking_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

print("\n=== CHECKING MEMBER DATA ===\n")

# Get all members
members = session.query(Member).all()
print(f"Total Members: {len(members)}\n")

for member in members:
    user = session.query(User).filter(User.id == member.user_id).first()
    if user:
        print(f"Member ID: {member.id}")
        print(f"User: {user.name} ({user.email})")
        print(f"Plan: {member.membership_plan}")
        print(f"Expiry: {member.expiry_date}")
        print(f"Active: {member.is_active()}")
        print(f"User to_dict: {user.to_dict()}")
        print("-" * 50)

session.close()
