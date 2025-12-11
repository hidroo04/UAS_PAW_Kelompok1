# Backend - Python Pyramid

Backend API menggunakan Python 3.x dengan Pyramid Framework untuk GymBook - Gym Class Booking System.

## 🚀 Technology Stack

- Python 3.x
- Pyramid Framework
- SQLAlchemy ORM
- Alembic (migrations)
- PostgreSQL
- PyJWT (Authentication)
- Waitress (WSGI Server)

## 📦 Installation

1. Create virtual environment:

```bash
python -m venv venv
```

2. Activate virtual environment:

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Install package in development mode:

```bash
pip install -e .
```

## 🗄️ Database Setup

### Quick Setup (Recommended)

```bash
# Run database initialization script
python init_db.py
```

This will create all tables and optionally add sample data.

### Manual Setup

See [DATABASE_SETUP.md](DATABASE_SETUP.md) for detailed PostgreSQL integration guide.

**Quick Steps:**

1. Create PostgreSQL database:

```sql
CREATE DATABASE gym_booking_db;
```

2. Update database URL in `development.ini`:

```ini
sqlalchemy.url = postgresql://postgres:password@localhost/gym_booking_db
```

3. Run initialization:

```bash
python init_db.py
```

## 🏃 Development

Run the development server:

```bash
pserve development.ini --reload
```

Server akan berjalan di `http://localhost:6543`

## 📁 Project Structure

```
app/
├── models/                 # Database models (SQLAlchemy)
│   ├── __init__.py        # Models initialization
│   ├── user.py            # User model (admin, trainer, member)
│   ├── member.py          # Member/Membership model
│   ├── gym_class.py       # Class model
│   ├── booking.py         # Booking model
│   └── attendance.py      # Attendance model
├── views/                 # API endpoints/routes
│   ├── __init__.py        # Error handlers
│   ├── auth_views.py      # Authentication (login, register)
│   ├── class_views.py     # Class management CRUD
│   ├── booking_views.py   # Booking operations
│   ├── attendance_views.py # Attendance tracking
│   └── membership_views.py # Membership management
├── __init__.py            # App initialization & routes
└── routes.py              # Route definitions
alembic/                   # Database migrations
init_db.py                 # Database setup script
DATABASE_SETUP.md          # PostgreSQL integration guide
```

## 🔌 API Endpoints

### Authentication

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user info

### Classes (Trainer & Member)

- `GET /api/classes` - Get all classes
- `POST /api/classes` - Create new class (Trainer only)
- `GET /api/classes/{id}` - Get class by ID
- `PUT /api/classes/{id}` - Update class (Trainer only)
- `DELETE /api/classes/{id}` - Delete class (Trainer only)
- `GET /api/classes/{id}/participants` - Get class participants (Trainer only)

### Bookings (Member)

- `GET /api/bookings` - Get all bookings
- `POST /api/bookings` - Create booking (Member only)
- `GET /api/bookings/{id}` - Get booking by ID
- `DELETE /api/bookings/{id}` - Cancel booking
- `GET /api/bookings/my` - Get current user's bookings

### Attendance (Trainer)

- `GET /api/attendance` - Get all attendance records
- `POST /api/attendance` - Mark attendance (Trainer only)
- `GET /api/attendance/my` - Get current member's attendance

### Membership

- `GET /api/membership/plans` - Get available membership plans
- `GET /api/membership/my` - Get current user's membership
- `GET /api/members` - Get all members (Admin only)
- `POST /api/members` - Create/Update membership (Admin only)

## 🔐 Authentication

API menggunakan JWT (JSON Web Token) untuk authentication.

**Login Request:**

```json
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**

```json
{
  "status": "success",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "data": {
    "id": 1,
    "name": "User Name",
    "email": "user@example.com",
    "role": "member"
  }
}
```

**Using Token:**

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## 👥 User Roles

1. **Admin** - Manage membership plans and users
2. **Trainer** - Create/manage classes, mark attendance
3. **Member** - Book classes, view bookings

## 🧪 Testing

Sample credentials (if you added sample data):

- Admin: `admin@gymbook.com` / `admin123`
- Trainer: `trainer@gymbook.com` / `trainer123`
- Member: `member@gymbook.com` / `member123`

## 📊 Database Models

- **Users** - User accounts with roles
- **Members** - Membership information
- **Classes** - Gym class schedules
- **Bookings** - Class bookings
- **Attendance** - Attendance tracking

See models in `app/models/` for detailed schema.
