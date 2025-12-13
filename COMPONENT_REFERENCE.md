# Component & Page Reference Guide

## 📄 New Pages Added (v2.0)

### 1. UserProfile.jsx
**Location**: `frontend/src/pages/UserProfile.jsx`

**Purpose**: Comprehensive user profile management with tabbed interface

**Features**:
- Profile tab (view/edit personal info)
- Bookings tab (view all bookings)
- Attendance tab (attendance history & stats)
- Membership tab (plan details & expiration)
- Logout functionality

**State Management**:
```javascript
const [activeTab, setActiveTab] = useState('profile');
const [userData, setUserData] = useState(null);
const [bookings, setBookings] = useState([]);
const [attendance, setAttendance] = useState([]);
const [membership, setMembership] = useState(null);
const [editMode, setEditMode] = useState(false);
```

**API Endpoints Used**:
- GET /auth/me
- PUT /auth/profile
- GET /bookings/my
- GET /attendance/my
- GET /membership/status

**Icons Used**:
- FaUser (Profile)
- FaCreditCard (Membership)
- FaCalendarAlt (Calendar)
- FaChartLine (Statistics)
- FaEdit (Edit)
- FaSignOutAlt (Logout)

**Styling**: `UserProfile.css` with responsive breakpoints

---

### 2. MembershipPlans.jsx
**Location**: `frontend/src/pages/MembershipPlans.jsx`

**Purpose**: Display and allow selection of membership plans

**Features**:
- Plan comparison cards
- Popular badge on recommended plan
- Feature lists per plan
- Benefits section
- FAQ section
- Plan selection/subscription

**State Management**:
```javascript
const [plans, setPlans] = useState([]);
const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);
const [selectedPlan, setSelectedPlan] = useState(null);
```

**API Endpoints Used**:
- GET /membership/plans
- POST /membership/subscribe

**Icons Used**:
- FaCheck (Checkmarks for features)
- FaCrown (VIP/Elite plans)
- FaStar (Premium plans)
- FaBolt (Basic plans)

**Styling**: `MembershipPlans.css` with gradient cards and hover effects

---

## 🔄 Enhanced Existing Pages

### 3. Classes.jsx (Enhanced)
**Location**: `frontend/src/pages/Classes.jsx`

**New Features Added**:
- Search box with real-time filtering
- Type dropdown filter (10 class types)
- Difficulty dropdown filter (4 levels)
- Date picker filter
- Clear filters button
- Filtered results count

**New State**:
```javascript
const [searchTerm, setSearchTerm] = useState('');
const [selectedType, setSelectedType] = useState('');
const [selectedDifficulty, setSelectedDifficulty] = useState('');
const [selectedDate, setSelectedDate] = useState('');
const [filteredClasses, setFilteredClasses] = useState([]);
```

**New Functions**:
```javascript
const filterClasses = () => {
  // Filters classes based on search and filter criteria
};

const clearFilters = () => {
  // Resets all filters
};
```

**Icons Added**:
- FaSearch (Search icon)
- FaFilter (Filter icon)
- FaStar (Rating display)

**API Enhancement**:
- Now uses query parameters for server-side filtering
- `GET /classes?search=term&class_type=YOGA&difficulty=BEGINNER&date=2025-01-15`

**Styling Updates**: `Classes.css` with filter section, search box, and responsive grid

---

## 🧩 Updated Components

### 4. Navbar.jsx (Updated)
**Location**: `frontend/src/components/Navbar.jsx`

**Changes Made**:
- Added "Membership" link (visible to all users)
- Added "Profile" link (authenticated users only)
- Maintained existing authentication logic
- Mobile responsive menu updated

**New Menu Structure**:
```javascript
<ul>
  <li><Link to="/">Home</Link></li>
  <li><Link to="/classes">Classes</Link></li>
  <li><Link to="/membership">Membership</Link></li> {/* NEW */}
  {user && (
    <>
      <li><Link to="/my-bookings">My Bookings</Link></li>
      <li><Link to="/profile">Profile</Link></li> {/* NEW */}
    </>
  )}
</ul>
```

---

### 5. App.jsx (Updated)
**Location**: `frontend/src/App.jsx`

**New Routes Added**:
```javascript
<Routes>
  {/* Existing routes */}
  <Route path="/" element={<Home />} />
  <Route path="/login" element={<Login />} />
  <Route path="/register" element={<Register />} />
  <Route path="/classes" element={<Classes />} />
  <Route path="/my-bookings" element={<MyBookings />} />
  
  {/* NEW ROUTES */}
  <Route path="/profile" element={<UserProfile />} />
  <Route path="/membership" element={<MembershipPlans />} />
</Routes>
```

