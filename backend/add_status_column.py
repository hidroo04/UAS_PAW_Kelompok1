"""Add status column to bookings table"""
from sqlalchemy import create_engine, text

engine = create_engine('postgresql://postgres:123140197@localhost/gym_booking_db')
conn = engine.connect()

try:
    conn.execute(text("ALTER TABLE bookings ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'confirmed'"))
    conn.commit()
    print('Column status added successfully!')
except Exception as e:
    print(f'Error or column already exists: {e}')
finally:
    conn.close()
