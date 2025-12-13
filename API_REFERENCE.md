# API Quick Reference Guide

## Base URL
```
http://localhost:6543/api
```

---

## 🔐 Authentication Endpoints

### Register
```http
POST /auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "role": "MEMBER"
}

Response: {
  "token": "eyJhbGc...",
  "user": { "id": 1, "name": "John Doe", ... }
}
```

### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "password123"
}

Response: {
  "token": "eyJhbGc...",
  "user": { "id": 1, "name": "John Doe", ... }
}
```

### Get Current User
```http
GET /auth/me
Authorization: Bearer <token>

Response: {
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  ...
}
```

### Update Profile
```http
PUT /auth/profile
Authorization: Bearer <token>
Content-Type: application/json

{
  "full_name": "John Smith",
  "email": "john.smith@example.com",
  "phone": "+62812345678"
}
```

---

## 🏋️ Classes Endpoints

### Get All Classes (with filters)
```http
GET /classes?search=yoga&class_type=YOGA&difficulty=BEGINNER&date=2025-01-15

Query Parameters:
- search: text search (optional)
- class_type: YOGA|HIIT|STRENGTH|CARDIO|PILATES|CROSSFIT|ZUMBA|SPINNING|BOXING|STRETCHING (optional)
- difficulty: BEGINNER|INTERMEDIATE|ADVANCED|ALL_LEVELS (optional)
- date: YYYY-MM-DD (optional)
- min_date: YYYY-MM-DD (optional)
- max_date: YYYY-MM-DD (optional)

Response: [
  {
    "id": 1,
    "name": "Morning Yoga",
    "trainer": "Sarah Johnson",
    "class_type": "YOGA",
    "difficulty": "BEGINNER",
    "duration": 60,
    "date": "2025-01-15",
    "time": "08:00:00",
    "capacity": 20,
    "booked_count": 15,
    "available_slots": 5,
    "average_rating": 4.5
  },
  ...
]
```

### Get Class by ID
```http
GET /classes/{id}

Response: {
  "id": 1,
  "name": "Morning Yoga",
  "trainer": "Sarah Johnson",
  "class_type": "YOGA",
  "difficulty": "BEGINNER",
  "duration": 60,
  ...
}
```

### Create Class (TRAINER/ADMIN)
```http
POST /classes
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Evening HIIT",
  "trainer": "Mike Chen",
  "class_type": "HIIT",
  "difficulty": "INTERMEDIATE",
  "duration": 45,
  "date": "2025-01-20",
  "time": "18:00:00",
  "capacity": 15,
  "description": "High-intensity interval training"
}
```

### Update Class (TRAINER/ADMIN)
```http
PUT /classes/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Updated Class Name",
  "capacity": 25
}
```

### Delete Class (ADMIN)
```http
DELETE /classes/{id}
Authorization: Bearer <token>
```

### Get Class Participants (TRAINER/ADMIN)
```http
GET /classes/{id}/participants
Authorization: Bearer <token>

Response: [
  {
    "user_id": 1,
    "user_name": "John Doe",
    "booking_status": "confirmed",
    "attendance_status": "present"
  },
  ...
]
```

---

## 📅 Booking Endpoints

### Get My Bookings
```http
GET /bookings/my
Authorization: Bearer <token>

Response: [
  {
    "id": 1,
    "class_id": 1,
    "class_name": "Morning Yoga",
    "class_date": "2025-01-15",
    "class_time": "08:00:00",
    "status": "confirmed",
    "booking_date": "2025-01-10T10:30:00"
  },
  ...
]
```

### Create Booking
```http
POST /bookings
Authorization: Bearer <token>
Content-Type: application/json

{
  "class_id": 1
}

Response: {
  "id": 1,
  "class_id": 1,
  "user_id": 1,
  "status": "confirmed",
  "booking_date": "2025-01-10T10:30:00"
}
```

### Cancel Booking
```http
DELETE /bookings/{id}
Authorization: Bearer <token>

Response: {
  "message": "Booking cancelled successfully"
}
```

### Get All Bookings (ADMIN)
```http
GET /bookings
Authorization: Bearer <token>

Response: [...]
```

---

## ✅ Attendance Endpoints

### Get My Attendance
```http
GET /attendance/my
Authorization: Bearer <token>

Response: [
  {
    "id": 1,
    "class_id": 1,
    "class_name": "Morning Yoga",
    "date": "2025-01-15",
    "status": "present",
    "checked_in_at": "2025-01-15T08:05:00"
  },
  ...
]
```

### Mark Attendance (TRAINER/ADMIN)
```http
POST /attendance/mark
Authorization: Bearer <token>
Content-Type: application/json

{
  "booking_id": 1,
  "status": "present"
}
```

### Get Class Attendance (TRAINER/ADMIN)
```http
GET /attendance/class/{class_id}
Authorization: Bearer <token>

Response: [
  {
    "booking_id": 1,
    "user_id": 1,
    "user_name": "John Doe",
    "status": "present",
    "checked_in_at": "2025-01-15T08:05:00"
  },
  ...
]
```

---

## 💳 Membership Endpoints

### Get Membership Plans
```http
GET /membership/plans

