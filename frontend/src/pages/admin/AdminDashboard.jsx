import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  FaUsers, 
  FaDumbbell, 
  FaCalendarCheck, 
  FaChartLine, 
  FaCrown, 
  FaStar,
  FaUserCheck,
  FaMoneyBillWave 
} from 'react-icons/fa';
import apiClient from '../../services/api';
import './AdminDashboard.css';

const AdminDashboard = () => {
  const [stats, setStats] = useState({
    totalMembers: 0,
    totalClasses: 0,
    totalBookings: 0,
    todayAttendance: 0,
    basicMembers: 0,
    premiumMembers: 0,
    vipMembers: 0,
    activeMembers: 0
  });
  const [recentBookings, setRecentBookings] = useState([]);
  const [popularClasses, setPopularClasses] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userRole = localStorage.getItem('userRole');
    
    if (!token || userRole !== 'admin') {
      navigate('/login');
      return;
    }
    
    fetchDashboardData();
  }, [navigate]);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch all data in parallel
      const [membersRes, classesRes, bookingsRes] = await Promise.all([
        apiClient.get('/users?role=member'),
        apiClient.get('/classes'),
        apiClient.get('/bookings')
      ]);

      const members = membersRes.data.data || [];
      const classes = classesRes.data.data || [];
      const bookings = bookingsRes.data.data || [];

      // Calculate statistics
      const basicCount = members.filter(m => m.membership_plan === 'Basic').length;
      const premiumCount = members.filter(m => m.membership_plan === 'Premium').length;
      const vipCount = members.filter(m => m.membership_plan === 'VIP').length;
      const activeCount = members.filter(m => m.is_active).length;

      setStats({
        totalMembers: members.length,
        totalClasses: classes.length,
        totalBookings: bookings.length,
        todayAttendance: 0, // Will be calculated from attendance API
        basicMembers: basicCount,
        premiumMembers: premiumCount,
        vipMembers: vipCount,
        activeMembers: activeCount
      });

      // Recent bookings (last 5)
      setRecentBookings(bookings.slice(0, 5));

      // Popular classes (most booked)
      const classBookingCount = {};
      bookings.forEach(booking => {
        const classId = booking.class_id;
        classBookingCount[classId] = (classBookingCount[classId] || 0) + 1;
      });

      const popular = classes
        .map(cls => ({
          ...cls,
          bookingCount: classBookingCount[cls.id] || 0
        }))
        .sort((a, b) => b.bookingCount - a.bookingCount)
        .slice(0, 5);

      setPopularClasses(popular);
      
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="admin-loading">Loading dashboard...</div>;
  }

  return (
    <div className="admin-dashboard">
      <div className="admin-header">
        <h1>Admin Dashboard</h1>
        <p>Welcome back! Here's what's happening with your gym today.</p>
      </div>

      {/* Statistics Cards */}
      <div className="stats-grid">
        <div className="stat-card primary">
          <div className="stat-icon">
            <FaUsers />
          </div>
          <div className="stat-info">
            <h3>{stats.totalMembers}</h3>
            <p>Total Members</p>
            <span className="stat-detail">{stats.activeMembers} active</span>
          </div>
        </div>

        <div className="stat-card success">
          <div className="stat-icon">
            <FaDumbbell />
          </div>
          <div className="stat-info">
            <h3>{stats.totalClasses}</h3>
            <p>Total Classes</p>
            <span className="stat-detail">Available today</span>
          </div>
        </div>

        <div className="stat-card warning">
          <div className="stat-icon">
            <FaCalendarCheck />
          </div>
          <div className="stat-info">
            <h3>{stats.totalBookings}</h3>
            <p>Total Bookings</p>
            <span className="stat-detail">All time</span>
          </div>
        </div>

        <div className="stat-card info">
          <div className="stat-icon">
            <FaUserCheck />
          </div>
          <div className="stat-info">
            <h3>{stats.todayAttendance}</h3>
            <p>Today's Attendance</p>
            <span className="stat-detail">Check-ins</span>
          </div>
        </div>
      </div>

      {/* Membership Distribution */}
      <div className="membership-distribution">
        <h2>Membership Distribution</h2>
        <div className="membership-grid">
          <div className="membership-card basic">
            <div className="membership-icon">💼</div>
            <h3>{stats.basicMembers}</h3>
            <p>Basic Members</p>
            <div className="membership-percentage">
              {stats.totalMembers > 0 ? Math.round((stats.basicMembers / stats.totalMembers) * 100) : 0}%
            </div>
          </div>

          <div className="membership-card premium">
            <div className="membership-icon">⭐</div>
            <h3>{stats.premiumMembers}</h3>
            <p>Premium Members</p>
            <div className="membership-percentage">
              {stats.totalMembers > 0 ? Math.round((stats.premiumMembers / stats.totalMembers) * 100) : 0}%
            </div>
          </div>

          <div className="membership-card vip">
            <div className="membership-icon">👑</div>
            <h3>{stats.vipMembers}</h3>
            <p>VIP Members</p>
            <div className="membership-percentage">
              {stats.totalMembers > 0 ? Math.round((stats.vipMembers / stats.totalMembers) * 100) : 0}%
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="dashboard-content">
        <div className="content-section">
          <h2>Recent Bookings</h2>
          <div className="recent-bookings">
            {recentBookings.length > 0 ? (
              recentBookings.map((booking, index) => (
                <div key={index} className="booking-item">
                  <div className="booking-info">
                    <h4>Class ID: {booking.class_id}</h4>
                    <p>Member ID: {booking.member_id}</p>
                    <span className="booking-date">
                      {new Date(booking.booking_date).toLocaleDateString()}
                    </span>
                  </div>
                  <div className={`booking-status ${booking.status || 'confirmed'}`}>
                    {booking.status || 'Confirmed'}
                  </div>
                </div>
              ))
            ) : (
              <p className="no-data">No recent bookings</p>
            )}
          </div>
        </div>

        <div className="content-section">
          <h2>Popular Classes</h2>
          <div className="popular-classes">
            {popularClasses.length > 0 ? (
              popularClasses.map((cls, index) => (
                <div key={cls.id} className="class-item">
                  <div className="class-rank">#{index + 1}</div>
                  <div className="class-info">
                    <h4>{cls.name}</h4>
                    <p>Trainer ID: {cls.trainer_id}</p>
                  </div>
                  <div className="class-bookings">
                    <FaStar />
                    <span>{cls.bookingCount} bookings</span>
                  </div>
                </div>
              ))
            ) : (
              <p className="no-data">No class data</p>
            )}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="quick-actions">
        <h2>Quick Actions</h2>
        <div className="action-buttons">
          <button className="action-btn" onClick={() => navigate('/admin/members')}>
            <FaUsers />
            <span>Manage Members</span>
          </button>
          <button className="action-btn" onClick={() => navigate('/admin/classes')}>
            <FaDumbbell />
            <span>Manage Classes</span>
          </button>
          <button className="action-btn" onClick={() => navigate('/admin/bookings')}>
            <FaCalendarCheck />
            <span>View Bookings</span>
          </button>
          <button className="action-btn" onClick={() => navigate('/admin/attendance')}>
            <FaUserCheck />
            <span>Mark Attendance</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
