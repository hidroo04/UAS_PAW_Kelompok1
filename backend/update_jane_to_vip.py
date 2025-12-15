from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Member, User

engine = create_engine('postgresql://postgres:ripaldy@localhost/gym_booking_db')
Session = sessionmaker(bind=engine)
session = Session()

# Find Jane Member (user_id = 3)
jane_member = session.query(Member).filter(Member.user_id == 3).first()

if jane_member:
    print(f"Current membership: {jane_member.membership_plan}")
    
    # Update to VIP
    jane_member.membership_plan = 'VIP'
    session.commit()
    
    print(f"Updated to: {jane_member.membership_plan}")
    print("✅ Jane Member is now VIP!")
else:
    print("❌ Jane Member not found")

# Show all members with their membership types
print("\n=== ALL MEMBERS ===")
members = session.query(Member).all()
for member in members:
    user = session.query(User).filter(User.id == member.user_id).first()
    print(f"{user.name} ({user.email}): {member.membership_plan}")

session.close()
