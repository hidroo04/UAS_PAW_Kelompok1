"""
Check trainer user data and verify profile functionality
"""
from app.models import User, UserRole
from pyramid.paster import bootstrap
import os

# Get the absolute path to development.ini
current_dir = os.path.dirname(os.path.abspath(__file__))
ini_path = os.path.join(current_dir, 'development.ini')

env = bootstrap(ini_path)
request = env['request']
dbsession = request.dbsession

print("=== CHECKING TRAINER DATA ===\n")

# Get all trainers
trainers = dbsession.query(User).filter(User.role == UserRole.TRAINER).all()

print(f"Total Trainers: {len(trainers)}\n")

for trainer in trainers:
    print(f"Trainer ID: {trainer.id}")
    print(f"Name: {trainer.name}")
    print(f"Email: {trainer.email}")
    print(f"Phone: {trainer.phone}")
    print(f"Address: {trainer.address}")
    print(f"Role: {trainer.role.value}")
    print(f"Created: {trainer.created_at}")
    
    # Check to_dict() output
    trainer_dict = trainer.to_dict()
    print(f"\nTrainer to_dict():")
    print(trainer_dict)
    
    # Check if trainer has member record (should not have)
    has_member = trainer.member is not None
    print(f"\nHas Member Record: {has_member}")
    if has_member:
        print(f"Warning: Trainer {trainer.name} has member record!")
    
    print("-" * 50)

print("\n=== Trainer Login Credentials ===")
print("Email: john@trainer.com")
print("Password: password123")
print("\nEmail: sarah@trainer.com") 
print("Password: password123")

env['closer']()
