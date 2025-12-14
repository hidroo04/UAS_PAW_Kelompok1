"""
Simple script to seed sample data into the database
"""
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import hashlib

# Import models
from app.models import User, Member, Class, Booking, Attendance, UserRole

# Database URL
DB_URL = "postgresql://postgres:ripaldy@localhost/gym_booking_db"

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
        
        # Create users
        admin_user = User(
            name="Admin User",
            email="admin@gym.com",
            password=hash_password("admin123"),
            role=UserRole.ADMIN
        )
        
        trainer_user = User(
            name="John Trainer",
            email="trainer@gym.com",
            password=hash_password("trainer123"),
            role=UserRole.TRAINER
        )
        
        member_user = User(
            name="Jane Member",
            email="member@gym.com",
            password=hash_password("member123"),
            role=UserRole.MEMBER
        )
        
        session.add_all([admin_user, trainer_user, member_user])
        session.flush()  # Get IDs
        
        print(f"\n✅ Created users:")
        print(f"   - Admin (ID: {admin_user.id})")
        print(f"   - Trainer (ID: {trainer_user.id})")
        print(f"   - Member (ID: {member_user.id})")
        
        # Create member profile
        member_profile = Member(
            user_id=member_user.id,
            membership_plan="Premium",
            expiry_date=(datetime.now() + timedelta(days=365)).date()
        )
        session.add(member_profile)
        session.flush()
        
        print(f"\n✅ Created member profile (ID: {member_profile.id})")
        
        # Create classes
        class1 = Class(
            trainer_id=trainer_user.id,
            name="Yoga Basics",
            description="Perfect for beginners looking to improve flexibility",
            schedule=datetime.now() + timedelta(days=1, hours=9),
            capacity=20
        )
        
        class2 = Class(
            trainer_id=trainer_user.id,
            name="HIIT Training",
            description="High-intensity interval training for maximum results",
            schedule=datetime.now() + timedelta(days=2, hours=18),
            capacity=15
        )
        
        class3 = Class(
            trainer_id=trainer_user.id,
            name="Pilates Flow",
            description="Core strengthening and body conditioning",
            schedule=datetime.now() + timedelta(days=3, hours=10),
            capacity=12
        )
        
        session.add_all([class1, class2, class3])
        session.flush()
        
        print(f"\n✅ Created classes:")
        print(f"   - {class1.name} (ID: {class1.id})")
        print(f"   - {class2.name} (ID: {class2.id})")
        print(f"   - {class3.name} (ID: {class3.id})")
        
        # Create a sample booking
        booking1 = Booking(
            member_id=member_profile.id,
            class_id=class1.id,
            booking_date=datetime.now()
        )
        session.add(booking1)
        session.flush()
        
        print(f"\n✅ Created sample booking (ID: {booking1.id})")
        
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
        print("\nTrainer:")
        print("  Email: trainer@gym.com")
        print("  Password: trainer123")
        print("\nMember:")
        print("  Email: member@gym.com")
        print("  Password: member123")
        print("=" * 60)
        
    except Exception as e:
        session.rollback()
        print(f"\n❌ Error: {e}")
        raise
    finally:
        session.close()

if __name__ == '__main__':
    seed_data()
