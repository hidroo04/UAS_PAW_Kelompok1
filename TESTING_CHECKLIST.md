# Testing & Deployment Checklist

## 📋 Pre-Deployment Testing Checklist

### Backend Testing

#### Database Setup
- [ ] PostgreSQL service is running
- [ ] Database `gym_booking_db` exists
- [ ] Connection string in `.env` is correct
- [ ] Run migrations: `alembic upgrade head`
- [ ] Verify tables created (users, gym_classes, bookings, attendance, reviews, members)
- [ ] Check ENUM types created (classtype, difficulty)
- [ ] Verify indexes exist

#### Backend Dependencies
- [ ] Virtual environment activated
- [ ] All packages installed: `pip install -r requirements.txt`
- [ ] Check Python version (3.8+)
- [ ] Verify packages: pyramid, sqlalchemy, alembic, psycopg2-binary, PyJWT, python-dotenv

#### Environment Configuration
- [ ] `.env` file exists
- [ ] `DATABASE_URL` configured correctly
- [ ] `JWT_SECRET_KEY` is set (strong random string)
- [ ] `JWT_EXPIRATION_HOURS` is set (default: 24)
- [ ] Test environment loading: `python -c "from app.config import get_database_url; print(get_database_url())"`

#### Server Startup
- [ ] Start server: `pserve development.ini`
- [ ] Server starts without errors
- [ ] Server accessible at http://localhost:6543
- [ ] Health check endpoint responds (if exists)

#### API Endpoints Testing (use Postman)

**Authentication**
- [ ] POST /api/auth/register - Create new user
- [ ] POST /api/auth/login - Login and receive token
- [ ] GET /api/auth/me - Get current user (with token)
- [ ] PUT /api/auth/profile - Update profile (with token)

**Classes**
- [ ] GET /api/classes - Get all classes
- [ ] GET /api/classes?search=yoga - Search classes
- [ ] GET /api/classes?class_type=YOGA - Filter by type
- [ ] GET /api/classes?difficulty=BEGINNER - Filter by difficulty
- [ ] GET /api/classes?date=2025-01-15 - Filter by date
- [ ] GET /api/classes/{id} - Get single class
- [ ] POST /api/classes - Create class (TRAINER/ADMIN token)
- [ ] PUT /api/classes/{id} - Update class (TRAINER/ADMIN token)
- [ ] DELETE /api/classes/{id} - Delete class (ADMIN token)
- [ ] GET /api/classes/{id}/participants - Get participants (TRAINER/ADMIN)

**Bookings**
- [ ] GET /api/bookings/my - Get user bookings (with token)
- [ ] POST /api/bookings - Create booking (with token)
- [ ] DELETE /api/bookings/{id} - Cancel booking (with token)
- [ ] GET /api/bookings - Get all bookings (ADMIN token)

**Attendance**
- [ ] GET /api/attendance/my - Get user attendance (with token)
- [ ] POST /api/attendance/mark - Mark attendance (TRAINER/ADMIN)
- [ ] GET /api/attendance/class/{id} - Get class attendance (TRAINER/ADMIN)

**Membership**
- [ ] GET /api/membership/plans - Get plans (no auth)
- [ ] POST /api/membership/subscribe - Subscribe to plan (with token)
- [ ] GET /api/membership/my - Get user membership (with token)
- [ ] GET /api/membership/status - Get membership status (with token)

**Reviews** ⭐ NEW
- [ ] GET /api/classes/{id}/reviews - Get class reviews (no auth)
- [ ] POST /api/classes/{id}/reviews - Create review (with token, must have attended)
- [ ] PUT /api/reviews/{id} - Update review (with token, owner only)
- [ ] DELETE /api/reviews/{id} - Delete review (with token, owner only)
- [ ] GET /api/reviews/my - Get user reviews (with token)

