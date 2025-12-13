import { useState, useEffect } from 'react';
import { FaUser, FaCreditCard, FaCalendarAlt, FaChartLine, FaEdit, FaSignOutAlt } from 'react-icons/fa';
import apiClient from '../services/api';
import './UserProfile.css';

const UserProfile = () => {
  const [activeTab, setActiveTab] = useState('profile');
  const [userData, setUserData] = useState(null);
  const [bookings, setBookings] = useState([]);
  const [attendance, setAttendance] = useState([]);
  const [membership, setMembership] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    phone: ''
  });

  useEffect(() => {
    fetchUserData();
  }, []);

  useEffect(() => {
    if (activeTab === 'bookings') {
      fetchBookings();
    } else if (activeTab === 'attendance') {
      fetchAttendance();
    } else if (activeTab === 'membership') {
      fetchMembership();
    }
  }, [activeTab]);

  const fetchUserData = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/auth/me');
      setUserData(response.data);
      setFormData({
        full_name: response.data.full_name,
        email: response.data.email,
        phone: response.data.phone || ''
      });
      setError(null);
    } catch (err) {
      console.error('Error fetching user data:', err);
      setError('Failed to load profile information');
    } finally {
      setLoading(false);
    }
  };

  const fetchBookings = async () => {
    try {
      const response = await apiClient.get('/bookings/my');
      setBookings(response.data);
    } catch (err) {
      console.error('Error fetching bookings:', err);
    }
  };

  const fetchAttendance = async () => {
    try {
      const response = await apiClient.get('/attendance/my');
      setAttendance(response.data);
    } catch (err) {
      console.error('Error fetching attendance:', err);
    }
  };

  const fetchMembership = async () => {
    try {
      const response = await apiClient.get('/membership/status');
      setMembership(response.data);
    } catch (err) {
      console.error('Error fetching membership:', err);
    }
  };

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    try {
      const response = await apiClient.put('/auth/profile', formData);
      setUserData(response.data);
      setEditMode(false);
      alert('Profile updated successfully!');
    } catch (err) {
      console.error('Error updating profile:', err);
      alert('Failed to update profile');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/login';
  };

  const renderProfileTab = () => (
    <div className="profile-content">
      <div className="profile-header">
        <div className="profile-avatar">
          {userData?.full_name?.charAt(0).toUpperCase() || 'U'}
        </div>
        <div className="profile-info">
          <h2>{userData?.full_name}</h2>
          <p className="member-since">Member since {new Date(userData?.created_at).toLocaleDateString()}</p>
        </div>
      </div>

      {!editMode ? (
        <div className="profile-details">
          <div className="detail-row">
            <label>Email</label>
            <span>{userData?.email}</span>
          </div>
          <div className="detail-row">
            <label>Phone</label>
            <span>{userData?.phone || 'Not provided'}</span>
          </div>
          <div className="detail-row">
            <label>Role</label>
            <span className="role-badge">{userData?.role}</span>
          </div>
          <button className="btn-edit" onClick={() => setEditMode(true)}>
            <FaEdit /> Edit Profile
          </button>
        </div>
      ) : (
        <form className="profile-edit-form" onSubmit={handleUpdateProfile}>
          <div className="form-group">
            <label>Full Name</label>
            <input
              type="text"
              value={formData.full_name}
              onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label>Phone</label>
            <input
              type="tel"
              value={formData.phone}
              onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
            />
          </div>
          <div className="form-actions">
            <button type="submit" className="btn-primary">Save Changes</button>
            <button type="button" className="btn-secondary" onClick={() => setEditMode(false)}>
              Cancel
            </button>
          </div>
        </form>
      )}
    </div>
  );

  const renderBookingsTab = () => (
    <div className="bookings-content">
      <h3>My Bookings</h3>
      {bookings.length === 0 ? (
        <p className="no-data">No bookings found</p>
      ) : (
        <div className="bookings-list">
          {bookings.map((booking) => (
            <div key={booking.id} className="booking-item">
              <div className="booking-info">
                <h4>{booking.class_name}</h4>
                <p className="booking-date">
                  <FaCalendarAlt /> {new Date(booking.class_date).toLocaleDateString()} at {booking.class_time}
                </p>
                <span className={`booking-status status-${booking.status}`}>
                  {booking.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );

  const renderAttendanceTab = () => (
    <div className="attendance-content">
      <h3>Attendance History</h3>
      <div className="attendance-stats">
        <div className="stat-card">
          <FaChartLine />
          <div>
            <h4>{attendance.length}</h4>
            <p>Total Classes Attended</p>
          </div>
        </div>
        <div className="stat-card">
          <FaCalendarAlt />
          <div>
            <h4>{attendance.filter(a => a.status === 'present').length}</h4>
            <p>Present</p>
          </div>
        </div>
      </div>
      {attendance.length === 0 ? (
        <p className="no-data">No attendance records found</p>
      ) : (
        <div className="attendance-list">
          {attendance.map((record) => (
            <div key={record.id} className="attendance-item">
              <div className="attendance-info">
                <h4>{record.class_name}</h4>
                <p>{new Date(record.date).toLocaleDateString()}</p>
              </div>
              <span className={`status-badge status-${record.status}`}>
                {record.status}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );

  const renderMembershipTab = () => (
    <div className="membership-content">
      <h3>Membership Details</h3>
      {membership ? (
        <div className="membership-card">
          <div className="membership-header">
            <FaCreditCard size={40} />
            <h4>{membership.plan_name}</h4>
          </div>
          <div className="membership-details">
            <div className="detail-row">
              <label>Status</label>
              <span className={`status-badge status-${membership.status}`}>
                {membership.status}
              </span>
            </div>
            <div className="detail-row">
              <label>Start Date</label>
              <span>{new Date(membership.start_date).toLocaleDateString()}</span>
            </div>
            <div className="detail-row">
              <label>End Date</label>
              <span>{new Date(membership.end_date).toLocaleDateString()}</span>
            </div>
            <div className="detail-row">
              <label>Days Remaining</label>
              <span className="highlight">
                {Math.ceil((new Date(membership.end_date) - new Date()) / (1000 * 60 * 60 * 24))} days
              </span>
            </div>
          </div>
        </div>
      ) : (
        <div className="no-membership">
          <p>No active membership</p>
          <button className="btn-primary" onClick={() => window.location.href = '/membership'}>
            View Plans
          </button>
        </div>
      )}
    </div>
  );

  if (loading) {
    return <div className="loading">Loading profile...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="user-profile-page">
      <div className="profile-container">
        <div className="profile-sidebar">
          <nav className="profile-tabs">
            <button
              className={`tab-button ${activeTab === 'profile' ? 'active' : ''}`}
              onClick={() => setActiveTab('profile')}
            >
              <FaUser /> Profile
            </button>
            <button
              className={`tab-button ${activeTab === 'bookings' ? 'active' : ''}`}
              onClick={() => setActiveTab('bookings')}
            >
              <FaCalendarAlt /> Bookings
            </button>
            <button
              className={`tab-button ${activeTab === 'attendance' ? 'active' : ''}`}
              onClick={() => setActiveTab('attendance')}
            >
              <FaChartLine /> Attendance
            </button>
            <button
              className={`tab-button ${activeTab === 'membership' ? 'active' : ''}`}
              onClick={() => setActiveTab('membership')}
            >
              <FaCreditCard /> Membership
            </button>
            <button className="tab-button logout" onClick={handleLogout}>
              <FaSignOutAlt /> Logout
            </button>
          </nav>
        </div>

        <div className="profile-main">
          {activeTab === 'profile' && renderProfileTab()}
          {activeTab === 'bookings' && renderBookingsTab()}
          {activeTab === 'attendance' && renderAttendanceTab()}
          {activeTab === 'membership' && renderMembershipTab()}
        </div>
      </div>
    </div>
  );
};

export default UserProfile;
