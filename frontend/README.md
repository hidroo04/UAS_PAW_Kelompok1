# FitZone Gym System – Presentation Script (MD)

Skrip presentasi ini merangkum rute (routes), API, tabel database, serta teknologi frontend yang digunakan pada sistem FitZone Gym.

## 1. Arsitektur Sistem

- **Backend**: Pyramid (Python) + Waitress, Database PostgreSQL
- **Frontend**: React 18 + Vite (SPA)
- **Autentikasi**: JWT via header `Authorization: Bearer <token>`
- **CORS**: Diaktifkan untuk `GET, POST, PUT, DELETE, OPTIONS`

## 2. Routes & API Utama (Backend)

### Auth & Users
- `POST /api/auth/register` – Registrasi pengguna
- `POST /api/auth/login` – Login, terima JWT
- `POST /api/auth/logout` – Logout
- `GET  /api/auth/me` – Profil pengguna saat ini
- `GET  /api/users` – Daftar pengguna; `GET /api/users/{id}` detail

### Classes
- `GET  /api/classes` – List kelas gym
- `GET  /api/classes/{id}` – Detail kelas
- `GET  /api/classes/{id}/participants` – Peserta kelas

### Bookings
- `GET  /api/bookings` – Semua booking (termasuk relasi class & member)
- `GET  /api/bookings/my` – Booking milik member yang login
- `POST /api/bookings` – Buat booking baru
- `DELETE /api/bookings/{id}` – Batalkan booking
	- Admin: dapat batalkan booking siapa saja
	- Member: hanya dapat batalkan booking miliknya

### Attendance
- `GET  /api/attendance` – Daftar kehadiran
- `GET  /api/attendance/my` – Kehadiran milik pengguna login

### Membership
- `GET  /api/membership/plans` – Rencana keanggotaan
- `GET  /api/membership/my` – Keanggotaan pengguna login
- `GET  /api/members` – Daftar member

### Reviews
- `GET  /api/classes/{id}/reviews` – Review untuk kelas
- `GET  /api/reviews/{id}` – Detail review
- `GET  /api/reviews/my` – Review milik pengguna

### Trainer
- `GET  /api/trainer/classes` – Kelas yang dikelola trainer
- `GET  /api/trainer/classes/{class_id}/members` – Anggota kelas
- `POST /api/trainer/classes/{class_id}/attendance/{booking_id}` – Tandai hadir
- `POST /api/trainer/classes/create` – Buat kelas
- `POST /api/trainer/classes/{class_id}/update` – Ubah kelas
- `POST /api/trainer/classes/{class_id}/delete` – Hapus kelas

## 3. Skema Database (PostgreSQL)

### Tabel `users`
- Kolom: `id`, `name`, `email` (unik), `password`, `phone`, `address`, `avatar_url`, `role` (admin/trainer/member), `created_at`, `updated_at`
- Relasi: `member` (1–1), `trainer_classes` (1–N), `reviews` (1–N)

### Tabel `members`
- Kolom: `id`, `user_id` (FK `users`, unik), `membership_plan` (Basic/Premium/VIP), `expiry_date`
- Relasi: `user` (1–1), `bookings` (1–N)

### Tabel `classes`
- Kolom: `id`, `trainer_id` (FK `users`), `name`, `description`, `schedule` (DateTime), `capacity`, `created_at`
- Relasi: `trainer` (users), `bookings` (1–N)

### Tabel `bookings`
- Kolom: `id`, `member_id` (FK `members`), `class_id` (FK `classes`), `booking_date`
- Relasi: `member`, `gym_class`, `attendance` (1–1)
- Constraint: `unique_member_class_booking` – satu member hanya bisa booking kelas yang sama sekali

### Tabel `attendance`
- Kolom: `id`, `booking_id` (FK `bookings`, unik), `attended` (bool), `date`
- Relasi: `booking`

### Tabel `reviews`
- Kolom: `id`, `class_id` (FK `classes`), `user_id` (FK `users`), `rating` (float 1–5), `comment`, `created_at`, `updated_at`
- Relasi: `gym_class`, `user`

## 4. Frontend – Teknologi & Struktur

### Teknologi
- **React 18** + **Vite** (development server & build)
- **Axios** untuk HTTP client (`frontend/src/services/api.js`)
- **react-icons** untuk icon UI
- **CSS modular** per komponen/halaman (tema dark + glass morphism)

### Struktur Proyek
```
frontend/
├── public/
├── src/
│   ├── services/        # api.js (Axios + JWT interceptor)
│   ├── components/      # Header, Footer, Cards, dsb.
│   ├── pages/           # Home, Classes, Login, Register, MyBookings, UserProfile
│   │   └── admin/       # AdminDashboard, AdminBookings, AdminAttendance, dll.
│   ├── App.jsx / App.css
│   ├── index.jsx / index.css
│   └── assets/
└── package.json
```

