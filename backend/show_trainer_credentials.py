"""
Display trainer login credentials
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User

# Database connection
DATABASE_URL = "postgresql://postgres:123140197@localhost/gym_booking_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
db = Session()

print("\n" + "=" * 60)
print("TRAINER LOGIN CREDENTIALS")
print("=" * 60)

trainers = db.query(User).filter(User.role == 'trainer').all()

if trainers:
    for trainer in trainers:
        print(f"\nTrainer: {trainer.name}")
        print(f"Email: {trainer.email}")
        print(f"Password: trainer123")  # Default password for all trainers
        print("-" * 60)
else:
    print("\nNo trainers found in database")

print("\n" + "=" * 60)
print(f"Total Trainers: {len(trainers)}")
print("=" * 60 + "\n")

db.close()
