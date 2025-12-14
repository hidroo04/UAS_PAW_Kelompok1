from sqlalchemy import create_engine, text

try:
    engine = create_engine('postgresql://postgres:ripaldy@localhost/gym_booking_db')
    conn = engine.connect()
    
    print('✓ Database terhubung ke PostgreSQL!')
    print('✓ Database: gym_booking_db')
    print('✓ Host: localhost')
    
    # Cek tabel
    result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name"))
    tables = [row[0] for row in result.fetchall()]
    
    print(f'\n✓ Jumlah tabel: {len(tables)}')
    if tables:
        print('\nDaftar tabel:')
        for t in tables:
            print(f'  - {t}')
    else:
        print('\n⚠ Belum ada tabel (perlu migration: alembic upgrade head)')
    
    conn.close()
    
except Exception as e:
    print(f'✗ GAGAL: {str(e)}')
