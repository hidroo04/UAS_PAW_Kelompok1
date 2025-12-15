#!/usr/bin/env python
"""
Script untuk memeriksa akun admin dan membuat jika belum ada
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import User, UserRole
from app.utils.auth import hash_password
from datetime import datetime

# Database URL
DATABASE_URL = "postgresql://postgres:ripaldy@localhost/gym_booking_db"

# Create engine
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
db = Session()

try:
    # Cek admin yang sudah ada
    admins = db.query(User).filter(User.role == UserRole.ADMIN).all()
    
    if admins:
        print(f"\n✅ Ditemukan {len(admins)} akun admin:\n")
        for admin in admins:
            print(f"  ID: {admin.id}")
            print(f"  Name: {admin.name}")
            print(f"  Email: {admin.email}")
            print(f"  Role: {admin.role.value}")
            print(f"  Created: {admin.created_at}")
            print("-" * 50)
    else:
        print("\n❌ Tidak ada akun admin!")
        print("\n🔨 Membuat akun admin default...\n")
        
        # Buat admin baru
        admin_user = User(
            name="Admin FitZone",
            email="admin@gym.com",
            password=hash_password("admin123"),
            role=UserRole.ADMIN,
            created_at=datetime.utcnow()
        )
        
        db.add(admin_user)
        db.commit()
        
        print("✅ Akun admin berhasil dibuat!")
        print(f"  Email: admin@gym.com")
        print(f"  Password: admin123")
        print(f"  Role: admin")
        print("\n⚠️  Jangan lupa ganti password setelah login pertama!")
    
    # Tampilkan semua user
    print("\n" + "=" * 50)
    print("📋 Semua User di Database:")
    print("=" * 50)
    all_users = db.query(User).all()
    for user in all_users:
        print(f"\n  ID: {user.id} | {user.name} ({user.email})")
        print(f"  Role: {user.role.value}")

except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()
