"""
Display trainer login credentials using direct SQL
"""
import psycopg2

# Database connection
conn = psycopg2.connect(
    dbname="gym_booking_db",
    user="postgres",
    password="123140197",
    host="localhost"
)

cursor = conn.cursor()

print("\n" + "=" * 60)
print("TRAINER LOGIN CREDENTIALS")
print("=" * 60)

# Query trainers
cursor.execute("""
    SELECT id, name, email, role 
    FROM users 
    WHERE role = 'TRAINER'
    ORDER BY name
""")

trainers = cursor.fetchall()

if trainers:
    for trainer in trainers:
        trainer_id, name, email, role = trainer
        print(f"\nTrainer: {name}")
        print(f"Email: {email}")
        print(f"Password: trainer123")
        print("-" * 60)
        
        # Get classes taught by this trainer
        cursor.execute("""
            SELECT c.id, c.name, c.schedule, c.capacity,
                   COUNT(b.id) as enrolled_count
            FROM classes c
            LEFT JOIN bookings b ON c.id = b.class_id
            WHERE c.trainer_id = %s
            GROUP BY c.id, c.name, c.schedule, c.capacity
            ORDER BY c.schedule
        """, (trainer_id,))
        
        classes = cursor.fetchall()
        if classes:
            print(f"Kelas yang diajar:")
            for cls in classes:
                class_id, class_name, schedule, capacity, enrolled = cls
                print(f"  - {class_name} ({enrolled}/{capacity} member)")
        else:
            print("Belum ada kelas yang ditugaskan")
else:
    print("\nNo trainers found in database")

print("\n" + "=" * 60)
print(f"Total Trainers: {len(trainers)}")
print("=" * 60 + "\n")

cursor.close()
conn.close()
