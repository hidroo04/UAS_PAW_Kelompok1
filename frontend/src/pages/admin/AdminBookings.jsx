import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  FaSearch, 
  FaCalendarAlt, 
  FaCheckCircle,
  FaTimesCircle,
  FaClock,
  FaFilter
} from 'react-icons/fa';
import apiClient from '../../services/api';
import './AdminBookings.css';

const AdminBookings = () => {
  const [bookings, setBookings] = useState([]);
  const [filteredBookings, setFilteredBookings] = useState([]);
  const [classes, setClasses] = useState([]);
  const [members, setMembers] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userRole = localStorage.getItem('userRole');
    
    if (!token || userRole !== 'admin') {
      navigate('/login');
      return;
    }
    
    fetchData();
  }, [navigate]);

  useEffect(() => {
    filterBookings();
  }, [searchTerm, statusFilter, bookings]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [bookingsRes, classesRes, membersRes] = await Promise.all([
        apiClient.get('/bookings'),
        apiClient.get('/classes'),
        apiClient.get('/users?role=member')
      ]);

      setBookings(bookingsRes.data.data || []);
      setClasses(classesRes.data.data || []);
      setMembers(membersRes.data.data || []);
    } catch (err) {
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  const filterBookings = () => {
    let filtered = [...bookings];

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(booking => {
        const className = getClassName(booking.class_id);
        const memberName = getMemberName(booking.member_id);
        return (
          className.toLowerCase().includes(searchTerm.toLowerCase()) ||
          memberName.toLowerCase().includes(searchTerm.toLowerCase())
        );
      });
    }

    // Filter by status
    if (statusFilter !== 'all') {
      filtered = filtered.filter(booking => 
        (booking.status || 'confirmed') === statusFilter
      );
    }

    setFilteredBookings(filtered);
  };

  const getClassName = (classId) => {
    const cls = classes.find(c => c.id === classId);
    return cls ? cls.name : 'Unknown Class';
  };

  const getMemberName = (memberId) => {
    const member = members.find(m => m.id === memberId);
    return member ? member.name : 'Unknown Member';
  };

  const handleCancelBooking = async (bookingId) => {
    if (!window.confirm('Are you sure you want to cancel this booking?')) {
      return;
    }

    try {
      await apiClient.delete(`/bookings/${bookingId}`);
      alert('Booking cancelled successfully!');
      fetchData();
    } catch (err) {
      alert('Failed to cancel booking');
      console.error(err);
    }
  };

  const getStatusBadge = (status) => {
    const statusLower = (status || 'confirmed').toLowerCase();
    const badges = {
      confirmed: { class: 'confirmed', icon: <FaCheckCircle />, text: 'Confirmed' },
      pending: { class: 'pending', icon: <FaClock />, text: 'Pending' },
      cancelled: { class: 'cancelled', icon: <FaTimesCircle />, text: 'Cancelled' }
    };
    return badges[statusLower] || badges.confirmed;
  };

  const stats = {
    total: bookings.length,
    confirmed: bookings.filter(b => (b.status || 'confirmed') === 'confirmed').length,
    pending: bookings.filter(b => b.status === 'pending').length,
    cancelled: bookings.filter(b => b.status === 'cancelled').length
  };

  if (loading) {
    return <div className="admin-loading">Loading bookings...</div>;
  }

  return (
    <div className="admin-bookings">
      <div className="bookings-header">
        <h1>Bookings Management</h1>
      </div>

      {/* Statistics */}
      <div className="booking-stats">
        <div className="stat-box total">
          <div className="stat-icon">
            <FaCalendarAlt />
          </div>
          <div className="stat-info">
            <h3>{stats.total}</h3>
            <p>Total Bookings</p>
          </div>
        </div>

        <div className="stat-box confirmed">
          <div className="stat-icon">
            <FaCheckCircle />
          </div>
          <div className="stat-info">
            <h3>{stats.confirmed}</h3>
            <p>Confirmed</p>
          </div>
        </div>

        <div className="stat-box pending">
          <div className="stat-icon">
            <FaClock />
          </div>
          <div className="stat-info">
            <h3>{stats.pending}</h3>
            <p>Pending</p>
          </div>
        </div>

        <div className="stat-box cancelled">
          <div className="stat-icon">
            <FaTimesCircle />
          </div>
          <div className="stat-info">
            <h3>{stats.cancelled}</h3>
            <p>Cancelled</p>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="bookings-filters">
        <div className="search-box">
          <FaSearch />
          <input
            type="text"
            placeholder="Search by class or member name..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <div className="status-filters">
          <button 
            className={statusFilter === 'all' ? 'active' : ''}
            onClick={() => setStatusFilter('all')}
          >
            All
          </button>
          <button 
            className={statusFilter === 'confirmed' ? 'active confirmed' : ''}
            onClick={() => setStatusFilter('confirmed')}
          >
            Confirmed
          </button>
          <button 
            className={statusFilter === 'pending' ? 'active pending' : ''}
            onClick={() => setStatusFilter('pending')}
          >
            Pending
          </button>
          <button 
            className={statusFilter === 'cancelled' ? 'active cancelled' : ''}
            onClick={() => setStatusFilter('cancelled')}
          >
            Cancelled
          </button>
        </div>
      </div>

      {/* Bookings Table */}
      <div className="bookings-table-container">
        <table className="bookings-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Member</th>
              <th>Class</th>
              <th>Booking Date</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredBookings.length > 0 ? (
              filteredBookings.map((booking) => {
                const badge = getStatusBadge(booking.status);
                return (
                  <tr key={booking.id}>
                    <td>{booking.id}</td>
                    <td>{getMemberName(booking.member_id)}</td>
                    <td>{getClassName(booking.class_id)}</td>
                    <td>
                      <div className="booking-date">
                        <FaCalendarAlt />
                        <span>{new Date(booking.booking_date || Date.now()).toLocaleDateString()}</span>
                      </div>
                    </td>
                    <td>
                      <span className={`status-badge ${badge.class}`}>
                        {badge.icon} {badge.text}
                      </span>
                    </td>
                    <td className="actions">
                      {booking.status !== 'cancelled' && (
                        <button 
                          className="btn-cancel-booking"
                          onClick={() => handleCancelBooking(booking.id)}
                        >
                          Cancel
                        </button>
                      )}
                    </td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan="6" className="no-data">
                  No bookings found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AdminBookings;
