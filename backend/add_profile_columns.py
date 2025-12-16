import psycopg2
from psycopg2 import sql

# Database connection parameters
DB_PARAMS = {
    'host': 'localhost',
    'database': 'gym_booking_db',
    'user': 'postgres',
    'password': '123140197'
}

def add_profile_columns():
    """Add phone, address, and avatar_url columns to users table"""
    conn = None
    try:
        # Connect to database
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        
        print("Connected to database successfully!")
        
        # Check if columns already exist
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' 
            AND column_name IN ('phone', 'address', 'avatar_url')
        """)
        existing_columns = [row[0] for row in cur.fetchall()]
        
        # Add phone column if not exists
        if 'phone' not in existing_columns:
            cur.execute("""
                ALTER TABLE users 
                ADD COLUMN phone VARCHAR(20)
            """)
            print("✓ Added 'phone' column")
        else:
            print("- 'phone' column already exists")
        
        # Add address column if not exists
        if 'address' not in existing_columns:
            cur.execute("""
                ALTER TABLE users 
                ADD COLUMN address TEXT
            """)
            print("✓ Added 'address' column")
        else:
            print("- 'address' column already exists")
        
        # Add avatar_url column if not exists
        if 'avatar_url' not in existing_columns:
            cur.execute("""
                ALTER TABLE users 
                ADD COLUMN avatar_url VARCHAR(255)
            """)
            print("✓ Added 'avatar_url' column")
        else:
            print("- 'avatar_url' column already exists")
        
        # Commit changes
        conn.commit()
        print("\n✅ Database schema updated successfully!")
        
        # Verify columns
        cur.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'users' 
            ORDER BY ordinal_position
        """)
        
        print("\nCurrent users table structure:")
        print("-" * 40)
        for row in cur.fetchall():
            print(f"{row[0]:<20} {row[1]}")
        
        cur.close()
        
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        if conn:
            conn.rollback()
    
    finally:
        if conn:
            conn.close()
            print("\nDatabase connection closed.")

if __name__ == '__main__':
    add_profile_columns()
