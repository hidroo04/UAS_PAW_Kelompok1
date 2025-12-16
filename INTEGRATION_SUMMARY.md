# UserProfile Database Integration - Summary

## Perubahan yang Dilakukan

### 1. Backend - Model User (`backend/app/models/user.py`)

**Perubahan:** Update method `to_dict()` untuk mengembalikan data membership dari relasi Member

```python
def to_dict(self):
    user_dict = {
        'id': self.id,
        'name': self.name,
        'email': self.email,
        'phone': self.phone,
        'address': self.address,
        'avatar_url': self.avatar_url,
        'role': self.role.value,
        'created_at': self.created_at.isoformat() if self.created_at else None
    }
    
    # Include membership info if user is a member
    if self.member:
        user_dict['membership_plan'] = self.member.membership_plan
        user_dict['membership_expiry'] = self.member.expiry_date.isoformat() if self.member.expiry_date else None
        user_dict['membership_status'] = 'Active' if self.member.is_active() else 'Expired'
    
    return user_dict
```

**Hasil:** API `/api/profile` sekarang mengembalikan:
- `membership_plan`: 'Basic', 'Premium', atau 'VIP'
- `membership_expiry`: tanggal berakhir membership
- `membership_status`: 'Active' atau 'Expired'

### 2. Frontend - UserProfile Component (`frontend/src/pages/UserProfile.jsx`)

#### a. Update `fetchBookings()`
- Menyimpan data bookings yang sudah lengkap dengan relasi `class` dan `attendance`
- Data yang didapat dari API sudah sesuai dengan struktur database

#### b. Update `fetchAttendance()`
```javascript
const fetchAttendance = async () => {
  try {
    const response = await apiClient.get('/bookings/my');
    if (response.data.status === 'success') {
      // Filter bookings yang sudah ada attendance
      const attendedClasses = (response.data.data || []).filter(booking => 
        booking.attendance !== null && booking.attendance !== undefined
      );
      setAttendance(attendedClasses);
    }
  } catch (err) {
    console.error('Error fetching attendance:', err);
    setAttendance([]);
  }
};
```

**Perubahan:**
- Filter berdasarkan `booking.attendance` (bukan `booking.attendance.status`)
- Check untuk `null` dan `undefined` karena di database attendance bisa tidak ada

#### c. Update `fetchMembership()`
```javascript
const fetchMembership = async () => {
  try {
    const response = await apiClient.get('/bookings/my');
    const bookingsData = response.data.status === 'success' ? response.data.data : [];
    const attendedData = bookingsData.filter(b => b.attendance);
    
    if (userData) {
      const expiryDate = userData.membership_expiry ? new Date(userData.membership_expiry) : null;
      const isActive = expiryDate ? expiryDate > new Date() : false;
      
      setMembership({
        plan: userData.membership_plan || 'Basic',
        status: isActive ? 'Active' : 'Expired',
        expiry: userData.membership_expiry,
        total_bookings: bookingsData.length,
        total_attended: attendedData.filter(b => b.attendance.attended === true).length
      });
    }
  }
};
```

**Perubahan:**
- Menggunakan data dari `userData` yang sudah include membership dari database
- Menghitung `total_bookings` dari jumlah bookings
- Menghitung `total_attended` dari bookings dengan `attendance.attended === true`

#### d. Update `renderBookingsTab()`

**Field yang digunakan dari database:**
- `booking.class.name` - nama class
- `booking.class.schedule` - jadwal class
- `booking.booking_date` - tanggal booking dibuat
- `booking.class.trainer.name` - nama trainer
- `booking.attendance.attended` - status kehadiran (boolean)

```javascript
{bookings.map((booking) => (
  <div key={booking.id} className="booking-item">
    <div className="booking-header">
      <h4>{booking.class?.name || 'Class'}</h4>
      <span className="booking-status status-confirmed">Confirmed</span>
    </div>
    <div className="booking-details">
      <div className="detail-item">
        <HiCalendar />
        <span>{booking.class?.schedule ? new Date(booking.class.schedule).toLocaleDateString() : 'N/A'}</span>
      </div>
      <div className="detail-item">
        <HiUser />
        <span>Booked on: {booking.booking_date ? new Date(booking.booking_date).toLocaleDateString() : 'N/A'}</span>
      </div>
      {booking.class?.trainer && (
        <div className="detail-item">
          <HiAcademicCap />
          <span>Trainer: {booking.class.trainer.name}</span>
        </div>
      )}
      {booking.attendance && (
        <div className="detail-item">
          <HiCheckCircle />
          <span className={`attendance-status ${booking.attendance.attended ? 'present' : 'absent'}`}>
            {booking.attendance.attended ? '✓ Present' : '✗ Absent'}
          </span>
        </div>
      )}
    </div>
  </div>
))}
```

