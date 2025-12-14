from sqlalchemy import create_engine, text

try:
    engine = create_engine('postgresql://postgres:ripaldy@localhost/gym_booking_db')
    conn = engine.connect()
    
    print('=' * 80)
    print('DAFTAR AKUN USERS')
    print('=' * 80)
    
    # Query semua user dengan info member jika ada
    result = conn.execute(text("""
        SELECT 
            u.id,
            u.name,
            u.email,
            u.role,
            m.membership_plan,
            m.expiry_date
        FROM users u
        LEFT JOIN members m ON u.id = m.user_id
        ORDER BY u.id
    """))
    
    users = result.fetchall()
    
    if users:
        print(f'\nTotal akun: {len(users)}\n')
        for user in users:
            print(f'ID: {user[0]}')
            print(f'Nama: {user[1]}')
            print(f'Email: {user[2]}')
            print(f'Role: {user[3]}')
            if user[4]:  # Jika ada membership_plan
                print(f'Membership: {user[4]}')
                print(f'Expiry: {user[5]}')
            print('-' * 80)
    else:
        print('\n⚠ Belum ada akun user di database')
        print('💡 Jalankan: python seed_data.py untuk membuat data dummy')
    
    conn.close()
    
except Exception as e:
    print(f'✗ Error: {str(e)}')
