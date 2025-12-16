import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  HiUsers, 
  HiAcademicCap, 
  HiCalendar, 
  HiClipboardCheck,
  HiTrendingUp,
  HiStar,
  HiCog,
  HiChartBar
} from 'react-icons/hi';
import { 
  RiVipCrownFill, 
  RiMedalFill,
  RiUserStarFill 
} from 'react-icons/ri';
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
    activeMembers: 0,
    totalTrainers: 0,
    upcomingClasses: 0,
    totalRevenue: 0,
    totalUsers: 0,
    averageBookingsPerClass: 0,
    mostActiveDay: 'N/A',
    bookingGrowth: 0
  });
  const [recentBookings, setRecentBookings] = useState([]);
  const [popularClasses, setPopularClasses] = useState([]);
  const [recentMembers, setRecentMembers] = useState([]);
  const [classUtilization, setClassUtilization] = useState([]);
  const [membershipTrend, setMembershipTrend] = useState({ labels: [], data: [] });
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    
    if (!token || user.role !== 'admin') {
      navigate('/login');
      return;
    }
    
    fetchDashboardData();
  }, [navigate]);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch all data in parallel
      const [membersRes, classesRes, bookingsRes, trainersRes] = await Promise.all([
        apiClient.get('/users?role=member'),
        apiClient.get('/classes'),
        apiClient.get('/bookings'),
        apiClient.get('/users?role=trainer')
      ]);

      const members = membersRes.data.data || [];
      const classes = classesRes.data.data || [];
      const bookings = bookingsRes.data.data || [];
      const trainers = trainersRes.data.data || [];

      // Calculate statistics
      const basicCount = members.filter(m => m.membership_plan === 'Basic').length;
      const premiumCount = members.filter(m => m.membership_plan === 'Premium').length;
      const vipCount = members.filter(m => m.membership_plan === 'VIP').length;
      const activeCount = members.filter(m => m.is_active).length;

      // Calculate upcoming classes
      const now = new Date();
      const upcomingCount = classes.filter(cls => {
        if (cls.schedule) {
          const scheduleDate = new Date(cls.schedule);
          return scheduleDate > now;
        }
        return false;
      }).length;

      // Calculate revenue estimation
      const basicPrice = 100000;
      const premiumPrice = 250000;
      const vipPrice = 500000;
      const revenue = (basicCount * basicPrice) + (premiumCount * premiumPrice) + (vipCount * vipPrice);

      // Calculate average bookings per class
      const avgBookings = classes.length > 0 ? (bookings.length / classes.length).toFixed(1) : 0;

      // Find most active day
      const dayCount = {};
      bookings.forEach(booking => {
        if (booking.booking_date) {
          const day = new Date(booking.booking_date).toLocaleDateString('en-US', { weekday: 'long' });
          dayCount[day] = (dayCount[day] || 0) + 1;
        }
      });
      const mostActive = Object.keys(dayCount).length > 0 
        ? Object.entries(dayCount).sort((a, b) => b[1] - a[1])[0][0]
        : 'N/A';

      // Calculate booking growth (comparing this week vs last week)
      const today = new Date();
      const lastWeek = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);
      const twoWeeksAgo = new Date(today.getTime() - 14 * 24 * 60 * 60 * 1000);
      
      const thisWeekBookings = bookings.filter(b => {
        const bookingDate = new Date(b.booking_date);
        return bookingDate >= lastWeek && bookingDate <= today;
      }).length;
      
      const lastWeekBookings = bookings.filter(b => {
        const bookingDate = new Date(b.booking_date);
        return bookingDate >= twoWeeksAgo && bookingDate < lastWeek;
      }).length;

      const growth = lastWeekBookings > 0 
        ? (((thisWeekBookings - lastWeekBookings) / lastWeekBookings) * 100).toFixed(1)
        : 0;

      // Calculate total users (all roles)
      const totalUsers = members.length + trainers.length + 1; // +1 for admin

      setStats({
        totalMembers: members.length,
        totalClasses: classes.length,
        totalBookings: bookings.length,
        todayAttendance: 0, // Will be calculated from attendance API
        basicMembers: basicCount,
        premiumMembers: premiumCount,
        vipMembers: vipCount,
        activeMembers: activeCount,
        totalTrainers: trainers.length,
        upcomingClasses: upcomingCount,
        totalRevenue: revenue,
        totalUsers: totalUsers,
        averageBookingsPerClass: avgBookings,
        mostActiveDay: mostActive,
        bookingGrowth: growth
      });

      // Recent members (last 5)
      setRecentMembers(members.slice(0, 5));

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

      // Calculate class utilization (booking vs capacity)
      const utilization = classes
        .map(cls => ({
          name: cls.name,
          bookings: classBookingCount[cls.id] || 0,
          capacity: cls.capacity || 20,
          percentage: cls.capacity > 0 
            ? ((classBookingCount[cls.id] || 0) / cls.capacity * 100).toFixed(1)
            : 0
        }))
        .sort((a, b) => b.percentage - a.percentage)
        .slice(0, 5);

      setClassUtilization(utilization);

      // Calculate membership trend (last 6 months simulation)
      const monthNames = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      const membershipData = monthNames.map((month, index) => {
        return Math.floor(members.length * (0.6 + (index * 0.08))); // Simulated growth
      });

      setMembershipTrend({
        labels: monthNames,
        data: membershipData
      });
      
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
        <div className="stat-card">
          <div className="stat-icon">
            <HiUsers />
          </div>
          <div className="stat-info">
            <h3>{stats.totalMembers}</h3>
            <p>Total Members</p>
            <span className="stat-detail">{stats.activeMembers} active</span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <HiAcademicCap />
          </div>
          <div className="stat-info">
            <h3>{stats.totalClasses}</h3>
            <p>Total Classes</p>
            <span className="stat-detail">Available today</span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <HiCalendar />
          </div>
          <div className="stat-info">
            <h3>{stats.totalBookings}</h3>
            <p>Total Bookings</p>
            <span className="stat-detail">All time</span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <HiClipboardCheck />
          </div>
          <div className="stat-info">
            <h3>{stats.todayAttendance}</h3>
            <p>Today's Attendance</p>
            <span className="stat-detail">Check-ins</span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <HiUsers />
          </div>
          <div className="stat-info">
            <h3>{stats.totalTrainers}</h3>
            <p>Total Trainers</p>
            <span className="stat-detail">Active staff</span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <HiTrendingUp />
          </div>
          <div className="stat-info">
            <h3>{stats.upcomingClasses}</h3>
            <p>Upcoming Classes</p>
            <span className="stat-detail">Scheduled</span>
          </div>
        </div>

        <div className="stat-card revenue">
          <div className="stat-icon">
            <HiChartBar />
          </div>
          <div className="stat-info">
            <h3>Rp {(stats.totalRevenue / 1000000).toFixed(1)}M</h3>
            <p>Monthly Revenue</p>
            <span className="stat-detail">From memberships</span>
          </div>
        </div>

        <div className="stat-card highlight">
          <div className="stat-icon">
            <HiTrendingUp />
          </div>
          <div className="stat-info">
            <h3>{stats.bookingGrowth}%</h3>
            <p>Booking Growth</p>
            <span className="stat-detail">This week vs last</span>
          </div>
        </div>
      </div>

      {/* Additional Statistics Section */}
      <div className="additional-stats">
        <div className="stat-box">
          <div className="stat-box-header">
            <HiUsers className="stat-box-icon" />
            <h3>Total Users</h3>
          </div>
          <div className="stat-box-value">{stats.totalUsers}</div>
          <p className="stat-box-label">All system users</p>
        </div>

        <div className="stat-box">
          <div className="stat-box-header">
            <HiChartBar className="stat-box-icon" />
            <h3>Avg Bookings</h3>
          </div>
          <div className="stat-box-value">{stats.averageBookingsPerClass}</div>
          <p className="stat-box-label">Per class</p>
        </div>

        <div className="stat-box">
          <div className="stat-box-header">
            <HiCalendar className="stat-box-icon" />
            <h3>Most Active Day</h3>
          </div>
          <div className="stat-box-value">{stats.mostActiveDay}</div>
          <p className="stat-box-label">Highest bookings</p>
        </div>

        <div className="stat-box">
          <div className="stat-box-header">
            <HiAcademicCap className="stat-box-icon" />
            <h3>Class Capacity</h3>
          </div>
          <div className="stat-box-value">
            {stats.totalClasses > 0 
              ? ((stats.totalBookings / (stats.totalClasses * 20)) * 100).toFixed(1)
              : 0}%
          </div>
          <p className="stat-box-label">Overall utilization</p>
        </div>
      </div>

      {/* Membership Distribution */}
      <div className="membership-distribution">
        <h2>Membership Distribution</h2>
        <div className="membership-grid">
          <div className="membership-card basic">
            <div className="membership-icon"><RiMedalFill /></div>
            <h3>{stats.basicMembers}</h3>
            <p>Basic Members</p>
            <div className="membership-percentage">
              {stats.totalMembers > 0 ? Math.round((stats.basicMembers / stats.totalMembers) * 100) : 0}%
            </div>
          </div>

          <div className="membership-card premium">
            <div className="membership-icon"><RiUserStarFill /></div>
            <h3>{stats.premiumMembers}</h3>
            <p>Premium Members</p>
            <div className="membership-percentage">
              {stats.totalMembers > 0 ? Math.round((stats.premiumMembers / stats.totalMembers) * 100) : 0}%
            </div>
          </div>

          <div className="membership-card vip">
            <div className="membership-icon"><RiVipCrownFill /></div>
            <h3>{stats.vipMembers}</h3>
            <p>VIP Members</p>
            <div className="membership-percentage">
              {stats.totalMembers > 0 ? Math.round((stats.vipMembers / stats.totalMembers) * 100) : 0}%
            </div>
          </div>
        </div>
      </div>

      {/* Class Utilization & Membership Trend */}
      <div className="analytics-section">
        <div className="content-section">
          <h2>Class Utilization Rate</h2>
          <div className="utilization-list">
            {classUtilization.length > 0 ? (
              classUtilization.map((util, index) => (
                <div key={index} className="utilization-item">
                  <div className="util-info">
                    <h4>{util.name}</h4>
                    <p>{util.bookings} / {util.capacity} bookings</p>
                  </div>
                  <div className="util-bar-container">
                    <div 
                      className="util-bar" 
                      style={{
                        width: `${Math.min(util.percentage, 100)}%`,
                        backgroundColor: util.percentage >= 80 ? '#22c55e' : 
                                       util.percentage >= 50 ? '#fbbf24' : '#ef4444'
                      }}
                    />
                    <span className="util-percentage">{util.percentage}%</span>
                  </div>
                </div>
              ))
            ) : (
              <p className="no-data">No utilization data</p>
            )}
          </div>
        </div>

        <div className="content-section">
          <h2>Membership Growth Trend</h2>
          <div className="trend-chart">
            {membershipTrend.labels.length > 0 ? (
              <div className="simple-chart">
                {membershipTrend.labels.map((label, index) => (
                  <div key={index} className="chart-bar">
                    <div 
                      className="bar"
                      style={{
                        height: `${(membershipTrend.data[index] / Math.max(...membershipTrend.data)) * 100}%`
                      }}
                    >
                      <span className="bar-value">{membershipTrend.data[index]}</span>
                    </div>
                    <span className="bar-label">{label}</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="no-data">No trend data</p>
            )}
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
                    <h4>{booking.class?.name || `Class ID: ${booking.class_id}`}</h4>
                    <p>Member: {booking.member?.user?.name || `Member ID: ${booking.member_id}`}</p>
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
                    <p>{cls.description?.substring(0, 50)}...</p>
                  </div>
                  <div className="class-bookings">
                    <HiStar />
                    <span>{cls.bookingCount} bookings</span>
                  </div>
                </div>
              ))
            ) : (
              <p className="no-data">No class data</p>
            )}
          </div>
        </div>

        <div className="content-section">
          <h2>Recent Members</h2>
          <div className="recent-members">
            {recentMembers.length > 0 ? (
              recentMembers.map((member, index) => (
                <div key={index} className="member-item">
                  <div className="member-info">
                    <h4>{member.name}</h4>
                    <p>{member.email}</p>
                  </div>
                  <div className={`membership-badge ${member.membership_plan?.toLowerCase()}`}>
                    {member.membership_plan || 'Basic'}
                  </div>
                </div>
              ))
            ) : (
              <p className="no-data">No members yet</p>
            )}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="quick-actions">
        <h2>Quick Actions</h2>
        <div className="action-buttons">
          <button className="action-btn" onClick={() => navigate('/admin/members')}>
            <HiUsers />
            <span>Manage Members</span>
          </button>
          <button className="action-btn" onClick={() => navigate('/admin/classes')}>
            <HiAcademicCap />
            <span>Manage Classes</span>
          </button>
          <button className="action-btn" onClick={() => navigate('/admin/bookings')}>
            <HiCalendar />
            <span>View Bookings</span>
          </button>
          <button className="action-btn" onClick={() => navigate('/admin/attendance')}>
            <HiClipboardCheck />
            <span>Mark Attendance</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
