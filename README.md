# 🏋️ Hydroo Gym - Sistem Manajemen Gym

Sistem manajemen gym yang komprehensif dengan fitur booking kelas, manajemen membership, dan tracking attendance untuk member, trainer, dan admin.

## 👥 Tim Pengembang - Kelompok 1

| Nama | NIM | Role |
|------|-----|------|
| Ripaldy Saputra Lumbantoruan | 123140179 | Backend Developer |
| Mega Zayyani | 123140180 | Frontend Developer |
| Gilang Surya Agung | 123140187 | Backend Developer |
| Maxavier Girvanus Manurung | 123140191 | Frontend Developer |
| Muhammad Rafiq Ridho | 123140197 | Database Administrator |

### Pembagian Tugas
- **Backend Development**: Ripaldy Saputra Lumbantoruan, Gilang Surya Agung
  - API development dengan Pyramid Framework
  - Database modeling dan migrations
  - Authentication & authorization
  - Business logic implementation
  
- **Frontend Development**: Mega Zayani, Maxavier Girvanus Manurung
  - React component development
  - UI/UX implementation
  - State management
  - API integration
  
- **Database Administration**: Muhammad Rafiq Ridho
  - Database schema design
  - Data migration
  - Query optimization
  - Database backup & maintenance

## 📖 Deskripsi Project

Hydroo Gym adalah aplikasi web full-stack untuk manajemen gym yang memungkinkan member untuk booking kelas, mengelola membership, dan tracking progress fitness mereka. Aplikasi ini menyediakan dashboard khusus untuk admin, trainer, dan member dengan fitur yang disesuaikan untuk setiap role.

### Fitur Utama

#### 🔐 Authentication & Authorization
- Registrasi dan login user dengan JWT authentication
- Role-based access control (Admin, Trainer, Member)
- Secure password hashing dengan bcrypt
- Session management

#### 👤 Member Features
- Browse dan booking kelas gym
- View jadwal kelas dan trainer
- Membership plan management
- Payment processing dan history
- Personal profile management
- Booking history dan status tracking
- Review dan rating untuk kelas

#### 🏃 Trainer Features
- Dashboard untuk manage kelas
- View enrolled members per kelas
- Schedule management
- Attendance tracking untuk member
- Class capacity monitoring
- Calendar view untuk jadwal mengajar

#### 👨‍💼 Admin Features
- Dashboard dengan analytics dan statistics
  - Total members, classes, bookings, revenue
  - Booking growth tracking
  - Active day monitoring
  - Class capacity utilization
- Member management (CRUD operations)
- Class management (create, update, delete)
- Trainer assignment
- Attendance tracking dan reporting
- Membership plan configuration
- Payment verification dan monitoring
- Review moderation

#### 💳 Payment System
- Multiple membership plans (Basic, Premium, VIP)
- Secure payment processing
- Payment history tracking
- Monthly revenue reporting
- Payment verification system

#### 📊 Analytics & Reporting
- Real-time dashboard statistics
- Booking trends analysis
- Revenue tracking
- Member activity monitoring
- Class popularity metrics

## 🛠️ Tech Stack

### Backend
- **Framework**: Python Pyramid 2.0.2
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0.23
- **Migration**: Alembic 1.13.1
- **Authentication**: PyJWT 2.8.0
- **Password Hashing**: bcrypt 4.1.2, passlib 1.7.4
- **CORS**: Cornice 6.1.0
- **Server**: Waitress 2.1.2 (WSGI Server)
- **Transaction Management**: pyramid_tm, zope.sqlalchemy

### Frontend
- **Framework**: React 18.2.0
- **Build Tool**: Vite 5.0.8
- **Routing**: React Router DOM 6.20.0
- **HTTP Client**: Axios 1.6.2
- **Icons**: React Icons 4.12.0
- **Animations**: AOS 2.3.4
- **Styling**: CSS3 dengan custom styling

### Database
- **PostgreSQL** (Production & Development)
- Database migrations dengan Alembic
- Relational data model dengan foreign keys
- Transaction support

### DevOps & Deployment
- **Backend Hosting**: Railway/Neon PostgreSQL
- **Frontend Hosting**: Vercel
- **Version Control**: Git & GitHub
- **API Testing**: Postman

## 🚀 Cara Instalasi dan Menjalankan

### Prerequisites
- Python 3.9 atau lebih tinggi
- Node.js 16.x atau lebih tinggi
- PostgreSQL 12 atau lebih tinggi
- Git

### Backend Setup

1. **Clone repository**
```bash
git clone https://github.com/hidroo04/UAS_PAW_Kelompok1.git
cd UAS_PAW_Kelompok1/backend
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
pip install -e .
```

