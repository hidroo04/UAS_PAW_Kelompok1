# Quick Start Guide - FitZone Gym Booking System

## 🚀 Get Started in 5 Minutes

### Prerequisites
- PostgreSQL 13+ installed and running
- Python 3.8+ with pip
- Node.js 16+ with npm
- Git (to clone the repository)

---

## ⚡ Quick Setup

### 1. Database Setup (2 minutes)

```bash
# Open PostgreSQL terminal (psql)
psql -U postgres

# Create database
CREATE DATABASE gym_booking_db;

# Exit psql
\q
```

---

### 2. Backend Setup (2 minutes)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
.\venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Edit .env file with your PostgreSQL credentials:
# DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost/gym_booking_db
# JWT_SECRET_KEY=your-super-secret-key-change-this-in-production

# Run database migrations
alembic upgrade head

# (Optional) Seed sample data
python seed_data.py

# Start backend server
pserve development.ini
```

**Backend now running at: http://localhost:6543** ✅

---

### 3. Frontend Setup (1 minute)

Open a **new terminal window**:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend now running at: http://localhost:5173** ✅

---

## 🎉 You're Ready!

Open your browser and visit:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:6543/api

---

## 🧪 Test the System

### Create Your First Account

1. Go to http://localhost:5173
2. Click "Join Now" in the navbar
3. Fill in registration form:
   - Name: Test User
   - Email: test@example.com
   - Password: password123
   - Role: MEMBER
4. Click Register
5. Login with your credentials

### Book Your First Class

1. Navigate to "Classes" page
2. Use search and filters to find a class
3. Click "Book Now" on any class
4. Go to "My Bookings" to see your booking

### Leave Your First Review

1. Go to a class you've booked
2. (Admin/Trainer) Mark your attendance
3. Return to the class page
4. Submit a review with rating and comment

### Explore Features

- **Search Classes**: Try searching for "yoga" or "HIIT"
- **Filter Classes**: Use type, difficulty, and date filters
- **View Profile**: Click "Profile" to see your information
- **Check Membership**: Visit "Membership" page to view plans

---

## 📱 Default Test Accounts

If you ran `seed_data.py`, use these accounts:

### Admin Account
- **Email**: admin@fitzone.com
- **Password**: admin123
- **Access**: Full system access

### Trainer Account
- **Email**: trainer@fitzone.com
- **Password**: trainer123
- **Access**: Manage classes, mark attendance

### Member Account
- **Email**: member@fitzone.com
- **Password**: member123
- **Access**: Book classes, leave reviews

---

## 🔧 Common Commands

### Backend

```bash
# Start server
pserve development.ini

# Run migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Create new migration
alembic revision -m "description"

# Seed data
python seed_data.py

# Initialize database
python init_db.py
```

### Frontend

```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

---

## 🗂️ Project Structure Overview

```
UAS_PAW_Kelompok1/
├── backend/
│   ├── app/              # Application code
│   ├── alembic/          # Database migrations
│   ├── .env              # Environment variables
│   └── development.ini   # Server configuration
├── frontend/
│   ├── src/              # React source code
│   │   ├── components/   # Reusable components
│   │   ├── pages/        # Page components
│   │   └── services/     # API services
│   └── package.json      # Dependencies
└── docs/                 # Documentation files
```

---

## 📚 Key Features to Try

### 🔍 Enhanced Search & Filtering
- Search classes by keyword
- Filter by type (Yoga, HIIT, Strength, etc.)
- Filter by difficulty (Beginner, Intermediate, Advanced)
- Filter by date
- Combine multiple filters

### ⭐ Reviews & Ratings
- Leave reviews after attending classes
- Rate classes from 1.0 to 5.0 stars
- Edit or delete your reviews
- View average ratings per class

### 👤 User Profile
- View and edit personal information
- See all your bookings
- Track attendance history
- Monitor membership status

### 💳 Membership Plans
- Compare different plans
- View detailed features
- Subscribe to plans
- Track membership expiration

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if PostgreSQL is running
# Windows: Services > PostgreSQL
# Linux: sudo systemctl status postgresql
# Mac: brew services list

# Check database exists
psql -U postgres -l | grep gym_booking_db

# Verify .env configuration
cat .env  # Linux/Mac
type .env # Windows
```

### Frontend won't start
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json  # Linux/Mac
rmdir /s node_modules                  # Windows
npm install

# Check Node version
node --version  # Should be 16+
```

### Database connection error
```bash
# Test PostgreSQL connection
psql -U postgres -d gym_booking_db -c "SELECT 1;"

# Check .env DATABASE_URL format:
# postgresql://username:password@host:port/database
```

### API calls failing
- Verify backend is running on port 6543
- Check `frontend/src/services/api.js` has correct base URL
- Open browser DevTools > Network tab to inspect requests

---

## 📖 Next Steps

### Learn More
- Read `FEATURES.md` for detailed feature documentation
- Check `API_REFERENCE.md` for API endpoint details
- Review `SETUP_GUIDE.md` for comprehensive setup instructions

### Test with Postman
- Import `FitZone_Gym_API.postman_collection.json`
- Set `token` variable after login
- Test all API endpoints

### Customize
- Update colors in `frontend/src/index.css`
- Add new class types in `backend/app/models/gym_class_enhanced.py`
- Modify membership plans in database

---

## 🎯 Development Workflow

### Making Changes

1. **Backend Changes**:
   ```bash
   cd backend
   # Edit Python files
   # Server auto-reloads with development.ini
   ```

2. **Frontend Changes**:
   ```bash
   cd frontend
   # Edit React components
   # Vite auto-reloads (Hot Module Replacement)
   ```

3. **Database Changes**:
   ```bash
   cd backend
   # Create migration
   alembic revision -m "add new field"
   # Edit migration file in alembic/versions/
   # Apply migration
   alembic upgrade head
   ```

### Git Workflow

```bash
# Check status
git status

# Add changes
git add .

# Commit
git commit -m "Add new feature"

# Push to repository
git push origin main
```

---

## 💡 Pro Tips

1. **Keep terminal windows open**: One for backend, one for frontend
2. **Use Postman**: Test API endpoints before frontend integration
3. **Check browser console**: Look for errors when debugging frontend
4. **Use database GUI**: Tools like pgAdmin, DBeaver for database inspection
5. **Read error messages**: They usually tell you exactly what's wrong

---

## 🆘 Need Help?

- **Setup Issues**: Check `SETUP_GUIDE.md`
- **API Questions**: Check `API_REFERENCE.md`
- **Feature Details**: Check `FEATURES.md`
- **Testing**: Check `TESTING_CHECKLIST.md`
- **Database**: Check `DATABASE_SETUP.md`

---

## 📞 Support

For issues or questions:
1. Check documentation files first
2. Review error messages carefully
3. Verify all prerequisites are met
4. Check database connection and credentials

---

## ✅ Quick Verification

Everything working if you can:
- ✅ Access frontend (http://localhost:5173)
- ✅ Access backend API (http://localhost:6543/api)
- ✅ Register new user
- ✅ Login successfully
- ✅ See classes list
- ✅ Book a class
- ✅ View profile
- ✅ See membership plans

---

**Happy Coding! 🚀**

**Version**: 2.0.0  
**Last Updated**: January 10, 2025
