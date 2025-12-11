"""
Database initialization script
Run this script to create all tables in PostgreSQL database
"""
from sqlalchemy import create_engine
from app.models import Base, User, UserRole, Member, Class, Booking, Attendance
from datetime import datetime, timedelta
import hashlib


def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def init_database(db_url):
    """Initialize database with tables"""
    print("Creating database engine...")
    engine = create_engine(db_url, echo=True)
    
    print("\nCreating all tables...")
    Base.metadata.create_all(engine)
    
    print("\n✅ Database tables created successfully!")
    return engine


def seed_sample_data(db_url):
    """Add sample data for testing"""
    from sqlalchemy.orm import sessionmaker
    
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        print("\nAdding sample data...")
        
        # Create admin user
        admin = User(
            name="Admin User",
            email="admin@gymbook.com",
            password=hash_password("admin123"),
            role=UserRole.ADMIN
        )
        session.add(admin)
        
        # Create trainer
        trainer = User(
            name="John Trainer",
            email="trainer@gymbook.com",
            password=hash_password("trainer123"),
            role=UserRole.TRAINER
        )
        session.add(trainer)
        
        # Create member
        member_user = User(
            name="Jane Member",
            email="member@gymbook.com",
            password=hash_password("member123"),
            role=UserRole.MEMBER
        )
        session.add(member_user)
        
        session.flush()  # Get IDs
        
        # Create membership
        member = Member(
            user_id=member_user.id,
            membership_plan="Premium",
            expiry_date=(datetime.now() + timedelta(days=30)).date()
        )
        session.add(member)
        
        # Create sample classes
        classes = [
            Class(
                trainer_id=trainer.id,
                name="Yoga Morning",
                description="Relaxing yoga session to start your day",
                schedule=datetime.now() + timedelta(days=1, hours=7),
                capacity=20
            ),
            Class(
                trainer_id=trainer.id,
                name="HIIT Workout",
                description="High intensity interval training",
                schedule=datetime.now() + timedelta(days=1, hours=18),
                capacity=15
            ),
            Class(
                trainer_id=trainer.id,
                name="Strength Training",
                description="Build muscle and strength",
                schedule=datetime.now() + timedelta(days=2, hours=10),
                capacity=12
            )
        ]
        
        for cls in classes:
            session.add(cls)
        
        session.commit()
        print("✅ Sample data added successfully!")
        
        print("\n📝 Sample Login Credentials:")
        print("Admin: admin@gymbook.com / admin123")
        print("Trainer: trainer@gymbook.com / trainer123")
        print("Member: member@gymbook.com / member123")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error adding sample data: {e}")
    finally:
        session.close()


if __name__ == '__main__':
    import sys
    
    # Database URL - update with your PostgreSQL credentials
    DB_URL = "postgresql://postgres:ripaldy@localhost/gym_booking_db"
    
    if len(sys.argv) > 1:
        DB_URL = sys.argv[1]
    
    print("=" * 60)
    print("GymBook Database Initialization")
    print("=" * 60)
    print(f"\nDatabase URL: {DB_URL}")
    
    # Initialize database
    engine = init_database(DB_URL)
    
    # Ask if user wants to add sample data
    add_sample = input("\nDo you want to add sample data? (yes/no): ").lower()
    if add_sample in ['yes', 'y']:
        seed_sample_data(DB_URL)
    
    print("\n" + "=" * 60)
    print("Database setup completed!")
    print("=" * 60)
