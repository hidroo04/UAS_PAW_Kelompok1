# UAS Pengweb Project

Full-stack web application dengan React Vite (Frontend) dan Python Pyramid (Backend).

## 🚀 Technology Stack

### Frontend

- ReactJS (Create React App atau Vite)
- React Router
- Axios/Fetch API
- CSS murni (wajib untuk CPMK0501) - boleh tambah Tailwind/Bootstrap

### Backend

- Python 3.x
- Pyramid Framework
- SQLAlchemy ORM
- Alembic (migrations)

### Database

- PostgreSQL (wajib)

### Deployment

- Frontend: Vercel
- Backend: Domain \*.web.id (beli sendiri di Niagahoster/Rumahweb)

## 📁 Project Structure

```
project-root/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API calls
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.js
│   ├── package.json
│   └── README.md
│
├── backend/
│   ├── app/
│   │   ├── models/         # Database models (SQLAlchemy)
│   │   ├── views/          # API endpoints/routes
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── alembic/            # Database migrations
│   ├── requirements.txt
│   ├── development.ini
│   └── README.md
│
└── README.md (root - project overview)
```

## 🛠️ Setup Instructions

### Frontend Setup

1. Navigate to frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Run development server:

```bash
npm run dev
```

Frontend will run on `http://localhost:3000`

### Backend Setup

1. Navigate to backend directory:

```bash
cd backend
```

2. Create virtual environment:

```bash
python -m venv venv
```

3. Activate virtual environment:

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
pip install -e .
```

5. Setup database (PostgreSQL):

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
