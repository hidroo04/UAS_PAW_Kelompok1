from sqlalchemy import create_engine, text

try:
    engine = create_engine('postgresql://postgres:ripaldy@localhost/gym_booking_db')
    conn = engine.connect()
    
    print('=' * 80)
    print('DAFTAR CLASSES')
    print('=' * 80)
    
    # Query semua classes
    result = conn.execute(text("""
        SELECT 
            c.id,
            c.name,
            c.schedule,
            c.duration,
            c.capacity,
            u.name as trainer_name
        FROM classes c
        LEFT JOIN users u ON c.trainer_id = u.id
        ORDER BY c.schedule
    """))
    
    classes = result.fetchall()
    
    if classes:
        print(f'\nTotal kelas: {len(classes)}\n')
        for cls in classes:
            print(f'ID: {cls[0]}')
            print(f'Nama: {cls[1]}')
            print(f'Trainer: {cls[5]}')
            print(f'Schedule: {cls[2]}')
            print(f'Duration: {cls[3]} minutes')
            print(f'Capacity: {cls[4]}')
            print('-' * 80)
    else:
        print('\n⚠ Belum ada data kelas')
        print('💡 Jalankan: python seed_data.py untuk membuat data dummy')
    
    conn.close()
    
except Exception as e:
    print(f'✗ Error: {str(e)}')