### Alur Frontend
- Interceptor Axios menambahkan JWT otomatis ke setiap request.
- Halaman Admin Dashboard menampilkan statistik + grafik tren membership.
- Halaman Admin Bookings membaca `/bookings` (data relasi member & class tersedia) dan mengizinkan admin membatalkan booking.

## 5. Demo Alur Utama (Ringkas)

1. Login sebagai **admin** → lihat dashboard dan statistik.
2. Kelola **kelas**: buat/update/hapus kelas via rute trainer/admin.
3. **Member** melakukan booking → muncul di Admin Bookings.
4. **Cancel booking**: admin bisa batalkan siapa saja; member hanya miliknya.
5. **Attendance** ditandai oleh trainer; **Review** oleh member.

---

## Lampiran: Perintah Pengembangan Frontend

```bash
npm install
npm run dev
npm run build
```

Dev server: `http://localhost:3000` (atau port Vite yang dikonfigurasi)

## 6. Penjelasan Detail

### 6.1 Autentikasi & Otorisasi
- Frontend menyimpan JWT di `localStorage` setelah login.
- Semua request API otomatis membawa header `Authorization: Bearer <token>` melalui Axios interceptor (`services/api.js`).
- Backend mengekstrak `user_id` dari JWT untuk menentukan hak akses.
- Aturan khusus:
	- Admin: bebas mengelola kelas dan membatalkan booking siapa saja.
	- Member: hanya dapat melihat/membatalkan booking miliknya dan melihat kehadirannya sendiri.
	- Trainer: mengelola kelasnya, menandai kehadiran peserta.

### 6.2 Alur Booking
1) Member login → mendapatkan JWT.
2) Member memilih kelas → `POST /api/bookings` membuat booking.
3) Admin melihat semua booking → `GET /api/bookings` (data sudah termasuk relasi `member` dan `class`).
4) Cancel booking:
	 - Admin: `DELETE /api/bookings/{id}` pada booking apa saja.
	 - Member: `DELETE /api/bookings/{id}` hanya jika booking tersebut miliknya (divalidasi di backend).

Contoh `POST /api/bookings` body:

```json
{
	"class_id": 12
}
```

Contoh sukses `DELETE /api/bookings/{id}`:

```json
{
	"status": "success",
	"message": "Booking cancelled successfully"
}
```

Contoh error (member mencoba batalkan booking orang lain):

```json
{
	"status": "error",
	"message": "Booking not found"
}
```

### 6.3 Relasi Data & Validasi
- `users` 1–1 `members`: setiap member punya satu user.
- `classes` 1–N `bookings`: satu kelas memiliki banyak booking.
- `bookings` 1–1 `attendance`: satu booking memiliki satu record kehadiran.
- Constraint: `unique_member_class_booking` mencegah double booking kelas yang sama oleh member yang sama.

### 6.4 CORS & Error Handling
- CORS aktif untuk semua metode; ada `OPTIONS /*path` untuk preflight.
- Error API menggunakan format konsisten: `{ status: 'error', message: '...' }`.
- Frontend menangani `401` dengan menghapus token dan redirect ke `/login`.

### 6.5 Integrasi Frontend
- Axios client (`services/api.js`) menambahkan token dan mengelola error 401.
- `AdminBookings.jsx`:
	- Memanggil `/bookings`, `/classes`, `/users?role=member`.
	- Menampilkan nama member dari `booking.member.user.name` dan nama kelas dari `booking.class.name` (fallback ke list jika relasi tidak tersedia).
	- Tombol Cancel memanggil `DELETE /bookings/{id}` dan refresh data.
- `AdminDashboard.jsx`:
	- Grafik tren membership: bar horizontal, 3 bar per bulan (Basic, Premium, VIP), scroll vertikal saat konten melebihi container.

### 6.6 Contoh Cepat (curl)

Login dan simpan token:

```bash
curl -X POST http://localhost:6543/api/auth/login \
	-H "Content-Type: application/json" \
	-d '{"email":"admin@example.com","password":"secret"}'
```

Ambil semua booking (gunakan token):

```bash
curl http://localhost:6543/api/bookings \
	-H "Authorization: Bearer <TOKEN>"
```

Batalkan booking dengan id 5:

```bash
curl -X DELETE http://localhost:6543/api/bookings/5 \
	-H "Authorization: Bearer <TOKEN>"
```

---

Jika ingin versi slide, minta saya membuat `frontend/public/presentation.md` dengan poin-poin yang siap dipresentasikan.
