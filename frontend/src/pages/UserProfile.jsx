import { useState, useEffect } from 'react';
import { 
  HiUser, 
  HiCreditCard, 
  HiCalendar, 
  HiChartBar, 
  HiPencil, 
  HiLogout,
  HiCheckCircle,
  HiClock,
  HiAcademicCap,
  HiUsers,
  HiClipboardCheck
} from 'react-icons/hi';
import { RiMedalFill, RiUserStarFill, RiVipCrownFill } from 'react-icons/ri';
import { useNavigate } from 'react-router-dom';
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
  const [showPasswordModal, setShowPasswordModal] = useState(false);
  const [passwordData, setPasswordData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    address: ''
  });

  useEffect(() => {
    fetchUserData();
  }, []);

  useEffect(() => {
    // Only fetch booking/attendance/membership data for members
    if (userData?.role === 'member') {
      if (activeTab === 'bookings') {
        fetchBookings();
      } else if (activeTab === 'attendance') {
        fetchAttendance();
      } else if (activeTab === 'membership') {
        fetchMembership();
      }
    }
  }, [activeTab, userData]);

  const fetchUserData = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/profile');
      const profileData = response.data.data;
      setUserData(profileData);
      setFormData({
        name: profileData.name || '',
        email: profileData.email || '',
        phone: profileData.phone || '',
        address: profileData.address || ''
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
      if (response.data.status === 'success') {
        const bookingsData = response.data.data || [];
        setBookings(bookingsData);
      } else {
        setBookings([]);
      }
    } catch (err) {
      console.error('Error fetching bookings:', err);
      setBookings([]);
    }
  };

  const fetchAttendance = async () => {
    try {
      // Ambil dari bookings karena attendance ada di dalam data bookings
      const response = await apiClient.get('/bookings/my');
      if (response.data.status === 'success') {
        // Filter bookings yang sudah ada attendance
        const attendedClasses = (response.data.data || []).filter(booking => 
          booking.attendance !== null && booking.attendance !== undefined
        );
        setAttendance(attendedClasses);
      } else {
        setAttendance([]);
      }
    } catch (err) {
      console.error('Error fetching attendance:', err);
      setAttendance([]);
    }
  };

  const fetchMembership = async () => {
    try {
      // Gunakan data dari userData yang sudah berisi info member
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
    } catch (err) {
      console.error('Error fetching membership:', err);
    }
  };

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    try {
      const response = await apiClient.put('/profile/update', formData);
      setUserData(response.data.data);
      setEditMode(false);
      alert('Profile updated successfully!');
    } catch (err) {
      console.error('Error updating profile:', err);
      alert(err.response?.data?.message || 'Failed to update profile');
    }
  };

  const handleChangePassword = async (e) => {
    e.preventDefault();
    
    if (passwordData.new_password !== passwordData.confirm_password) {
      alert('New password and confirm password do not match');
      return;
    }

    if (passwordData.new_password.length < 6) {
      alert('Password must be at least 6 characters');
      return;
    }

    try {
      await apiClient.put('/profile/change-password', {
        current_password: passwordData.current_password,
        new_password: passwordData.new_password
      });
      alert('Password changed successfully!');
      setShowPasswordModal(false);
      setPasswordData({
        current_password: '',
        new_password: '',
        confirm_password: ''
      });
    } catch (err) {
      console.error('Error changing password:', err);
      alert(err.response?.data?.message || 'Failed to change password');
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
          {userData?.name?.charAt(0).toUpperCase() || 'U'}
        </div>
        <div className="profile-info">
          <h2>{userData?.name}</h2>
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
            <label>Address</label>
            <span>{userData?.address || 'Not provided'}</span>
          </div>
          <div className="detail-row">
            <label>Role</label>
            <span className={`role-badge role-${userData?.role}`}>
              {userData?.role === 'admin' && <HiUsers />}
              {userData?.role === 'trainer' && <HiAcademicCap />}
              {userData?.role === 'member' && <HiUser />}
              {userData?.role}
            </span>
          </div>
          {userData?.membership_plan && (
            <>
              <div className="detail-row">
                <label>Membership Plan</label>
                <span className={`membership-badge ${userData.membership_plan.toLowerCase()}`}>
                  {userData.membership_plan === 'Basic' && <RiMedalFill />}
                  {userData.membership_plan === 'Premium' && <RiUserStarFill />}
                  {userData.membership_plan === 'VIP' && <RiVipCrownFill />}
                  {userData.membership_plan}
                </span>
              </div>
              <div className="detail-row">
                <label>Status</label>
                <span className={`status-badge ${userData.membership_status}`}>
                  {userData.membership_status}
                </span>
              </div>
              {userData.membership_expiry && (
                <div className="detail-row">
                  <label>Expires</label>
                  <span>{new Date(userData.membership_expiry).toLocaleDateString()}</span>
                </div>
              )}
            </>
          )}
          <div className="profile-actions">
            <button className="btn-edit" onClick={() => setEditMode(true)}>
              <HiPencil /> Edit Profile
            </button>
            <button className="btn-change-password" onClick={() => setShowPasswordModal(true)}>
              Change Password
            </button>
          </div>
        </div>
      ) : (
        <form className="profile-edit-form" onSubmit={handleUpdateProfile}>
          <div className="form-group">
            <label>Full Name</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
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
              placeholder="08123456789"
            />
          </div>
          <div className="form-group">
            <label>Address</label>
            <textarea
              value={formData.address}
              onChange={(e) => setFormData({ ...formData, address: e.target.value })}
              placeholder="Enter your address"
              rows="3"
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
      <div className="section-header">
        <h3>My Bookings</h3>
        <p className="section-subtitle">View all your class bookings</p>
      </div>
      {bookings.length === 0 ? (
        <div className="no-data-card">
          <HiCalendar size={48} />
          <p>No bookings found</p>
          <small>Book a class to get started!</small>
        </div>
      ) : (
        <div className="bookings-list">
          {bookings.map((booking) => (
            <div key={booking.id} className="booking-item">
              <div className="booking-header">
                <h4>{booking.class?.name || 'Class'}</h4>
                <span className="booking-status status-confirmed">
                  Confirmed
                </span>
              </div>
              <div className="booking-details">
                <div className="detail-item">
                  <HiCalendar />
                  <span>{booking.class?.schedule ? new Date(booking.class.schedule).toLocaleDateString('en-US', {
                    weekday: 'short',
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                  }) : 'N/A'}</span>
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
        </div>
      )}
    </div>
  );

  const renderAttendanceTab = () => {
    const presentCount = attendance.filter(a => a.attendance?.attended === true).length;
    const absentCount = attendance.filter(a => a.attendance?.attended === false).length;
    
    return (
      <div className="attendance-content">
        <div className="section-header">
          <h3>Attendance History</h3>
          <p className="section-subtitle">Track your class attendance</p>
        </div>
        <div className="attendance-stats">
          <div className="stat-card">
            <div className="stat-icon">
              <HiClipboardCheck />
            </div>
            <div className="stat-info">
              <h4>{attendance.length}</h4>
              <p>Total Classes</p>
            </div>
          </div>
          <div className="stat-card present">
            <div className="stat-icon">
              <HiCheckCircle />
            </div>
            <div className="stat-info">
              <h4>{presentCount}</h4>
              <p>Present</p>
            </div>
          </div>
          <div className="stat-card absent">
            <div className="stat-icon">
              <HiClock />
            </div>
            <div className="stat-info">
              <h4>{absentCount}</h4>
              <p>Absent</p>
            </div>
          </div>
        </div>
        {attendance.length === 0 ? (
          <div className="no-data-card">
            <HiClipboardCheck size={48} />
            <p>No attendance records found</p>
            <small>Attend classes to see your records here</small>
          </div>
        ) : (
          <div className="attendance-list">
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
                    <span>{record.class?.schedule ? new Date(record.class.schedule).toLocaleDateString('en-US', {
                      weekday: 'short',
                      month: 'short',
                      day: 'numeric',
                      year: 'numeric'
                    }) : 'N/A'}</span>
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
          </div>
        )}
      </div>
    );
  };

  const renderMembershipTab = () => (
    <div className="membership-content">
      <div className="section-header">
        <h3>Membership Details</h3>
        <p className="section-subtitle">Your membership information</p>
      </div>
      {membership ? (
        <div className="membership-card">
          <div className="membership-header">
            <div className="membership-icon">
              {membership.plan === 'VIP' && <RiVipCrownFill size={48} />}
              {membership.plan === 'Premium' && <RiUserStarFill size={48} />}
              {membership.plan === 'Basic' && <RiMedalFill size={48} />}
            </div>
            <div className="membership-title">
              <h4>{membership.plan || 'Basic'} Membership</h4>
              <span className={`status-badge ${membership.status?.toLowerCase() || 'active'}`}>
                {membership.status || 'Active'}
              </span>
            </div>
          </div>
          <div className="membership-details">
            {membership.expiry && (
              <div className="detail-row">
                <label><HiCalendar /> Expires On</label>
                <span>{new Date(membership.expiry).toLocaleDateString()}</span>
              </div>
            )}
            <div className="detail-row">
              <label><HiClipboardCheck /> Total Bookings</label>
              <span>{membership.total_bookings || bookings.length}</span>
            </div>
            <div className="detail-row">
              <label><HiCheckCircle /> Classes Attended</label>
              <span>{membership.total_attended || attendance.length}</span>
            </div>
          </div>
          <div className="membership-benefits">
            <h5>Membership Benefits</h5>
            <ul>
              {membership.plan === 'VIP' && (
                <>
                  <li>✓ Unlimited class bookings</li>
                  <li>✓ Priority booking access</li>
                  <li>✓ Free personal training sessions</li>
                  <li>✓ Access to premium equipment</li>
                </>
              )}
              {membership.plan === 'Premium' && (
                <>
                  <li>✓ Up to 20 classes per month</li>
                  <li>✓ Priority booking</li>
                  <li>✓ Group training sessions</li>
                </>
              )}
              {membership.plan === 'Basic' && (
                <>
                  <li>✓ Up to 10 classes per month</li>
                  <li>✓ Access to basic equipment</li>
                  <li>✓ Standard booking</li>
                </>
              )}
            </ul>
          </div>
        </div>
      ) : (
        <div className="no-data-card">
          <HiCreditCard size={48} />
          <p>No membership information available</p>
          <small>Contact admin for membership details</small>
        </div>
      )}
    </div>
  );

  const oldRenderMembershipTab = () => (
    <div className="membership-content">
      <h3>Membership Details</h3>
      {membership ? (
        <div className="membership-card">
          <div className="membership-header">
            <HiCreditCard size={40} />
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
              <HiUser /> Profile
            </button>
            {userData?.role === 'member' && (
              <>
                <button
                  className={`tab-button ${activeTab === 'bookings' ? 'active' : ''}`}
                  onClick={() => setActiveTab('bookings')}
                >
                  <HiCalendar /> Bookings
                </button>
                <button
                  className={`tab-button ${activeTab === 'attendance' ? 'active' : ''}`}
                  onClick={() => setActiveTab('attendance')}
                >
                  <HiChartBar /> Attendance
                </button>
                <button
                  className={`tab-button ${activeTab === 'membership' ? 'active' : ''}`}
                  onClick={() => setActiveTab('membership')}
                >
                  <HiCreditCard /> Membership
                </button>
              </>
            )}
            <button className="tab-button logout" onClick={handleLogout}>
              <HiLogout /> Logout
            </button>
          </nav>
        </div>

        <div className="profile-main">
          {activeTab === 'profile' && renderProfileTab()}
          {userData?.role === 'member' && activeTab === 'bookings' && renderBookingsTab()}
          {userData?.role === 'member' && activeTab === 'attendance' && renderAttendanceTab()}
          {userData?.role === 'member' && activeTab === 'membership' && renderMembershipTab()}
        </div>
      </div>

      {/* Change Password Modal */}
      {showPasswordModal && (
        <div className="modal-overlay" onClick={() => setShowPasswordModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>Change Password</h3>
            <form onSubmit={handleChangePassword}>
              <div className="form-group">
                <label>Current Password</label>
                <input
                  type="password"
                  value={passwordData.current_password}
                  onChange={(e) => setPasswordData({ ...passwordData, current_password: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label>New Password</label>
                <input
                  type="password"
                  value={passwordData.new_password}
                  onChange={(e) => setPasswordData({ ...passwordData, new_password: e.target.value })}
                  required
                  minLength="6"
                />
              </div>
              <div className="form-group">
                <label>Confirm New Password</label>
                <input
                  type="password"
                  value={passwordData.confirm_password}
                  onChange={(e) => setPasswordData({ ...passwordData, confirm_password: e.target.value })}
                  required
                  minLength="6"
                />
              </div>
              <div className="modal-actions">
                <button type="submit" className="btn-primary">Change Password</button>
                <button type="button" className="btn-secondary" onClick={() => setShowPasswordModal(false)}>
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserProfile;