#### Backend Validation Testing
- [ ] Test invalid JWT token (401 response)
- [ ] Test expired JWT token (401 response)
- [ ] Test missing required fields (400 response)
- [ ] Test invalid rating (< 1.0 or > 5.0) (400 response)
- [ ] Test unauthorized access (403 response)
- [ ] Test non-existent resource (404 response)

---

### Frontend Testing

#### Frontend Dependencies
- [ ] Node.js installed (16+)
- [ ] Run `npm install` in frontend directory
- [ ] Verify no installation errors
- [ ] Check packages: react, react-dom, react-router-dom, axios, aos, react-icons

#### Development Server
- [ ] Start dev server: `npm run dev`
- [ ] Server accessible at http://localhost:5173 (or assigned port)
- [ ] No console errors in browser
- [ ] Hot reload works on file changes

#### API Connection
- [ ] Update API base URL in `src/services/api.js`
- [ ] Test connection to backend
- [ ] Verify CORS headers allow frontend origin
- [ ] Check network tab for API calls

#### Page Testing

**Home Page**
- [ ] Page loads without errors
- [ ] Hero section displays correctly
- [ ] Features section displays
- [ ] CTA buttons work
- [ ] AOS animations trigger on scroll
- [ ] Responsive on mobile/tablet/desktop

**Classes Page** 🔍 ENHANCED
- [ ] Classes load from API
- [ ] Search box filters classes in real-time
- [ ] Type dropdown filters classes
- [ ] Difficulty dropdown filters classes
- [ ] Date picker filters classes
- [ ] Multiple filters work together
- [ ] Clear filters button resets all filters
- [ ] Filtered count displays correctly
- [ ] Class cards display all information
- [ ] Book button works (if logged in)
- [ ] Average rating displays (if reviews exist)
- [ ] Available slots show correctly
- [ ] Responsive layout

**Login Page**
- [ ] Form displays correctly
- [ ] Email validation works
- [ ] Password field hides input
- [ ] Submit button works
- [ ] Error messages display for invalid credentials
- [ ] Success: redirects to home/classes
- [ ] Token stored in localStorage
- [ ] User data stored in localStorage

**Register Page**
- [ ] Form displays correctly
- [ ] All fields validate
- [ ] Password confirmation works
- [ ] Email format validation
- [ ] Submit button works
- [ ] Error messages display
- [ ] Success: redirects to login or home
- [ ] Link to login page works

**My Bookings Page**
- [ ] Requires authentication
- [ ] Bookings load from API
- [ ] Displays all user bookings
- [ ] Shows booking status (confirmed, cancelled)
- [ ] Cancel button works
- [ ] Empty state displays when no bookings
- [ ] Responsive layout

**User Profile Page** 👤 NEW
- [ ] Requires authentication
- [ ] Profile tab displays user info
- [ ] Edit button enables edit mode
- [ ] Profile update works
- [ ] Bookings tab shows user bookings
- [ ] Attendance tab shows attendance records
- [ ] Attendance statistics display correctly
- [ ] Membership tab shows membership details
- [ ] Days remaining calculates correctly
- [ ] Logout button works
- [ ] Tabs switch smoothly
- [ ] Sidebar navigation works
- [ ] Responsive (sidebar becomes horizontal on mobile)

**Membership Plans Page** 💳 NEW
- [ ] Plans load from API
- [ ] Plan cards display correctly
- [ ] Popular badge shows on recommended plan
- [ ] Features list displays with checkmarks
- [ ] Plan icons display (bolt, star, crown)
- [ ] Select plan button works
- [ ] Benefits section displays
- [ ] FAQ section displays
- [ ] Hover effects work
- [ ] Responsive grid layout

#### Component Testing

**Navbar** 🗂️ UPDATED
- [ ] Logo displays and links to home
- [ ] Navigation links work
- [ ] "Membership" link displays (all users)
- [ ] "Profile" link displays (authenticated only)
- [ ] User name displays when logged in
- [ ] Logout button works
- [ ] Mobile menu toggle works
- [ ] Responsive design

