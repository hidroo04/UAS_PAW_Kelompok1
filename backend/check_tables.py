import psycopg2

conn = psycopg2.connect(
    dbname="gym_booking_db",
    user="postgres",
    password="123140197",
    host="localhost"
)

cursor = conn.cursor()
cursor.execute("""
    SELECT tablename 
    FROM pg_tables 
    WHERE schemaname='public' 
    ORDER BY tablename
""")

print("\nDatabase Tables:")
for row in cursor.fetchall():
    print(f"  - {row[0]}")

conn.close()
