# FitZone Gym Booking System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Pyramid](https://img.shields.io/badge/Pyramid-2.0+-red.svg)](https://trypyramid.com/)
[![React](https://img.shields.io/badge/React-18.2+-61DAFB.svg)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791.svg)](https://www.postgresql.org/)

Modern, professional gym class booking system with user authentication, class management, attendance tracking, and reviews. Built with Pyramid (Python) backend and React frontend.

**UAS Pemrograman Aplikasi Web - Kelompok 1**

## 🏋️ Features

### Core Features
- **User Authentication**: JWT-based authentication with role management (Admin, Trainer, Member)
- **Class Management**: Create, update, and manage gym classes with types and difficulty levels
- **Advanced Search & Filters**: Search classes by name, filter by type, difficulty, and date
- **Booking System**: Easy class booking with capacity management
- **Attendance Tracking**: Track member attendance for each class
- **Membership Management**: Different membership plans with feature comparison
- **User Profiles**: Comprehensive user profile with bookings, attendance, and membership info
- **Reviews & Ratings**: Rate and review classes (1.0-5.0 stars)

### Design Features
- Modern gym-themed color palette (Orange & Dark theme)
- Fully responsive design (mobile, tablet, desktop)
- Smooth animations with AOS (Animate On Scroll)
- Professional UI components with React Icons
- Optimized user experience with loading states
- Filter-based class browsing
- Interactive membership plan cards

## 🆕 What's New in v2.0

- ⭐ **Reviews & Ratings System**: Rate and review classes after attendance
- 🔍 **Enhanced Class Filtering**: Search by name, filter by type, difficulty, and date
- 👤 **User Profile Management**: Comprehensive profile with tabs for bookings, attendance, and membership
- 💳 **Membership Plans Page**: Visual comparison of membership tiers
- 🎨 **Improved UI/UX**: Better navigation, responsive filters, and professional design
- 📊 **Class Statistics**: Average ratings, available slots, and booking counts
- 🗂️ **Better Navigation**: Added Profile and Membership links to navbar

## 📁 Project Structure

```
UAS_PAW_Kelompok1/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Application factory
│   │   ├── config.py            # Configuration management
│   │   ├── models/              # Database models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── member.py
│   │   │   ├── gym_class.py
│   │   │   ├── gym_class_enhanced.py  # Enhanced with types & difficulty
│   │   │   ├── booking.py
│   │   │   ├── attendance.py
│   │   │   └── review.py        # NEW: Review model
│   │   ├── routes/              # Modular route definitions
│   │   │   ├── __init__.py
│   │   │   ├── auth_routes.py
│   │   │   ├── class_routes.py
│   │   │   ├── booking_routes.py
│   │   │   ├── attendance_routes.py
│   │   │   ├── membership_routes.py
│   │   │   └── review_routes.py  # NEW: Review routes
│   │   ├── views/               # View handlers
│   │   │   ├── auth_views.py
│   │   │   ├── class_views.py
│   │   │   ├── class_views_enhanced.py  # Enhanced with filters
│   │   │   ├── booking_views.py
│   │   │   ├── attendance_views.py
│   │   │   ├── membership_views.py
│   │   │   └── review_views.py   # NEW: Review views
│   │   └── utils/               # Utility functions
│   │       └── auth.py          # JWT and authentication helpers
│   ├── alembic/                 # Database migrations
│   │   └── versions/
│   │       ├── 001_initial.py
│   │       └── 002_add_enhancements.py  # NEW: Reviews & enhancements
│   ├── .env                     # Environment variables
│   ├── .env.example             # Environment template
│   ├── requirements.txt         # Python dependencies
│   ├── development.ini          # Development configuration
│   ├── init_db.py              # Database initialization
│   └── seed_data.py            # Sample data seeding
├── frontend/
│   ├── src/
│   │   ├── components/         # Reusable components
│   │   │   ├── Navbar.jsx      # Updated with Profile & Membership links
│   │   │   ├── Footer.jsx
│   │   │   ├── ClassCard.jsx
│   │   │   ├── BookingCard.jsx
│   │   │   └── Loading.jsx
│   │   ├── pages/              # Page components
│   │   │   ├── Home.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Classes.jsx      # Enhanced with search & filters
│   │   │   ├── MyBookings.jsx
│   │   │   ├── UserProfile.jsx  # NEW: User profile with tabs
│   │   │   └── MembershipPlans.jsx  # NEW: Membership plans
│   │   ├── services/           # API services
│   │   │   └── api.js
│   │   ├── App.jsx             # Main app component
│   │   └── index.jsx           # Entry point
│   ├── package.json
│   └── vite.config.js
└── FitZone_Gym_API.postman_collection.json  # Postman API collection
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- PostgreSQL 13 or higher
- Git

### Backend Setup

   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**
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
   ```

4. **Configure PostgreSQL Database**
   
   Create a PostgreSQL database:
   ```sql
   CREATE DATABASE gym_booking_db;
   CREATE USER postgres WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE gym_booking_db TO postgres;
   ```

5. **Configure environment variables**
   ```bash
   # Copy .env.example to .env
   cp .env.example .env
   
   # Edit .env with your database credentials
   # DATABASE_URL=postgresql://username:password@localhost/gym_booking_db
   # JWT_SECRET_KEY=your-strong-secret-key
   ```

6. **Initialize database**
   ```bash
   # Run database initialization
   python init_db.py
   
   # (Optional) Seed sample data
   python seed_data.py
   ```

7. **Start the backend server**
   ```bash
   pserve development.ini
   ```
   
   Backend will run on `http://localhost:6543`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```
   
   Frontend will run on `http://localhost:5173`

## 🧪 API Testing with Postman

1. **Import Postman Collection**
   - Open Postman
   - Click "Import"
   - Select `FitZone_Gym_API.postman_collection.json`

2. **Set up environment**
   - After successful login, copy the JWT token
   - Set it as the `token` variable in Postman

3. **Available Endpoints**
   - **Authentication**: Register, Login, Get Profile
   - **Classes**: CRUD operations for gym classes
   - **Bookings**: Create and manage class bookings
   - **Attendance**: Track class attendance
   - **Membership**: Manage membership plans

## 📊 Database Schema

### Main Tables:
- **users**: User accounts with authentication
- **members**: Member profiles with membership details
- **gym_classes**: Available gym classes
- **bookings**: Class bookings by members
- **attendance**: Attendance records for classes

## 🔐 Authentication

The system uses JWT (JSON Web Tokens) for authentication:

1. **Register** or **Login** to receive a JWT token
2. Include the token in the `Authorization` header for protected routes:
   ```
   Authorization: Bearer <your-jwt-token>
   ```

### User Roles:
- **MEMBER**: Can book classes, view bookings, track attendance
- **TRAINER**: Can manage classes, mark attendance
- **ADMIN**: Full access to all features

## 🎨 Frontend Technologies

- **React 18**: Modern React with hooks
- **React Router**: Client-side routing
- **Axios**: HTTP client for API calls
- **AOS**: Animate On Scroll library
- **React Icons**: Icon library
- **Vite**: Fast build tool and dev server

## 🛠️ Backend Technologies

- **Pyramid**: Python web framework
- **SQLAlchemy**: ORM for database operations
- **Alembic**: Database migration tool
- **PostgreSQL**: Relational database
- **PyJWT**: JWT token handling
- **Python-dotenv**: Environment variable management

## 📝 Environment Variables

Create a `.env` file in the backend directory:

```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost/gym_booking_db

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Application
APP_ENV=development
DEBUG=True

# Server
HOST=localhost
PORT=6543
```

## 🐛 Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Verify database credentials in `.env`
- Check if the database exists

### Port Already in Use
- Backend: Change port in `development.ini`
- Frontend: Vite will automatically use next available port

### Module Not Found
- Backend: Ensure virtual environment is activated
- Frontend: Run `npm install` again

## 👥 Team - Kelompok 1

UAS Pemrograman Aplikasi Web

## 📄 License

This project is for educational purposes.

---

**Happy Coding! 💪🏋️‍♂️**

```sql
CREATE DATABASE uas_pengweb_db;
```

6. Update `development.ini` with your database credentials

7. Run migrations:

```bash
alembic upgrade head
```

8. Run development server:

```bash
pserve development.ini --reload
```

Backend will run on `http://localhost:6543`

## 📝 Development Guidelines

- **Frontend**: Gunakan CSS murni (wajib CPMK0501), boleh tambah Tailwind/Bootstrap
- **Backend**: Gunakan Pyramid Framework dengan SQLAlchemy ORM
- **Database**: Harus PostgreSQL (wajib)
- **API**: RESTful API dengan JSON response

## 🚢 Deployment

- **Frontend**: Deploy ke Vercel
- **Backend**: Deploy ke domain \*.web.id (Niagahoster/Rumahweb)

## 📄 License

Copyright © 2025 UAS Pengweb