4. **Setup database**
```bash
# Create PostgreSQL database
createdb gymdb

# Atau menggunakan psql
psql -U postgres
CREATE DATABASE gymdb;
\q
```

5. **Configure environment variables**
```bash
# Buat file .env di folder backend
cp .env.example .env

# Edit .env dengan konfigurasi database Anda
DATABASE_URL=postgresql://username:password@localhost/gymdb
JWT_SECRET=your-secret-key-here
```

6. **Run database migrations**
```bash
# Initialize database dengan schema
alembic upgrade head

# Atau gunakan script initialization
python init_db.py
```

7. **Seed database (optional)**
```bash
# Populate database dengan sample data
python seed_data.py
python seed_payments.py
```

8. **Run development server**
```bash
# Menggunakan pserve (development)
pserve development.ini --reload

# Server akan berjalan di http://localhost:6543
```

### Frontend Setup

1. **Navigate ke folder frontend**
```bash
cd ../frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment variables**
```bash
# Buat file .env di folder frontend
# Tambahkan URL backend API
VITE_API_URL=http://localhost:6543/api
```

4. **Run development server**
```bash
npm run dev

# Server akan berjalan di http://localhost:5173
```

5. **Build for production**
```bash
npm run build
```

### Quick Start dengan Sample Data

Untuk testing cepat dengan data sample:

```bash
# Backend
cd backend
python seed_data.py

# Sample credentials:
# Admin: admin@gym.com / admin123
# Trainer: john.trainer@gym.com / trainer123
# Member: alice@member.com / member123
```

## 🔗 Link Deployment

### Frontend
**URL**: [https://your-frontend-url.vercel.app](https://your-frontend-url.vercel.app)
- Deployed on Vercel
- Automatic deployments from main branch

### Backend
**API URL**: [https://your-backend-url.railway.app](https://your-backend-url.railway.app)
- Deployed on Railway
- PostgreSQL database hosted on Neon
- Environment variables configured in Railway dashboard

## 📚 API Documentation

Base URL: `http://localhost:6543/api` (Development) atau deployment URL

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "string",
  "email": "string",
  "password": "string",
  "full_name": "string",
  "role": "member|trainer|admin"
}

Response 201:
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "string",
    "email": "string",
    "role": "member"
  }
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "string",
  "password": "string"
}

Response 200:
{
  "token": "jwt_token_here",
  "user": {
    "id": 1,
    "username": "string",
    "email": "string",
    "role": "member"
  }
}
```

### Class Endpoints

#### Get All Classes
```http
GET /api/classes
Authorization: Bearer {token}

Response 200:
{
  "classes": [
    {
      "id": 1,
      "name": "Morning Yoga",
      "description": "Relaxing morning yoga session",
      "trainer_name": "John Smith",
      "schedule": "2025-12-20T08:00:00",
      "duration": 60,
      "capacity": 15,
      "enrolled_count": 5,
      "price": 50000
    }
  ]
}
```

#### Get Class Details
```http
GET /api/classes/{class_id}
Authorization: Bearer {token}

Response 200:
{
  "id": 1,
  "name": "Morning Yoga",
  "description": "Relaxing morning yoga session",
  "trainer": {
    "id": 2,
    "name": "John Smith",
    "specialization": "Yoga"
  },
  "schedule": "2025-12-20T08:00:00",
  "duration": 60,
  "capacity": 15,
  "enrolled_count": 5,
  "price": 50000
}
```

#### Create Class (Admin/Trainer)
```http
POST /api/classes
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "string",
  "description": "string",
  "trainer_id": 2,
  "schedule": "2025-12-20T08:00:00",
  "duration": 60,
  "capacity": 15,
  "price": 50000
}

Response 201:
{
  "message": "Class created successfully",
  "class": { ... }
}
```

#### Update Class (Admin/Trainer)
```http
PUT /api/classes/{class_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "string",
  "description": "string",
  "schedule": "2025-12-20T08:00:00",
  "capacity": 20
}

Response 200:
{
  "message": "Class updated successfully",
  "class": { ... }
}
```

#### Delete Class (Admin)
```http
DELETE /api/classes/{class_id}
Authorization: Bearer {token}

Response 200:
{
  "message": "Class deleted successfully"
}
```

### Booking Endpoints

#### Create Booking
```http
POST /api/bookings
Authorization: Bearer {token}
Content-Type: application/json

{
  "class_id": 1
}

