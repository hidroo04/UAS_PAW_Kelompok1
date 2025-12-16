"""Check if member exists for alice"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User, Member

# Database connection
DATABASE_URL = "postgresql://postgres:123140197@localhost/gym_booking_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
db = Session()

try:
    # Find Alice
    alice = db.query(User).filter(User.email == 'alice@member.com').first()
    if alice:
        print(f"✓ Alice found - User ID: {alice.id}, Name: {alice.name}")
        
        # Check member record
        member = db.query(Member).filter(Member.user_id == alice.id).first()
        if member:
            print(f"✓ Member record found - Member ID: {member.id}")
            print(f"  Membership Plan: {member.membership_plan}")
            print(f"  Join Date: {member.join_date}")
        else:
            print(f"✗ NO MEMBER RECORD for user_id={alice.id}")
            print("\nAll members in database:")
            all_members = db.query(Member).all()
            for m in all_members:
                user = db.query(User).filter(User.id == m.user_id).first()
                print(f"  Member ID: {m.id}, User ID: {m.user_id}, Email: {user.email if user else 'N/A'}")
    else:
        print("✗ Alice user not found")
        
finally:
    db.close()
