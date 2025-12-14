from sqlalchemy import create_engine, text
import hashlib

def hash_password(password):
    """Hash password menggunakan SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

try:
    engine = create_engine('postgresql://postgres:ripaldy@localhost/gym_booking_db')
    conn = engine.connect()
    
    print('=' * 80)
    print('DAFTAR AKUN & PASSWORD (TESTING)')
    print('=' * 80)
    
    # Query semua user
    result = conn.execute(text("""
        SELECT 
            u.id,
            u.name,
            u.email,
            u.role,
            u.password
        FROM users u
        ORDER BY u.id
    """))
    
    users = result.fetchall()
    
    # Test beberapa password umum
    common_passwords = ['password123', '123456', 'password', 'admin123', 'member123']
    
    print(f'\nTotal akun: {len(users)}\n')
    
    for user in users:
        print(f'📧 Email: {user[2]}')
        print(f'👤 Nama: {user[1]}')
        print(f'🎭 Role: {user[3]}')
        print(f'🔐 Password Hash: {user[4][:20]}...')
        
        # Coba cocokkan dengan password umum
        password_found = None
        for pwd in common_passwords:
            if hash_password(pwd) == user[4]:
                password_found = pwd
                break
        
        if password_found:
            print(f'✅ Password: {password_found}')
        else:
            print(f'❓ Password: (tidak diketahui, coba cek seed_data.py)')
        
        print('-' * 80)
    
    conn.close()
    
except Exception as e:
    print(f'✗ Error: {str(e)}')