Response 201:
{
  "message": "Booking created successfully",
  "booking": {
    "id": 1,
    "class_id": 1,
    "user_id": 3,
    "status": "confirmed",
    "booking_date": "2025-12-19T10:00:00"
  }
}
```

#### Get User Bookings
```http
GET /api/bookings/my-bookings
Authorization: Bearer {token}

Response 200:
{
  "bookings": [
    {
      "id": 1,
      "class_name": "Morning Yoga",
      "trainer_name": "John Smith",
      "schedule": "2025-12-20T08:00:00",
      "status": "confirmed"
    }
  ]
}
```

#### Cancel Booking
```http
DELETE /api/bookings/{booking_id}
Authorization: Bearer {token}

Response 200:
{
  "message": "Booking cancelled successfully"
}
```

#### Get All Bookings (Admin)
```http
GET /api/admin/bookings
Authorization: Bearer {token}

Response 200:
{
  "bookings": [
    {
      "id": 1,
      "user_name": "Diana Lee",
      "class_name": "Morning Yoga",
      "status": "confirmed",
      "booking_date": "2025-12-19T10:00:00"
    }
  ]
}
```

### Membership Endpoints

#### Get Membership Plans
```http
GET /api/memberships/plans
Authorization: Bearer {token}

Response 200:
{
  "plans": [
    {
      "id": 1,
      "name": "Basic",
      "price": 300000,
      "duration_days": 30,
      "features": ["Access to gym", "2 classes per week"]
    },
    {
      "id": 2,
      "name": "Premium",
      "price": 500000,
      "duration_days": 30,
      "features": ["Unlimited gym access", "Unlimited classes", "1 PT session"]
    }
  ]
}
```

#### Subscribe to Plan
```http
POST /api/memberships/subscribe
Authorization: Bearer {token}
Content-Type: application/json

{
  "plan_id": 2
}

Response 201:
{
  "message": "Membership activated successfully",
  "membership": {
    "plan_name": "Premium",
    "start_date": "2025-12-19",
    "end_date": "2026-01-19",
    "status": "active"
  }
}
```

### Payment Endpoints

#### Create Payment
```http
POST /api/payments
Authorization: Bearer {token}
Content-Type: application/json

{
  "membership_id": 1,
  "amount": 500000,
  "payment_method": "bank_transfer"
}

Response 201:
{
  "message": "Payment created successfully",
  "payment": {
    "id": 1,
    "amount": 500000,
    "status": "pending",
    "payment_date": "2025-12-19"
  }
}
```

#### Get Payment History
```http
GET /api/payments/history
Authorization: Bearer {token}

Response 200:
{
  "payments": [
    {
      "id": 1,
      "amount": 500000,
      "status": "completed",
      "payment_method": "bank_transfer",
      "payment_date": "2025-12-19"
    }
  ]
}
```

#### Verify Payment (Admin)
```http
PUT /api/admin/payments/{payment_id}/verify
Authorization: Bearer {token}

Response 200:
{
  "message": "Payment verified successfully"
}
```

### Attendance Endpoints

#### Mark Attendance (Trainer/Admin)
```http
POST /api/attendance
Authorization: Bearer {token}
Content-Type: application/json

{
  "class_id": 1,
  "user_id": 3,
  "status": "present"
}

Response 201:
{
  "message": "Attendance marked successfully"
}
```

#### Get Attendance Report
```http
GET /api/attendance/class/{class_id}
Authorization: Bearer {token}

Response 200:
{
  "attendance": [
    {
      "user_name": "Diana Lee",
      "status": "present",
      "check_in_time": "2025-12-20T08:05:00"
    }
  ]
}
```

### Review Endpoints

#### Create Review
```http
POST /api/reviews
Authorization: Bearer {token}
Content-Type: application/json

{
  "class_id": 1,
  "rating": 5,
  "comment": "Excellent class!"
}

Response 201:
{
  "message": "Review submitted successfully",
  "review": {
    "id": 1,
    "rating": 5,
    "comment": "Excellent class!"
  }
}
```

#### Get Class Reviews
```http
GET /api/reviews/class/{class_id}

Response 200:
{
  "reviews": [
    {
      "id": 1,
      "user_name": "Diana Lee",
      "rating": 5,
      "comment": "Excellent class!",
      "created_at": "2025-12-19"
    }
  ]
}
```

### User Profile Endpoints

#### Get Profile
```http
GET /api/users/profile
Authorization: Bearer {token}

Response 200:
{
  "id": 1,
  "username": "diana_lee",
  "email": "diana@gym.com",
  "full_name": "Diana Lee",
  "role": "member",
  "membership_status": "active"
}
```

#### Update Profile
```http
PUT /api/users/profile
Authorization: Bearer {token}
Content-Type: application/json

