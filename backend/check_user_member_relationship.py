"""Check all users and their member records"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User, Member

# Database connection
DATABASE_URL = "postgresql://postgres:123140197@localhost/gym_booking_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
db = Session()

try:
    print("=== Checking User-Member Relationships ===\n")
    
    # Get all users with role 'member'
    member_users = db.query(User).filter(User.role == 'member').all()
    print(f"Found {len(member_users)} users with role 'member'\n")
    
    for user in member_users:
        print(f"User: {user.name} ({user.email})")
        print(f"  User ID: {user.id}")
        print(f"  Role: {user.role}")
        
        # Check if member record exists
        member = db.query(Member).filter(Member.user_id == user.id).first()
        if member:
            print(f"  ✓ Member record exists (Member ID: {member.id}, Plan: {member.membership_plan})")
        else:
            print(f"  ✗ NO MEMBER RECORD FOUND!")
        print()
    
    # Also check all member records
    print("\n=== All Member Records ===")
    all_members = db.query(Member).all()
    print(f"Total member records: {len(all_members)}\n")
    
    for member in all_members:
        user = db.query(User).filter(User.id == member.user_id).first()
        if user:
            print(f"Member ID: {member.id}")
            print(f"  User: {user.name} ({user.email})")
            print(f"  User ID: {member.user_id}")
            print(f"  Plan: {member.membership_plan}")
        else:
            print(f"Member ID: {member.id}")
            print(f"  ✗ Orphaned member record (user_id={member.user_id} not found)")
        print()
        
finally:
    db.close()
