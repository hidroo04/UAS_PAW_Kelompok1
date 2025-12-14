from sqlalchemy import create_engine, text

try:
    engine = create_engine('postgresql://postgres:ripaldy@localhost/gym_booking_db')
    conn = engine.connect()
    
    print('=' * 80)
    print('STRUKTUR TABEL CLASSES')
    print('=' * 80)
    
    # Query struktur tabel
    result = conn.execute(text("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = 'classes'
        ORDER BY ordinal_position
    """))
    
    columns = result.fetchall()
    
    print('\nKolom-kolom di tabel classes:')
    for col in columns:
        print(f'  - {col[0]} ({col[1]}) - Nullable: {col[2]}')
    
    # Cek isi data
    print('\n' + '=' * 80)
    print('DATA CLASSES')
    print('=' * 80)
    
    result2 = conn.execute(text("SELECT * FROM classes LIMIT 5"))
    classes = result2.fetchall()
    
    print(f'\nTotal kelas: {len(classes)}')
    if classes:
        print('\nSample data (5 pertama):')
        for cls in classes:
            print(f'  {cls}')
    else:
        print('\n⚠ Tidak ada data kelas')
        print('💡 Jalankan: python seed_data.py')
    
    conn.close()
    
except Exception as e:
    print(f'✗ Error: {str(e)}')
