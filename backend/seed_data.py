"""
Simple script to seed sample data into the database
"""
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import hashlib

# Import models
from app.models import User, Member, GymClass, Booking, Attendance, UserRole

# Database URL
DB_URL = "postgresql://postgres:123140197@localhost/gym_booking_db"

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def seed_data():
    """Seed sample data into database"""
    engine = create_engine(DB_URL, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        print("\n" + "=" * 60)
        print("Seeding Sample Data")
        print("=" * 60)
        
        # Clear existing data
        print("\n🗑️  Clearing existing data...")
        session.query(Attendance).delete()
        session.query(Booking).delete()
        session.query(GymClass).delete()
        session.query(Member).delete()
        session.query(User).delete()
        session.commit()
        print("✅ Existing data cleared")
        
        # Create admin
        admin_user = User(
            name="Admin User",
            email="admin@gym.com",
            password=hash_password("admin123"),
            role=UserRole.ADMIN
        )
        session.add(admin_user)
        session.flush()
        print(f"\n✅ Created Admin (ID: {admin_user.id})")
        
        # Create 4 trainers
        trainers = [
            User(
                name="John Smith",
                email="john.trainer@gym.com",
                password=hash_password("trainer123"),
                role=UserRole.TRAINER
            ),
            User(
                name="Sarah Johnson",
                email="sarah.trainer@gym.com",
                password=hash_password("trainer123"),
                role=UserRole.TRAINER
            ),
            User(
                name="Mike Chen",
                email="mike.trainer@gym.com",
                password=hash_password("trainer123"),
                role=UserRole.TRAINER
            ),
            User(
                name="Emily Davis",
                email="emily.trainer@gym.com",
                password=hash_password("trainer123"),
                role=UserRole.TRAINER
            )
        ]
        session.add_all(trainers)
        session.flush()
        
        print(f"\n✅ Created {len(trainers)} Trainers:")
        for i, trainer in enumerate(trainers, 1):
            print(f"   {i}. {trainer.name} (ID: {trainer.id})")
        
        # Create 10 members
        members_data = [
            {"name": "Alice Brown", "email": "alice@member.com", "plan": "VIP"},
            {"name": "Bob Wilson", "email": "bob@member.com", "plan": "Premium"},
            {"name": "Charlie Martinez", "email": "charlie@member.com", "plan": "Basic"},
            {"name": "Diana Lee", "email": "diana@member.com", "plan": "VIP"},
            {"name": "Ethan Taylor", "email": "ethan@member.com", "plan": "Premium"},
            {"name": "Fiona Anderson", "email": "fiona@member.com", "plan": "Basic"},
            {"name": "George Thomas", "email": "george@member.com", "plan": "Premium"},
            {"name": "Hannah White", "email": "hannah@member.com", "plan": "VIP"},
            {"name": "Ian Harris", "email": "ian@member.com", "plan": "Basic"},
            {"name": "Julia Clark", "email": "julia@member.com", "plan": "Premium"}
        ]
        
        member_users = []
        member_profiles = []
        
        for member_data in members_data:
            member_user = User(
                name=member_data["name"],
                email=member_data["email"],
                password=hash_password("member123"),
                role=UserRole.MEMBER
            )
            session.add(member_user)
            session.flush()
            
            member_profile = Member(
                user_id=member_user.id,
                membership_plan=member_data["plan"],
                expiry_date=(datetime.now() + timedelta(days=365)).date()
            )
            session.add(member_profile)
            
            member_users.append(member_user)
            member_profiles.append(member_profile)
        
        session.flush()
        
        print(f"\n✅ Created {len(member_users)} Members:")
        for i, (user, profile) in enumerate(zip(member_users, member_profiles), 1):
            print(f"   {i}. {user.name} - {profile.membership_plan} (ID: {user.id})")
        
        # Create classes for different trainers
        classes_data = [
            {"trainer": trainers[0], "name": "Yoga Basics", "desc": "Perfect for beginners looking to improve flexibility", "days": 1, "hours": 9, "capacity": 20},
            {"trainer": trainers[0], "name": "Morning Stretch", "desc": "Start your day with energizing stretches", "days": 2, "hours": 7, "capacity": 15},
            {"trainer": trainers[1], "name": "HIIT Training", "desc": "High-intensity interval training for maximum results", "days": 1, "hours": 18, "capacity": 15},
            {"trainer": trainers[1], "name": "Cardio Blast", "desc": "Burn calories with intense cardio workout", "days": 3, "hours": 17, "capacity": 20},
            {"trainer": trainers[2], "name": "Pilates Flow", "desc": "Core strengthening and body conditioning", "days": 2, "hours": 10, "capacity": 12},
            {"trainer": trainers[2], "name": "Strength Training", "desc": "Build muscle and increase strength", "days": 4, "hours": 16, "capacity": 18},
            {"trainer": trainers[3], "name": "Zumba Dance", "desc": "Fun dance workout to Latin beats", "days": 1, "hours": 19, "capacity": 25},
            {"trainer": trainers[3], "name": "Spin Class", "desc": "Indoor cycling for endurance", "days": 3, "hours": 18, "capacity": 20}
        ]
        
        gym_classes = []
        for class_data in classes_data:
            gym_class = GymClass(
                trainer_id=class_data["trainer"].id,
                name=class_data["name"],
                description=class_data["desc"],
                schedule=datetime.now() + timedelta(days=class_data["days"], hours=class_data["hours"]),
                capacity=class_data["capacity"]
            )
            session.add(gym_class)
            gym_classes.append(gym_class)
        
        session.flush()
        
        print(f"\n✅ Created {len(gym_classes)} Classes:")
        for i, gym_class in enumerate(gym_classes, 1):
            print(f"   {i}. {gym_class.name} - Trainer: {gym_class.trainer.name} (ID: {gym_class.id})")
        
        # Create sample bookings
        import random
        bookings = []
        for i, member_profile in enumerate(member_profiles[:7]):  # First 7 members book classes
            # Each member books 1-3 random classes
            num_bookings = random.randint(1, 3)
            selected_classes = random.sample(gym_classes, num_bookings)
            
            for gym_class in selected_classes:
                booking = Booking(
                    member_id=member_profile.id,
                    class_id=gym_class.id,
                    booking_date=datetime.now() - timedelta(days=random.randint(0, 7))
                )
                session.add(booking)
                bookings.append(booking)
        
        session.flush()
        
        print(f"\n✅ Created {len(bookings)} Sample Bookings")
        
        # Commit all changes
        session.commit()
        
        print("\n" + "=" * 60)
        print("✅ Sample Data Seeded Successfully!")
        print("=" * 60)
        print("\n📋 Test Credentials:")
        print("-" * 60)
        print("Admin:")
        print("  Email: admin@gym.com")
        print("  Password: admin123")
        print("\nTrainers (All use password: trainer123):")
        print("  1. john.trainer@gym.com - John Smith")
        print("  2. sarah.trainer@gym.com - Sarah Johnson")
        print("  3. mike.trainer@gym.com - Mike Chen")
        print("  4. emily.trainer@gym.com - Emily Davis")
        print("\nMembers (All use password: member123):")
        print("  1. alice@member.com - Alice Brown (VIP)")
        print("  2. bob@member.com - Bob Wilson (Premium)")
        print("  3. charlie@member.com - Charlie Martinez (Basic)")
        print("  4. diana@member.com - Diana Lee (VIP)")
        print("  5. ethan@member.com - Ethan Taylor (Premium)")
        print("  6. fiona@member.com - Fiona Anderson (Basic)")
        print("  7. george@member.com - George Thomas (Premium)")
        print("  8. hannah@member.com - Hannah White (VIP)")
        print("  9. ian@member.com - Ian Harris (Basic)")
        print("  10. julia@member.com - Julia Clark (Premium)")
        print("=" * 60)
        print(f"\n📊 Summary:")
        print(f"  - Total Users: {1 + len(trainers) + len(member_users)}")
        print(f"  - Trainers: {len(trainers)}")
        print(f"  - Members: {len(member_users)}")
        print(f"  - Classes: {len(gym_classes)}")
        print(f"  - Bookings: {len(bookings)}")
        print("=" * 60)
        
    except Exception as e:
        session.rollback()
        print(f"\n❌ Error: {e}")
        raise
    finally:
        session.close()

if __name__ == '__main__':
    seed_data()