**New Imports**:
```javascript
import UserProfile from "./pages/UserProfile";
import MembershipPlans from "./pages/MembershipPlans";
```

---

## 🗄️ Backend Files Added

### 6. review.py (Model)
**Location**: `backend/app/models/review.py`

**Purpose**: Review and rating model for classes

**Schema**:
```python
class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey('gym_classes.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Float, nullable=False)  # 1.0 - 5.0
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
```

**Relationships**:
- Belongs to GymClass
- Belongs to User

**Methods**:
- `to_dict()`: Convert to dictionary

**Constraints**:
- Rating between 1.0 and 5.0
- CASCADE delete with class and user

---

### 7. gym_class_enhanced.py (Enhanced Model)
**Location**: `backend/app/models/gym_class_enhanced.py`

**Purpose**: Enhanced GymClass model with types and difficulty

**New ENUMs**:
```python
class ClassType(enum.Enum):
    YOGA = "Yoga"
    HIIT = "HIIT"
    STRENGTH = "Strength Training"
    CARDIO = "Cardio"
    PILATES = "Pilates"
    CROSSFIT = "CrossFit"
    ZUMBA = "Zumba"
    SPINNING = "Spinning"
    BOXING = "Boxing"
    STRETCHING = "Stretching"

class Difficulty(enum.Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    ALL_LEVELS = "All Levels"
```

**New Fields**:
```python
class_type = Column(Enum(ClassType))
difficulty = Column(Enum(Difficulty))
duration = Column(Integer)  # minutes
```

**New Methods**:
- `get_average_rating()`: Calculate average from reviews
- `is_full()`: Check if class is at capacity
- `get_available_slots()`: Calculate remaining slots

**New Relationship**:
- `reviews`: Relationship to Review model

---

### 8. review_views.py (Views)
**Location**: `backend/app/views/review_views.py`

**Purpose**: Handle review CRUD operations

**Functions**:

```python
def get_class_reviews(request):
    """Get all reviews for a specific class"""
    # Public endpoint, no auth required
    
def create_review(request):
    """Create a new review"""
    # Requires authentication
    # Requires user attended the class (booking exists)
    # Validates rating (1.0-5.0)
    
def update_review(request):
    """Update an existing review"""
    # Requires authentication
    # Requires ownership
    
def delete_review(request):
    """Delete a review"""
    # Requires authentication
    # Requires ownership
    
def get_my_reviews(request):
    """Get all reviews by current user"""
    # Requires authentication
```

**Authentication**: Uses JWT token validation

**Authorization**: Ownership checks for update/delete

---

### 9. class_views_enhanced.py (Enhanced Views)
**Location**: `backend/app/views/class_views_enhanced.py`

**Purpose**: Enhanced class views with filtering

**Enhanced Functions**:

```python
def get_classes(request):
    """Get all classes with optional filters"""
    # Query parameters:
    # - search: text search
    # - class_type: filter by type
    # - difficulty: filter by difficulty
    # - date: filter by specific date
    # - min_date: filter classes after date
    # - max_date: filter classes before date
    
def get_class(request):
    """Get single class with enhanced details"""
    # Includes:
    # - Average rating from reviews
    # - Booked count
    # - Available slots
    
def get_class_participants(request):
    """Get class participants with attendance"""
    # TRAINER/ADMIN only
```

**Database Optimization**:
- Uses SQLAlchemy filters
- Joins for related data
- Aggregation for counts and averages

---

### 10. review_routes.py (Routes)
**Location**: `backend/app/routes/review_routes.py`

**Purpose**: Define review API endpoints

**Routes Defined**:
```python
def includeme(config):
    config.add_route('api_class_reviews', '/api/classes/{id}/reviews')
    config.add_route('api_review', '/api/reviews/{id}')
    config.add_route('api_my_reviews', '/api/reviews/my')
```

**Mappings**:
- GET /api/classes/{id}/reviews → get_class_reviews
- POST /api/classes/{id}/reviews → create_review
- GET /api/reviews/{id} → (future: get single review)
- PUT /api/reviews/{id} → update_review
- DELETE /api/reviews/{id} → delete_review
- GET /api/reviews/my → get_my_reviews

---

### 11. routes/__init__.py (Updated)
**Location**: `backend/app/routes/__init__.py`

