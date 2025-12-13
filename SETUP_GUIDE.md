# FitZone Gym Booking System - Setup Guide

## Langkah-langkah Setup

### 1. Install Dependencies Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Konfigurasi Database PostgreSQL

1. Pastikan PostgreSQL sudah terinstall dan running
2. Buat database baru:
   ```sql
   CREATE DATABASE gym_booking_db;
   ```

3. Copy file `.env.example` menjadi `.env`:
   ```bash
   copy .env.example .env
   ```

4. Edit file `.env` dengan kredensial PostgreSQL Anda:
   ```
   DATABASE_URL=postgresql://postgres:ripaldy@localhost/gym_booking_db
   JWT_SECRET_KEY=your-secret-key-here
   ```

### 3. Initialize Database

```bash
python init_db.py
python seed_data.py
```

### 4. Jalankan Backend

```bash
pserve development.ini
```

Backend akan berjalan di: http://localhost:6543

### 5. Install Dependencies Frontend

Buka terminal baru:

```bash
cd frontend
npm install
```

### 6. Jalankan Frontend

```bash
npm run dev
```

Frontend akan berjalan di: http://localhost:5173

### 7. Testing dengan Postman

1. Import file `FitZone_Gym_API.postman_collection.json` ke Postman
2. Test endpoint `/api/auth/register` untuk membuat user baru
3. Test endpoint `/api/auth/login` untuk login
4. Gunakan token yang didapat untuk mengakses endpoint lain

## Fitur Utama

✅ **Backend:**
- Modular routes (terpisah per feature)
- JWT Authentication
- PostgreSQL Database
- Environment configuration
- Professional code structure

✅ **Frontend:**
- Responsive design (mobile, tablet, desktop)
- AOS animations
- Modern gym theme
- React Icons
- Professional UI/UX

## Struktur Modular Backend

```
backend/app/
├── routes/              # Route definitions (terpisah per feature)
│   ├── auth_routes.py
│   ├── class_routes.py
│   ├── booking_routes.py
│   ├── attendance_routes.py
│   └── membership_routes.py
├── views/               # View handlers
├── models/              # Database models
└── utils/               # Utility functions (auth, etc)
```

## Tips

- Gunakan `.env` untuk menyimpan kredensial (jangan commit ke git)
- Install semua dependencies sebelum menjalankan aplikasi
- Pastikan PostgreSQL running sebelum start backend
- Frontend dan backend harus running bersamaan untuk testing penuh

## Troubleshooting

**Database connection error:**
- Check PostgreSQL service running
- Verify credentials di `.env`
- Pastikan database sudah dibuat

**Module not found:**
- Backend: Activate virtual environment
- Frontend: Run `npm install`

**Port already in use:**
- Backend: Edit port di `development.ini`
- Frontend: Vite akan auto-select port lain
