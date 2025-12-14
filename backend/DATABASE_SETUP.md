# PostgreSQL Integration Guide

## Prerequisites

1. **Install PostgreSQL**

   - Download from: https://www.postgresql.org/download/
   - Or use Docker: `docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=password postgres`

2. **Create Database**

```sql
-- Login to PostgreSQL
psql -U postgres

-- Create database
CREATE DATABASE gym_booking_db;

-- Create user (optional)
CREATE USER gymbook_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE gym_booking_db TO gymbook_user;
```

## Configuration

### 1. Update `development.ini`

Edit `backend/development.ini` and update the database URL:

```ini
sqlalchemy.url = postgresql://postgres:password@localhost/gym_booking_db
```

Replace with your credentials:

- `postgres` - your PostgreSQL username
- `password` - your PostgreSQL password
- `localhost` - your PostgreSQL host
- `gym_booking_db` - your database name

### 2. Update `alembic.ini`

Edit `backend/alembic.ini` and update the database URL:

```ini
sqlalchemy.url = postgresql://postgres:password@localhost/gym_booking_db
```

## Database Initialization

### Option 1: Using init_db.py (Recommended for Quick Start)

```bash
# Activate virtual environment
.venv\Scripts\activate

# Navigate to backend directory
cd backend

# Run initialization script
python init_db.py

# Or with custom database URL
python init_db.py postgresql://user:pass@localhost/dbname
```

This will:

- Create all tables (users, members, classes, bookings, attendance)
- Optionally add sample data for testing

### Option 2: Using Alembic Migrations (Production Ready)

```bash
# Activate virtual environment
.venv\Scripts\activate

# Navigate to backend directory
cd backend

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

## Database Schema

### Tables Created:

1. **users**

   - id (Primary Key)
   - name
   - email (Unique)
   - password (Hashed)
   - role (admin, trainer, member)
   - created_at, updated_at

2. **members**

   - id (Primary Key)
   - user_id (Foreign Key → users.id)
   - membership_plan (Basic, Premium, VIP)
   - expiry_date

3. **classes**

   - id (Primary Key)
   - trainer_id (Foreign Key → users.id)
   - name
   - description
   - schedule
   - capacity
   - created_at

4. **bookings**

   - id (Primary Key)
   - member_id (Foreign Key → members.id)
   - class_id (Foreign Key → classes.id)
   - booking_date
   - Unique constraint: (member_id, class_id)

5. **attendance**
   - id (Primary Key)
   - booking_id (Foreign Key → bookings.id)
   - attended (Boolean)
   - date

## Verification

### Check Database Connection

```python
from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:password@localhost/gym_booking_db')
connection = engine.connect()
print("✅ Connected to database!")
connection.close()
```

### Check Tables

```sql
-- Connect to database
\c gym_booking_db

-- List all tables
\dt

-- View table structure
\d users
\d members
\d classes
\d bookings
\d attendance
```

## Running the Application

```bash
# Start backend server
pserve development.ini

# Or with reload
pserve development.ini --reload
```

## Sample Data

If you chose to add sample data, you can login with:

- **Admin**: admin@gymbook.com / admin123
- **Trainer**: trainer@gymbook.com / trainer123
- **Member**: member@gymbook.com / member123

## Troubleshooting

### Connection Error

```
psycopg2.OperationalError: FATAL: password authentication failed
```

**Solution**: Check your PostgreSQL credentials in configuration files

### Database Does Not Exist

```
psycopg2.OperationalError: FATAL: database "gym_booking_db" does not exist
```

**Solution**: Create the database first using `CREATE DATABASE gym_booking_db;`

### Port Already in Use

```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solution**: Check if PostgreSQL is running on port 5432

## Database Maintenance

### Backup Database

```bash
pg_dump -U postgres gym_booking_db > backup.sql
```

### Restore Database

```bash
psql -U postgres gym_booking_db < backup.sql
```

### Reset Database

```sql
DROP DATABASE gym_booking_db;
CREATE DATABASE gym_booking_db;
```

Then run `init_db.py` again or `alembic upgrade head`
