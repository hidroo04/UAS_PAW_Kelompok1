"""
Check enum values in database
"""
import psycopg2

conn = psycopg2.connect(
    dbname="gym_booking_db",
    user="postgres",
    password="123140197",
    host="localhost"
)

cursor = conn.cursor()

# Check enum type values
cursor.execute("""
    SELECT enumlabel 
    FROM pg_enum 
    WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = 'userrole')
    ORDER BY enumsortorder
""")

print("\nValid UserRole enum values:")
for row in cursor.fetchall():
    print(f"  - {row[0]}")

# Check actual users in database
cursor.execute("""
    SELECT role, COUNT(*) as count
    FROM users
    GROUP BY role
    ORDER BY count DESC
""")

print("\nUsers by role in database:")
for row in cursor.fetchall():
    print(f"  - {row[0]}: {row[1]} users")

# Get some sample users
cursor.execute("""
    SELECT name, email, role
    FROM users
    LIMIT 10
""")

print("\nSample users:")
for row in cursor.fetchall():
    print(f"  - {row[0]} ({row[1]}) - Role: {row[2]}")

cursor.close()
conn.close()