#### e. Update `renderAttendanceTab()`

**Field yang digunakan dari database:**
- `attendance.attended` - boolean (bukan string 'present'/'absent')
- `record.class.name` - nama class
- `record.class.schedule` - jadwal class
- `record.attendance.date` - tanggal attendance dicatat

```javascript
const presentCount = attendance.filter(a => a.attendance?.attended === true).length;
const absentCount = attendance.filter(a => a.attendance?.attended === false).length;

// Render attendance items
{attendance.map((record) => (
  <div key={record.id} className="attendance-item">
    <div className="attendance-header">
      <h4>{record.class?.name || 'Class'}</h4>
      <span className={`attendance-badge ${record.attendance?.attended ? 'present' : 'absent'}`}>
        {record.attendance?.attended ? '✓ Present' : '✗ Absent'}
      </span>
    </div>
    <div className="attendance-details">
      <div className="detail-item">
        <HiCalendar />
        <span>{record.class?.schedule ? new Date(record.class.schedule).toLocaleDateString() : 'N/A'}</span>
      </div>
      {record.attendance?.date && (
        <div className="detail-item">
          <HiClock />
          <span>Marked: {new Date(record.attendance.date).toLocaleDateString()}</span>
        </div>
      )}
    </div>
  </div>
))}
```

### 3. Frontend - CSS Update (`frontend/src/pages/UserProfile.css`)

Tambah styling untuk attendance status:
```css
.attendance-status {
  font-weight: 600;
}

.attendance-status.present {
  color: #22c55e !important;
}

.attendance-status.absent {
  color: #ef4444 !important;
}
```

## Struktur Data dari Database

### API Response `/api/profile`
```json
{
  "status": "success",
  "data": {
    "id": 57,
    "name": "Alice Brown",
    "email": "alice@member.com",
    "phone": null,
    "address": null,
    "avatar_url": null,
    "role": "member",
    "created_at": "2025-12-16T06:24:29.205627",
    "membership_plan": "VIP",
    "membership_expiry": "2026-12-16",
    "membership_status": "Active"
  }
}
```

### API Response `/api/bookings/my`
```json
{
  "status": "success",
  "data": [
    {
      "id": 123,
      "member_id": 28,
      "class_id": 45,
      "booking_date": "2025-12-15T10:30:00",
      "class": {
        "id": 45,
        "name": "Yoga Class",
        "description": "Morning yoga session",
        "schedule": "2025-12-20T08:00:00",
        "capacity": 20,
        "trainer": {
          "id": 12,
          "name": "John Smith",
          "email": "john@trainer.com"
        }
      },
      "attendance": {
        "id": 89,
        "attended": true,
        "date": "2025-12-20T08:15:00"
      }
    }
  ],
  "count": 1
}
```

## Mapping Field Database ke UI

### Bookings Tab
| UI Element | Database Field | Type |
|------------|----------------|------|
| Class Name | `booking.class.name` | string |
| Schedule | `booking.class.schedule` | datetime |
| Booking Date | `booking.booking_date` | datetime |
| Trainer Name | `booking.class.trainer.name` | string |
| Attendance Status | `booking.attendance.attended` | boolean |
| Status Badge | Fixed: "Confirmed" | string |

### Attendance Tab
| UI Element | Database Field | Type |
|------------|----------------|------|
| Class Name | `record.class.name` | string |
| Schedule | `record.class.schedule` | datetime |
| Marked Date | `record.attendance.date` | datetime |
| Present/Absent | `record.attendance.attended` | boolean |
| Present Count | Count where `attended === true` | number |
| Absent Count | Count where `attended === false` | number |

### Membership Tab
| UI Element | Database Field | Type |
|------------|----------------|------|
| Plan Name | `userData.membership_plan` | string |
| Status | `userData.membership_status` | string |
| Expiry Date | `userData.membership_expiry` | date |
| Total Bookings | Count of bookings | number |
| Total Attended | Count where `attendance.attended === true` | number |

## Testing

Login sebagai member untuk test:
- Email: `alice@member.com`
- Password: `password123`

Expected Results:
1. **Profile Tab**: Show membership plan (VIP), expiry date, status (Active)
2. **Bookings Tab**: Show all bookings with class name, schedule, trainer, attendance status
3. **Attendance Tab**: Show only bookings with attendance records, display present/absent counts
4. **Membership Tab**: Show VIP plan with benefits, total bookings, and attended count

## File Changes Summary

1. ✅ `backend/app/models/user.py` - Update to_dict() to include membership data
2. ✅ `frontend/src/pages/UserProfile.jsx` - Update all fetch and render functions
3. ✅ `frontend/src/pages/UserProfile.css` - Add attendance-status styling
4. ✅ Server restarted to apply model changes

Semua menu sudah terhubung dengan database dan menampilkan data yang sesuai!