{
  "full_name": "Diana Lee Updated",
  "phone": "081234567890"
}

Response 200:
{
  "message": "Profile updated successfully",
  "user": { ... }
}
```

### Admin Dashboard Endpoints

#### Get Dashboard Statistics
```http
GET /api/admin/dashboard/stats
Authorization: Bearer {token}

Response 200:
{
  "total_members": 14,
  "active_members": 13,
  "total_classes": 11,
  "total_bookings": 17,
  "total_trainers": 7,
  "upcoming_classes": 8,
  "monthly_revenue": 3100000,
  "booking_growth": -11.1,
  "most_active_day": "Tuesday",
  "class_capacity": 7.7,
  "total_users": 22,
  "avg_bookings": 1.5
}
```

### Error Responses

Semua endpoint dapat mengembalikan error responses berikut:

```http
# Unauthorized
401 Unauthorized
{
  "error": "Authentication required"
}

# Forbidden
403 Forbidden
{
  "error": "Permission denied"
}

# Not Found
404 Not Found
{
  "error": "Resource not found"
}

# Bad Request
400 Bad Request
{
  "error": "Validation error",
  "details": {
    "field": "error message"
  }
}

# Server Error
500 Internal Server Error
{
  "error": "Internal server error"
}
```

## 📸 Screenshot Aplikasi

### 1. Landing Page
![Landing Page](Screenshots/landing-page.png)
Halaman utama aplikasi dengan hero section dan call-to-action untuk browse classes dan join membership.

### 2. Home Page - Member Dashboard
![Home Page](Screenshots/dashboard-member.png)
Dashboard member yang menampilkan class browser, membership options, dan personal booking information.

### 3. Admin Dashboard
![Admin Dashboard](Screenshots/dashboard-admin.png)
Admin dashboard dengan comprehensive analytics termasuk total members (14), classes (11), bookings (17), trainers (7), monthly revenue (Rp 3.1M), booking growth tracking, dan metrics lainnya seperti most active day dan class capacity utilization.

### 4. Trainer Dashboard - My Classes
![Trainer Dashboard](Screenshots/dashboard-trainer.png)
Dashboard trainer untuk manage classes dengan informasi member enrollment, available slots, dan schedule management. Menampilkan kelas seperti "Yogaa class" dan "Morning yoga" dengan detail jadwal dan kapasitas.

## 🎥 Video Presentasi

Link video presentasi: [https://youtu.be/FjyNafPpfNs](https://youtu.be/FjyNafPpfNs)

## 📋 Project Structure

```
UAS_PAW_Kelompok1/
├── backend/                    # Python Pyramid Backend
│   ├── app/
│   │   ├── models/            # SQLAlchemy models
│   │   ├── views/             # API view handlers
│   │   ├── routes/            # Route configurations
│   │   └── utils/             # Utility functions (auth, etc.)
│   ├── alembic/               # Database migrations
│   ├── requirements.txt       # Python dependencies
│   └── development.ini        # Pyramid configuration
│
├── frontend/                  # React Frontend
│   ├── src/
│   │   ├── components/       # Reusable components
│   │   ├── pages/            # Page components
│   │   │   ├── admin/        # Admin dashboard pages
│   │   │   └── trainer/      # Trainer dashboard pages
│   │   ├── services/         # API service layer
│   │   └── App.jsx           # Main app component
│   ├── package.json          # Node dependencies
│   └── vite.config.js        # Vite configuration
│
└── README.md                 # This file
```

## 🔐 Default Users untuk Testing

Setelah menjalankan seed data, gunakan credentials berikut:

| Role | Nama | Email | Password |
|------|------|-------|----------|
| Admin | Admin User | admin@gym.com | admin123 |
| Trainer | John Smith | john.trainer@gym.com | trainer123 |
| Trainer | Sarah Johnson | sarah.trainer@gym.com | trainer123 |
| Trainer | Mike Chen | mike.trainer@gym.com | trainer123 |
| Trainer | Emily Davis | emily.trainer@gym.com | trainer123 |
| Member | Alice Brown | alice@member.com | member123 |
| Member | Bob Wilson | bob@member.com | member123 |
| Member | Charlie Martinez | charlie@member.com | member123 |
| Member | Diana Lee | diana@member.com | member123 |
| Member | Ethan Taylor | ethan@member.com | member123 |
| Member | Fiona Anderson | fiona@member.com | member123 |
| Member | George Thomas | george@member.com | member123 |
| Member | Hannah White | hannah@member.com | member123 |
| Member | Ian Harris | ian@member.com | member123 |
| Member | Julia Clark | julia@member.com | member123 |


