"""
Script to create payments table and verify database setup
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost/gym_booking_db')
engine = create_engine(DATABASE_URL)

# Check existing tables
print("=" * 50)
print("Checking database tables...")
print("=" * 50)

with engine.connect() as conn:
    result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
    tables = [r[0] for r in result]
    print("Existing tables:")
    for t in tables:
        print(f"  - {t}")
    
    # Check if payments table exists
    if 'payments' in tables:
        print("\n✓ Payments table already exists")
        # Check columns
        cols = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'payments' ORDER BY ordinal_position"))
        print("\nPayments table columns:")
        for col in cols:
            print(f"  - {col[0]}: {col[1]}")
    else:
        print("\n⚠ Payments table does not exist. Creating...")
        
        # Create payments table
        create_sql = """
        CREATE TABLE payments (
            id SERIAL PRIMARY KEY,
            member_id INTEGER NOT NULL REFERENCES members(id) ON DELETE CASCADE,
            order_id VARCHAR(100) UNIQUE NOT NULL,
            amount NUMERIC(12, 2) NOT NULL,
            payment_method VARCHAR(50),
            status VARCHAR(20) DEFAULT 'pending',
            membership_plan VARCHAR(50) NOT NULL,
            duration_days INTEGER DEFAULT 30,
            transaction_id VARCHAR(100),
            payment_url VARCHAR(500),
            va_number VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            paid_at TIMESTAMP,
            expired_at TIMESTAMP
        );

        CREATE INDEX ix_payments_order_id ON payments(order_id);
        CREATE INDEX ix_payments_member_id ON payments(member_id);
        CREATE INDEX ix_payments_status ON payments(status);
        """
        conn.execute(text(create_sql))
        conn.commit()
        print("✓ Payments table created successfully!")

print("\n" + "=" * 50)
print("Database setup complete!")
print("=" * 50)