Response: [
  {
    "id": 1,
    "name": "Basic",
    "description": "Perfect for beginners",
    "price": 300000,
    "duration_days": 30,
    "class_limit": 8,
    "features": [
      "Access to all gym equipment",
      "8 classes per month",
      "Locker room access"
    ],
    "is_popular": false
  },
  {
    "id": 2,
    "name": "Premium",
    "description": "Most popular choice",
    "price": 500000,
    "duration_days": 30,
    "class_limit": -1,
    "features": [
      "Unlimited classes",
      "Personal trainer consultation",
      "Nutrition guidance"
    ],
    "is_popular": true
  },
  ...
]
```

### Subscribe to Plan
```http
POST /membership/subscribe
Authorization: Bearer <token>
Content-Type: application/json

{
  "plan_id": 2
}

Response: {
  "message": "Membership activated successfully",
  "membership": {
    "plan_id": 2,
    "start_date": "2025-01-10",
    "end_date": "2025-02-09",
    "status": "active"
  }
}
```

### Get My Membership
```http
GET /membership/my
Authorization: Bearer <token>

Response: {
  "plan_id": 2,
  "plan_name": "Premium",
  "start_date": "2025-01-10",
  "end_date": "2025-02-09",
  "status": "active",
  "days_remaining": 30
}
```

### Get Membership Status
```http
GET /membership/status
Authorization: Bearer <token>

Response: {
  "plan_name": "Premium",
  "status": "active",
  "start_date": "2025-01-10",
  "end_date": "2025-02-09",
  "days_remaining": 30
}
```

---

## ⭐ Reviews & Ratings Endpoints

### Get Class Reviews
```http
GET /classes/{class_id}/reviews

Response: [
  {
    "id": 1,
    "class_id": 1,
    "user_id": 1,
    "user_name": "John Doe",
    "rating": 4.5,
    "comment": "Great class! Very motivating instructor.",
    "created_at": "2025-01-15T10:00:00",
    "updated_at": "2025-01-15T10:00:00"
  },
  ...
]
```

### Create Review
```http
POST /classes/{class_id}/reviews
Authorization: Bearer <token>
Content-Type: application/json

{
  "rating": 4.5,
  "comment": "Great class! Very motivating instructor."
}

Requirements:
- Rating must be between 1.0 and 5.0
- User must have attended the class
- User can only review each class once

Response: {
  "id": 1,
  "class_id": 1,
  "user_id": 1,
  "rating": 4.5,
  "comment": "Great class!",
  "created_at": "2025-01-15T10:00:00"
}
```

### Update Review
```http
PUT /reviews/{review_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "rating": 5.0,
  "comment": "Updated: Absolutely fantastic class!"
}

Requirements:
- User must own the review

Response: {
  "id": 1,
  "rating": 5.0,
  "comment": "Updated: Absolutely fantastic class!",
  "updated_at": "2025-01-15T11:00:00"
}
```

### Delete Review
```http
DELETE /reviews/{review_id}
Authorization: Bearer <token>

Requirements:
- User must own the review

Response: {
  "message": "Review deleted successfully"
}
```

### Get My Reviews
```http
GET /reviews/my
Authorization: Bearer <token>

Response: [
  {
    "id": 1,
    "class_id": 1,
    "class_name": "Morning Yoga",
    "rating": 5.0,
    "comment": "Absolutely fantastic class!",
    "created_at": "2025-01-15T10:00:00",
    "updated_at": "2025-01-15T11:00:00"
  },
  ...
]
```

---

## 👥 User Management (ADMIN)

### Get All Members
```http
GET /members
Authorization: Bearer <token> (ADMIN only)

Response: [
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "MEMBER",
    "membership_status": "active",
    "created_at": "2025-01-01T00:00:00"
  },
  ...
]
```

---

## 🔑 Authentication Headers

All protected endpoints require:
```
Authorization: Bearer <your_jwt_token>
```

Get token from login/register response:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {...}
}
```

---

## 📝 Common Response Codes

| Code | Meaning |
|------|---------|
| 200  | Success |
| 201  | Created |
| 400  | Bad Request (validation error) |
| 401  | Unauthorized (invalid/missing token) |
| 403  | Forbidden (insufficient permissions) |
| 404  | Not Found |
| 409  | Conflict (duplicate entry) |
| 500  | Internal Server Error |

---

## 🔍 Filter Examples

### Search for yoga classes
```
GET /classes?search=yoga
```

### Get beginner-friendly classes
```
GET /classes?difficulty=BEGINNER
```

### Get HIIT classes on specific date
```
GET /classes?class_type=HIIT&date=2025-01-20
```

### Get all upcoming classes
```
GET /classes?min_date=2025-01-10
```

### Complex filter
```
GET /classes?class_type=YOGA&difficulty=INTERMEDIATE&min_date=2025-01-15&search=morning
```

---

## 💡 Tips

1. **Token Storage**: Store JWT token in localStorage or secure cookie
2. **Error Handling**: Always check response status and handle errors
3. **Date Format**: Use ISO 8601 format (YYYY-MM-DD) for dates
4. **Time Format**: Use 24-hour format (HH:MM:SS) for times
5. **Rating Validation**: Ratings must be floats between 1.0 and 5.0
6. **Pagination**: Not yet implemented, but planned for future

---

## 🧪 Testing with cURL

### Login Example
```bash
curl -X POST http://localhost:6543/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"password123"}'
```

### Get Classes with Token
```bash
curl -X GET http://localhost:6543/api/classes \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Create Review
```bash
curl -X POST http://localhost:6543/api/classes/1/reviews \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"rating":4.5,"comment":"Great class!"}'
```

---

**Last Updated**: January 10, 2025  
**API Version**: 2.0.0
