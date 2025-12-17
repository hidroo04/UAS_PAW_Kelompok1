import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  HiSearch, 
  HiCalendar, 
  HiClipboardCheck
} from 'react-icons/hi';
import apiClient from '../../services/api';
import './AdminBookings.css';

const AdminBookings = () => {
  const [bookings, setBookings] = useState([]);
  const [filteredBookings, setFilteredBookings] = useState([]);
  const [classes, setClasses] = useState([]);
  const [members, setMembers] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    
    if (!token || user.role !== 'admin') {
      navigate('/login');
      return;
    }
    
    fetchData();
  }, [navigate]);

  useEffect(() => {
    filterBookings();
  }, [searchTerm, bookings]);

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
        const className = getClassName(booking);
        const memberName = getMemberName(booking);
        return (
          className.toLowerCase().includes(searchTerm.toLowerCase()) ||
          memberName.toLowerCase().includes(searchTerm.toLowerCase())
        );
      });
    }

    setFilteredBookings(filtered);
  };

  const getClassName = (booking) => {
    // Try from nested class object first
    if (booking.class && booking.class.name) {
      return booking.class.name;
    }
    // Fallback to searching in classes array
    const cls = classes.find(c => c.id === booking.class_id);
    return cls ? cls.name : 'Unknown Class';
  };

  const getMemberName = (booking) => {
    // Try from nested member object first
    if (booking.member && booking.member.user && booking.member.user.name) {
      return booking.member.user.name;
    }
    // Fallback to searching in members array
    const member = members.find(m => m.id === booking.member_id);
    return member ? member.name : 'Unknown Member';
  };

  const handleCancelBooking = async (bookingId) => {
    if (!window.confirm('Are you sure you want to cancel this booking?')) {
      return;
    }

    try {
      const response = await apiClient.delete(`/bookings/${bookingId}`);
      console.log('Cancel response:', response);
      
      // Hapus booking dari list
      setBookings(prevBookings => prevBookings.filter(b => b.id !== bookingId));
      setFilteredBookings(prevFiltered => prevFiltered.filter(b => b.id !== bookingId));
      
      alert('Booking cancelled successfully!');
    } catch (err) {
      console.error('Cancel error:', err);
      console.error('Error response:', err.response?.data);
      const errorMessage = err.response?.data?.message || 'Failed to cancel booking';
      alert(`Error: ${errorMessage}`);
    }
  };

  const stats = {
    total: bookings.length
  };

  if (loading) {
    return <div className="admin-loading">Loading bookings...</div>;
  }

  return (
    <div className="admin-bookings">
      <div className="bookings-header">
        <h1>Bookings Management</h1>
      </div>

      {/* Toolbar: Total + Search dalam satu baris */}
      <div className="bookings-toolbar">
        <div className="total-badge">
          <HiClipboardCheck />
          <span><strong>{stats.total}</strong> Total Bookings</span>
        </div>
        
        <div className="search-box">
          <HiSearch />
          <input
            type="text"
            placeholder="Search by class or member name..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
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
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredBookings.length > 0 ? (
              filteredBookings.map((booking) => {
                return (
                  <tr key={booking.id}>
                    <td>{booking.id}</td>
                    <td>{getMemberName(booking)}</td>
                    <td>{getClassName(booking)}</td>
                    <td>
                      <div className="booking-date">
                        <HiCalendar />
                        <span>{new Date(booking.booking_date || Date.now()).toLocaleDateString()}</span>
                      </div>
                    </td>
                    <td className="actions">
                      <button 
                        className="btn-cancel-booking"
                        onClick={() => handleCancelBooking(booking.id)}
                      >
                        Cancel
                      </button>
                    </td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan="5" className="no-data">
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