**Footer**
- [ ] Footer displays on all pages
- [ ] Social links work (if configured)
- [ ] Copyright text displays
- [ ] Responsive layout

**ClassCard**
- [ ] Class information displays
- [ ] Trainer name shows
- [ ] Date and time format correctly
- [ ] Capacity shows (X/Y)
- [ ] Average rating displays (if reviews exist)
- [ ] Class type badge shows
- [ ] Difficulty badge shows
- [ ] Book button state changes based on auth

**BookingCard**
- [ ] Booking information displays
- [ ] Class details show
- [ ] Status badge displays correctly
- [ ] Cancel button works
- [ ] Responsive design

#### Browser Testing
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (if on Mac)
- [ ] Edge (latest)
- [ ] Mobile Chrome (responsive mode)
- [ ] Mobile Safari (responsive mode)

#### Performance Testing
- [ ] Page load time < 3 seconds
- [ ] API response time < 500ms
- [ ] Images optimized
- [ ] No memory leaks (dev tools)
- [ ] Smooth scrolling with AOS
- [ ] No layout shifts

---

### Integration Testing

#### Full User Flows

**New User Registration Flow**
- [ ] Visit site (not logged in)
- [ ] Click "Join Now" in navbar
- [ ] Fill registration form
- [ ] Submit and verify account created
- [ ] Redirected appropriately
- [ ] Login works with new credentials

**Class Booking Flow**
- [ ] Login to account
- [ ] Navigate to Classes page
- [ ] Search/filter for specific class
- [ ] Click on class card
- [ ] Click "Book Now"
- [ ] Verify booking created
- [ ] Check "My Bookings" page
- [ ] Booking appears in list

**Review Creation Flow** ⭐ NEW
- [ ] Login to account
- [ ] Book a class
- [ ] Mark attendance (TRAINER/ADMIN)
- [ ] Navigate to class page
- [ ] Submit review with rating and comment
- [ ] Verify review appears
- [ ] Edit review
- [ ] Delete review

**Profile Management Flow** 👤 NEW
- [ ] Login to account
- [ ] Navigate to Profile page
- [ ] View profile information
- [ ] Edit profile (update name, email, phone)
- [ ] Switch to Bookings tab
- [ ] View all bookings
- [ ] Switch to Attendance tab
- [ ] View attendance history
- [ ] Switch to Membership tab
- [ ] View membership details

**Membership Subscription Flow** 💳 NEW
- [ ] Login to account
- [ ] Navigate to Membership page
- [ ] Compare plans
- [ ] Select a plan
- [ ] Verify subscription success
- [ ] Check Profile > Membership tab
- [ ] Membership details updated

**Search & Filter Flow** 🔍 NEW
- [ ] Navigate to Classes page
- [ ] Type in search box (e.g., "yoga")
- [ ] Results filter in real-time
- [ ] Select type from dropdown
- [ ] Results update
- [ ] Select difficulty from dropdown
- [ ] Results update
- [ ] Select date from date picker
- [ ] Results update
- [ ] Click "Clear Filters"
- [ ] All classes show again

---

## 🚀 Deployment Checklist

### Pre-Deployment

#### Code Quality
- [ ] No console.log statements in production code
- [ ] No commented-out code blocks
- [ ] All TODO comments addressed
- [ ] Code follows project style guide
- [ ] No hardcoded credentials
- [ ] Environment variables used for sensitive data

#### Security
- [ ] JWT secret is strong and unique
- [ ] Database credentials secured
- [ ] CORS configured for production domain
- [ ] SQL injection prevention verified
- [ ] XSS prevention verified
- [ ] HTTPS enforced (production)
- [ ] Rate limiting configured (recommended)

#### Database
- [ ] Backup database before deployment
- [ ] Migration scripts tested
- [ ] Rollback plan prepared
- [ ] Database indexes verified
- [ ] Foreign key constraints active

#### Documentation
- [ ] README.md updated
- [ ] API documentation complete
- [ ] Setup guide accurate
- [ ] Changelog updated
- [ ] Known issues documented

