"""
Script untuk migrasi data dari database lokal ke Neon
"""
import psycopg2
from psycopg2.extras import RealDictCursor

# Konfigurasi database
LOCAL_DB = {
    'host': 'localhost',
    'database': 'gym_booking_db',
    'user': 'postgres',
    'password': '123140197'
}

NEON_DB = {
    'host': 'ep-orange-frog-a15c4gak-pooler.ap-southeast-1.aws.neon.tech',
    'database': 'neondb',
    'user': 'neondb_owner',
    'password': 'npg_nHK1Dyo0TrtC',
    'sslmode': 'require'
}

def get_connection(db_config):
    """Buat koneksi ke database"""
    return psycopg2.connect(**db_config)

def clear_neon_tables(neon_conn):
    """Hapus data di Neon untuk migrasi ulang"""
    cursor = neon_conn.cursor()
    
    # Disable foreign key checks temporarily
    tables = ['attendance', 'payments', 'bookings', 'reviews', 'members', 'classes', 'users']
    
    for table in tables:
        try:
            cursor.execute(f"DELETE FROM {table}")
            print(f"  ✓ Cleared {table}")
        except Exception as e:
            print(f"  ⚠ Skip {table}: {e}")
    
    neon_conn.commit()
    cursor.close()

def migrate_users(local_conn, neon_conn):
    """Migrasi tabel users"""
    print("\n📋 Migrasi tabel users...")
    
    local_cursor = local_conn.cursor(cursor_factory=RealDictCursor)
    neon_cursor = neon_conn.cursor()
    
    local_cursor.execute("SELECT * FROM users ORDER BY id")
    users = local_cursor.fetchall()
    
    for user in users:
        try:
            neon_cursor.execute("""
                INSERT INTO users (id, name, email, password, phone, address, avatar_url, role, 
                    is_approved, approval_status, rejection_reason, approved_at, approved_by, 
                    created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                user['id'], user['name'], user['email'], user['password'],
                user.get('phone'), user.get('address'), user.get('avatar_url'),
                user['role'], user.get('is_approved', True), user.get('approval_status', 'approved'),
                user.get('rejection_reason'), user.get('approved_at'), user.get('approved_by'),
                user['created_at'], user['updated_at']
            ))
        except Exception as e:
            print(f"  ⚠ Skip user {user['email']}: {e}")
    
    # Update sequence
    neon_cursor.execute("SELECT setval('users_id_seq', (SELECT MAX(id) FROM users))")
    
    neon_conn.commit()
    print(f"  ✓ Migrated {len(users)} users")
    
    local_cursor.close()
    neon_cursor.close()

def migrate_members(local_conn, neon_conn):
    """Migrasi tabel members"""
    print("\n📋 Migrasi tabel members...")
    
    local_cursor = local_conn.cursor(cursor_factory=RealDictCursor)
    neon_cursor = neon_conn.cursor()
    
    local_cursor.execute("SELECT * FROM members ORDER BY id")
    members = local_cursor.fetchall()
    
    for member in members:
        try:
            neon_cursor.execute("""
                INSERT INTO members (id, user_id, membership_plan, expiry_date)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                member['id'], member['user_id'], member.get('membership_plan'), member.get('expiry_date')
            ))
        except Exception as e:
            print(f"  ⚠ Skip member {member['id']}: {e}")
    
    # Update sequence
    neon_cursor.execute("SELECT setval('members_id_seq', (SELECT MAX(id) FROM members))")
    
    neon_conn.commit()
    print(f"  ✓ Migrated {len(members)} members")
    
    local_cursor.close()
    neon_cursor.close()

def migrate_classes(local_conn, neon_conn):
    """Migrasi tabel classes"""
    print("\n📋 Migrasi tabel classes...")
    
    local_cursor = local_conn.cursor(cursor_factory=RealDictCursor)
    neon_cursor = neon_conn.cursor()
    
    local_cursor.execute("SELECT * FROM classes ORDER BY id")
    classes = local_cursor.fetchall()
    
    for cls in classes:
        try:
            neon_cursor.execute("""
                INSERT INTO classes (id, trainer_id, name, description, schedule, capacity, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                cls['id'], cls['trainer_id'], cls['name'], cls.get('description'),
                cls['schedule'], cls['capacity'], cls['created_at']
            ))
        except Exception as e:
            print(f"  ⚠ Skip class {cls['name']}: {e}")
    
    # Update sequence
    neon_cursor.execute("SELECT setval('classes_id_seq', (SELECT MAX(id) FROM classes))")
    
    neon_conn.commit()
    print(f"  ✓ Migrated {len(classes)} classes")
    
    local_cursor.close()
    neon_cursor.close()

def migrate_bookings(local_conn, neon_conn):
    """Migrasi tabel bookings"""
    print("\n📋 Migrasi tabel bookings...")
    
    local_cursor = local_conn.cursor(cursor_factory=RealDictCursor)
    neon_cursor = neon_conn.cursor()
    
    local_cursor.execute("SELECT * FROM bookings ORDER BY id")
    bookings = local_cursor.fetchall()
    
    for booking in bookings:
        try:
            neon_cursor.execute("""
                INSERT INTO bookings (id, member_id, class_id, booking_date, status)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                booking['id'], booking['member_id'], booking['class_id'],
                booking['booking_date'], booking['status']
            ))
        except Exception as e:
            print(f"  ⚠ Skip booking {booking['id']}: {e}")
    
    # Update sequence
    neon_cursor.execute("SELECT setval('bookings_id_seq', (SELECT COALESCE(MAX(id), 1) FROM bookings))")
    
    neon_conn.commit()
    print(f"  ✓ Migrated {len(bookings)} bookings")
    
    local_cursor.close()
    neon_cursor.close()

