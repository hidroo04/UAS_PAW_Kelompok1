from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Member, User

engine = create_engine('postgresql://postgres:ripaldy@localhost/gym_booking_db')
Session = sessionmaker(bind=engine)
session = Session()

print("=== CHECKING MEMBERS TABLE ===\n")

members = session.query(Member).all()
print(f"Total members: {len(members)}\n")

for member in members:
    user = session.query(User).filter(User.id == member.user_id).first()
    print(f"Member ID: {member.id}")
    print(f"  User ID: {member.user_id}")
    if user:
        print(f"  User Name: {user.name}")
        print(f"  User Email: {user.email}")
        print(f"  User Role: {user.role}")
    print()

session.close()
