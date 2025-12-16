import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import Loading from '../../components/Loading';
import './MyClasses.css';

const MyClasses = () => {
  const [classes, setClasses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user || user.role !== 'trainer') {
      navigate('/login');
      return;
    }
    fetchMyClasses();
  }, [navigate]);

  const fetchMyClasses = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Use dedicated trainer endpoint (no /api prefix, it's in baseURL)
      const response = await api.get('/trainer/classes');
      
      if (response.data.status === 'success') {
        setClasses(response.data.data);
      } else {
        setError('Failed to load classes');
      }
    } catch (err) {
      console.error('Error fetching classes:', err);
      if (err.response?.status === 401) {
        setError('Session expired. Please login again');
        setTimeout(() => navigate('/login'), 2000);
      } else {
        setError(err.response?.data?.message || 'Failed to load your classes');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleClassClick = (classId) => {
    navigate(`/trainer/my-classes/${classId}`);
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleString('id-ID', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatBookingDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleString('id-ID', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) return <Loading />;

  return (
    <div className="my-classes-container">
      <div className="my-classes-header">
        <span className="header-badge">Trainer Dashboard</span>
        <h1>My Classes</h1>
        <p>Manage your classes and view enrolled members</p>
      </div>

      {error && (
        <div className="error-message">
          <p>{error}</p>
          <button onClick={fetchMyClasses}>Try Again</button>
        </div>
      )}

      {!error && classes.length === 0 && (
        <div className="no-classes">
          <div className="no-classes-icon">📚</div>
          <p>You don't have any assigned classes yet.</p>
        </div>
      )}

      <div className="classes-list">
        {classes.map((cls) => (
          <div 
            key={cls.id} 
            className="class-card"
            onClick={() => handleClassClick(cls.id)}
            style={{ cursor: 'pointer' }}
          >
            <div className="class-header">
              <div className="class-info">
                <h2>{cls.name}</h2>
                <p className="class-description">{cls.description}</p>
                <div className="class-details">
                  <span className="class-schedule">
                    📅 {formatDate(cls.schedule)}
                  </span>
                  <span className="class-capacity">
                    👥 {cls.enrolled_count || 0} / {cls.capacity} Members
                  </span>
                  <span className={`class-status ${cls.available_slots === 0 ? 'full' : 'available'}`}>
                    {cls.available_slots === 0 ? '⚠️ Full' : `✅ ${cls.available_slots} Slots Available`}
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MyClasses;
