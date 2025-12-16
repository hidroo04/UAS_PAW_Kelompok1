"""
Script to reset all user passwords to known values
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import hashlib

# Import models
from app.models import User, UserRole

# Database URL
DB_URL = "postgresql://postgres:123140197@localhost/gym_booking_db"

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def reset_passwords():
    """Reset all user passwords"""
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        print("\n" + "=" * 80)
        print("RESET PASSWORD - GYM BOOKING SYSTEM")
        print("=" * 80)
        
        # Get all users
        users = session.query(User).all()
        
        if not users:
            print("\n❌ Tidak ada user ditemukan!")
            return
        
        # Password mappings
        password_map = {
            'admin@gym.com': 'admin123',
            'trainer@gym.com': 'trainer123',
            'member@gym.com': 'member123',
            'john@example.com': 'password123',
            'admin@gymbook.com': 'admin123',
            'trainer@gymbook.com': 'trainer123',
            'member@gymbook.com': 'member123'
        }
        
        print("\nMengupdate password untuk semua user...\n")
        
        for user in users:
            # Get password for this user
            new_password = password_map.get(user.email)
            
            if new_password:
                # Update password
                user.password = hash_password(new_password)
                print(f"✅ Updated: {user.email}")
                print(f"   Nama: {user.name}")
                print(f"   Role: {user.role.value}")
                print(f"   Password: {new_password}")
                print(f"   Hash: {user.password[:20]}...")
            else:
                print(f"⚠️  Skipped: {user.email} (no password mapping)")
            print("-" * 80)
        
        session.commit()
        
        print("\n" + "=" * 80)
        print("PASSWORD RESET SELESAI!")
        print("=" * 80)
        print("\n📝 DAFTAR LOGIN:")
        print("-" * 80)
        
        for user in users:
            password = password_map.get(user.email, "???")
            print(f"Email: {user.email}")
            print(f"Password: {password}")
            print(f"Role: {user.role.value}")
            print("-" * 80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    reset_passwords()