**Changes Made**:
```python
def include_routes(config):
    # Existing routes
    config.include('.auth_routes')
    config.include('.class_routes')
    config.include('.booking_routes')
    config.include('.attendance_routes')
    config.include('.membership_routes')
    
    # NEW: Review routes
    config.include('.review_routes')
```

---

## 🗃️ Database Migration

### 12. 002_add_enhancements.py
**Location**: `backend/alembic/versions/002_add_enhancements.py`

**Purpose**: Database migration for v2.0 features

**Changes Applied**:

1. **Create ENUMs**:
   - ClassType (10 types)
   - Difficulty (4 levels)

2. **Alter gym_classes table**:
   - Add class_type column
   - Add difficulty column
   - Add duration column
   - Set defaults for existing records

3. **Create reviews table**:
   - Complete schema with constraints
   - Foreign keys with CASCADE
   - Rating check constraint

4. **Create indexes**:
   - idx_gym_classes_type
   - idx_gym_classes_difficulty
   - idx_gym_classes_date
   - idx_reviews_class_id
   - idx_reviews_user_id

**Upgrade**: `alembic upgrade head`

**Downgrade**: `alembic downgrade -1`

---

## 🎨 CSS Files Added/Updated

### UserProfile.css
- Sidebar navigation styling
- Tab button styles
- Profile header with avatar
- Detail rows with labels
- Form styling for edit mode
- Booking/attendance list items
- Membership card with gradient
- Responsive breakpoints

### MembershipPlans.css
- Plan card grid layout
- Popular badge positioning
- Plan icon circles
- Pricing display
- Feature list with checkmarks
- Benefits section
- FAQ section
- Hover effects and animations
- Responsive breakpoints

### Classes.css (Enhanced)
- Filter section layout
- Search box with icon positioning
- Filter dropdowns styling
- Clear filters button
- Results count display
- Updated grid for filtered layout
- Responsive filter layout

---

## 📊 Component Hierarchy

```
App
├── Navbar (updated)
│   ├── Logo → Home
│   ├── Classes
│   ├── Membership (new)
│   ├── My Bookings (auth)
│   └── Profile (new, auth)
│
├── Routes
│   ├── Home
│   ├── Login
│   ├── Register
│   ├── Classes (enhanced)
│   │   ├── Search Box (new)
│   │   ├── Filters (new)
│   │   └── ClassCard (shows ratings)
│   ├── MyBookings
│   │   └── BookingCard
│   ├── UserProfile (new)
│   │   ├── Profile Tab
│   │   ├── Bookings Tab
│   │   ├── Attendance Tab
│   │   └── Membership Tab
│   └── MembershipPlans (new)
│       ├── Plan Cards
│       ├── Benefits Section
│       └── FAQ Section
│
└── Footer
```

---

## 🔗 API Endpoint Mapping

| Frontend Page | API Endpoints Used |
|--------------|-------------------|
| Home | None (static) |
| Login | POST /auth/login |
| Register | POST /auth/register |
| Classes | GET /classes (with filters) |
| MyBookings | GET /bookings/my, DELETE /bookings/{id} |
| **UserProfile** | GET /auth/me, PUT /auth/profile, GET /bookings/my, GET /attendance/my, GET /membership/status |
| **MembershipPlans** | GET /membership/plans, POST /membership/subscribe |

---

## 🆕 New vs. Enhanced Summary

### Completely New
- ✅ UserProfile page & component
- ✅ MembershipPlans page & component
- ✅ Review model & views
- ✅ Review routes
- ✅ Database migration (002)

### Enhanced Existing
- ✅ Classes page (search & filters)
- ✅ GymClass model (types & difficulty)
- ✅ Class views (filtering logic)
- ✅ Navbar (new links)
- ✅ App routing (new routes)

### Updated Documentation
- ✅ README.md
- ✅ FEATURES.md (new)
- ✅ API_REFERENCE.md (new)
- ✅ QUICK_START.md (new)
- ✅ TESTING_CHECKLIST.md (new)
- ✅ ENHANCEMENT_SUMMARY.md (new)

---

## 📦 File Count Summary

- **New Frontend Files**: 4 (2 JSX + 2 CSS)
- **Enhanced Frontend Files**: 3 (Classes.jsx/css, Navbar.jsx, App.jsx)
- **New Backend Files**: 5 (2 models, 2 views, 1 routes)
- **Enhanced Backend Files**: 2 (routes/__init__.py, class views)
- **New Migration Files**: 1
- **New Documentation Files**: 6
- **Total New/Modified**: 21 files

---

**Reference Version**: 2.0.0  
**Last Updated**: January 10, 2025