def migrate_attendance(local_conn, neon_conn):
    """Migrasi tabel attendance"""
    print("\n📋 Migrasi tabel attendance...")
    
    local_cursor = local_conn.cursor(cursor_factory=RealDictCursor)
    neon_cursor = neon_conn.cursor()
    
    local_cursor.execute("SELECT * FROM attendance ORDER BY id")
    attendances = local_cursor.fetchall()
    
    for att in attendances:
        try:
            neon_cursor.execute("""
                INSERT INTO attendance (id, booking_id, attended, date)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                att['id'], att['booking_id'], att['attended'], att['date']
            ))
        except Exception as e:
            print(f"  ⚠ Skip attendance {att['id']}: {e}")
    
    # Update sequence
    neon_cursor.execute("SELECT setval('attendance_id_seq', (SELECT COALESCE(MAX(id), 1) FROM attendance))")
    
    neon_conn.commit()
    print(f"  ✓ Migrated {len(attendances)} attendance records")
    
    local_cursor.close()
    neon_cursor.close()

def migrate_reviews(local_conn, neon_conn):
    """Migrasi tabel reviews"""
    print("\n📋 Migrasi tabel reviews...")
    
    local_cursor = local_conn.cursor(cursor_factory=RealDictCursor)
    neon_cursor = neon_conn.cursor()
    
    local_cursor.execute("SELECT * FROM reviews ORDER BY id")
    reviews = local_cursor.fetchall()
    
    for review in reviews:
        try:
            neon_cursor.execute("""
                INSERT INTO reviews (id, class_id, user_id, rating, comment, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                review['id'], review['class_id'], review['user_id'], review['rating'],
                review.get('comment'), review['created_at'], review.get('updated_at')
            ))
        except Exception as e:
            print(f"  ⚠ Skip review {review['id']}: {e}")
    
    # Update sequence
    neon_cursor.execute("SELECT setval('reviews_id_seq', (SELECT COALESCE(MAX(id), 1) FROM reviews))")
    
    neon_conn.commit()
    print(f"  ✓ Migrated {len(reviews)} reviews")
    
    local_cursor.close()
    neon_cursor.close()

def migrate_payments(local_conn, neon_conn):
    """Migrasi tabel payments"""
    print("\n📋 Migrasi tabel payments...")
    
    local_cursor = local_conn.cursor(cursor_factory=RealDictCursor)
    neon_cursor = neon_conn.cursor()
    
    local_cursor.execute("SELECT * FROM payments ORDER BY id")
    payments = local_cursor.fetchall()
    
    for payment in payments:
        try:
            neon_cursor.execute("""
                INSERT INTO payments (id, member_id, order_id, amount, payment_method, status,
                    membership_plan, duration_days, transaction_id, payment_url, va_number,
                    created_at, updated_at, paid_at, expired_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                payment['id'], payment['member_id'], payment['order_id'], payment['amount'],
                payment.get('payment_method'), payment.get('status'), payment['membership_plan'],
                payment.get('duration_days'), payment.get('transaction_id'), payment.get('payment_url'),
                payment.get('va_number'), payment['created_at'], payment.get('updated_at'),
                payment.get('paid_at'), payment.get('expired_at')
            ))
        except Exception as e:
            print(f"  ⚠ Skip payment {payment['id']}: {e}")
    
    # Update sequence
    neon_cursor.execute("SELECT setval('payments_id_seq', (SELECT COALESCE(MAX(id), 1) FROM payments))")
    
    neon_conn.commit()
    print(f"  ✓ Migrated {len(payments)} payments")
    
    local_cursor.close()
    neon_cursor.close()

def main():
    print("=" * 60)
    print("🚀 MIGRASI DATA: Local PostgreSQL → Neon Cloud")
    print("=" * 60)
    
    try:
        print("\n🔌 Connecting to Local Database...")
        local_conn = get_connection(LOCAL_DB)
        print("  ✓ Connected to Local Database")
        
        print("\n🔌 Connecting to Neon Database...")
        neon_conn = get_connection(NEON_DB)
        print("  ✓ Connected to Neon Database")
        
        print("\n🗑️ Clearing existing data in Neon...")
        clear_neon_tables(neon_conn)
        
        # Migrasi semua tabel
        migrate_users(local_conn, neon_conn)
        migrate_members(local_conn, neon_conn)
        migrate_classes(local_conn, neon_conn)
        migrate_bookings(local_conn, neon_conn)
        migrate_attendance(local_conn, neon_conn)
        migrate_reviews(local_conn, neon_conn)
        migrate_payments(local_conn, neon_conn)
        
        print("\n" + "=" * 60)
        print("✅ MIGRASI SELESAI!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise
    finally:
        if 'local_conn' in locals():
            local_conn.close()
        if 'neon_conn' in locals():
            neon_conn.close()

if __name__ == '__main__':
    main()
