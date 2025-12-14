from sqlalchemy import create_engine, inspect

engine = create_engine('postgresql://postgres:ripaldy@localhost/gym_booking_db')
inspector = inspect(engine)

columns = inspector.get_columns('bookings')
print("Bookings table columns:")
for col in columns:
    print(f"  - {col['name']}: {col['type']}")