### Backend Deployment

#### Production Configuration
- [ ] Create production `.env` file
- [ ] Update database URL for production
- [ ] Set strong JWT secret
- [ ] Configure production server (pserve or gunicorn)
- [ ] Set up process manager (systemd/supervisor)

#### Server Setup
- [ ] Install Python 3.8+
- [ ] Create virtual environment
- [ ] Install dependencies
- [ ] Run database migrations
- [ ] Seed initial data (if needed)
- [ ] Configure firewall rules
- [ ] Set up SSL certificate
- [ ] Configure reverse proxy (nginx/apache)

#### Monitoring
- [ ] Set up logging
- [ ] Configure error tracking (Sentry, etc.)
- [ ] Set up uptime monitoring
- [ ] Configure backup schedule
- [ ] Set up alerts

### Frontend Deployment

#### Build Process
- [ ] Update API base URL for production
- [ ] Run `npm run build`
- [ ] Test production build locally
- [ ] Verify no build errors
- [ ] Check bundle size

#### Hosting
- [ ] Choose hosting provider (Vercel, Netlify, S3, etc.)
- [ ] Upload build files
- [ ] Configure custom domain
- [ ] Set up SSL certificate
- [ ] Configure redirects for SPA routing

#### CDN Configuration
- [ ] Enable CDN for static assets
- [ ] Configure caching headers
- [ ] Test asset loading
- [ ] Verify CORS for CDN

### Post-Deployment

#### Verification
- [ ] Access production URL
- [ ] Test all critical user flows
- [ ] Verify API endpoints work
- [ ] Check database connectivity
- [ ] Test authentication
- [ ] Verify email notifications (if configured)

#### Performance
- [ ] Run Lighthouse audit
- [ ] Check Core Web Vitals
- [ ] Test on mobile devices
- [ ] Verify load times
- [ ] Monitor server resources

#### Final Checks
- [ ] All features working as expected
- [ ] No console errors
- [ ] Mobile responsive
- [ ] Cross-browser compatible
- [ ] Analytics configured (optional)

---

## 🐛 Troubleshooting

### Common Issues

#### Backend Issues
- **Database connection failed**: Check PostgreSQL service, credentials, database exists
- **Migration errors**: Check Alembic version, database state, rollback and retry
- **Import errors**: Verify virtual environment, reinstall dependencies
- **JWT errors**: Check secret key in .env, verify token format

#### Frontend Issues
- **API connection failed**: Check backend URL, CORS configuration, network tab
- **Blank page**: Check console for errors, verify build process
- **Routes not working**: Check React Router configuration, server redirects for SPA
- **Filters not working**: Check state management, API response format

#### Database Issues
- **Tables not found**: Run migrations, check database name
- **ENUM errors**: Check ENUM types created, migration ran successfully
- **Foreign key errors**: Check referenced records exist, cascade deletes configured

---

## 📊 Success Criteria

### Feature Completeness
- ✅ All v2.0 features implemented
- ✅ All API endpoints working
- ✅ All pages accessible
- ✅ All components functional
- ✅ Database migrations successful

### Quality Standards
- ✅ No critical bugs
- ✅ Responsive on all devices
- ✅ Cross-browser compatible
- ✅ Load time < 3 seconds
- ✅ API response < 500ms

### Documentation
- ✅ README complete
- ✅ API reference available
- ✅ Setup guide clear
- ✅ Postman collection updated
- ✅ Code comments adequate

---

## 📝 Testing Notes

**Tester Name**: ________________  
**Date**: ________________  
**Environment**: Development / Staging / Production  
**Browser/Device**: ________________

**Issues Found**:
1. _____________________________________________
2. _____________________________________________
3. _____________________________________________

**Notes**:
_________________________________________________
_________________________________________________
_________________________________________________

---

**Checklist Version**: 2.0  
**Last Updated**: January 10, 2025
