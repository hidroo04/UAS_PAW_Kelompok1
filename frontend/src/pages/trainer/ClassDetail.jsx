import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';
import Loading from '../../components/Loading';
import { FaArrowLeft, FaCalendar, FaUsers, FaTrash, FaCheckCircle, FaUserCheck, FaUserTimes } from 'react-icons/fa';
import './ClassDetail.css';

const ClassDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [classData, setClassData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [removingMember, setRemovingMember] = useState(null);
  const [markingAttendance, setMarkingAttendance] = useState(null);

  useEffect(() => {
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user || user.role !== 'trainer') {
      navigate('/login');
      return;
    }
    fetchClassDetail();
  }, [id, navigate]);

  const fetchClassDetail = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await api.get('/trainer/classes');
      
      if (response.data.status === 'success') {
        const foundClass = response.data.data.find(cls => cls.id === parseInt(id));
        if (foundClass) {
          setClassData(foundClass);
        } else {
          setError('Class not found');
        }
      } else {
        setError('Failed to load class details');
      }
    } catch (err) {
      console.error('Error fetching class detail:', err);
      if (err.response?.status === 401) {
        setError('Session expired. Please login again');
        setTimeout(() => navigate('/login'), 2000);
      } else {
        setError(err.response?.data?.message || 'Failed to load class details');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleMarkAttendance = async (bookingId, memberName, markAsPresent) => {
    const statusText = markAsPresent ? 'present' : 'absent';
    
    if (!window.confirm(`Mark ${memberName} as ${statusText}?`)) {
      return;
    }

    try {
      setMarkingAttendance(`${bookingId}-${markAsPresent ? 'present' : 'absent'}`);
      
      const response = await api.post(`/trainer/classes/${id}/attendance/${bookingId}`, {
        attended: markAsPresent
      });
      
      if (response.data.status === 'success') {
        await fetchClassDetail();
        // Success notification handled by UI update
      } else {
        alert('Failed to mark attendance: ' + (response.data.message || 'Unknown error'));
      }
    } catch (err) {
      console.error('Error marking attendance:', err);
      alert(err.response?.data?.message || 'Failed to mark attendance');
    } finally {
      setMarkingAttendance(null);
    }
  };

  const handleRemoveMember = async (bookingId, memberName) => {
    if (!window.confirm(`Are you sure you want to remove ${memberName} from this class?\n\nThis member will no longer see this class in their bookings.`)) {
      return;
    }

    try {
      setRemovingMember(bookingId);
      
      const response = await api.delete(`/trainer/classes/${id}/members/${bookingId}`);
      
      if (response.data.status === 'success') {
        await fetchClassDetail();
        alert(response.data.message || 'Member successfully removed from class');
      } else {
        alert('Failed to remove member: ' + (response.data.message || 'Unknown error'));
      }
    } catch (err) {
      console.error('Error removing member:', err);
      alert(err.response?.data?.message || 'Failed to remove member from class');
    } finally {
      setRemovingMember(null);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
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
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) return <Loading />;

  if (error) {
    return (
      <div className="class-detail-container">
        <div className="error-message">
          <p>{error}</p>
          <button onClick={() => navigate('/trainer/my-classes')}>Back to My Classes</button>
        </div>
      </div>
    );
  }

  if (!classData) {
    return (
      <div className="class-detail-container">
        <div className="error-message">
          <p>Class not found</p>
          <button onClick={() => navigate('/trainer/my-classes')}>Back to My Classes</button>
        </div>
      </div>
    );
  }

  return (
    <div className="class-detail-container">
      {/* Header */}
      <div className="class-detail-header">
        <button className="btn-back" onClick={() => navigate('/trainer/my-classes')}>
          <FaArrowLeft /> Back to My Classes
        </button>
        <div className="header-content">
          <span className="class-badge">Class Management</span>
          <h1>{classData.name}</h1>
          <p className="class-description-header">{classData.description}</p>
        </div>
      </div>

      {/* Class Info Cards */}
      <div className="class-info-grid">
        <div className="info-card">
          <div className="info-icon">
            <FaCalendar />
          </div>
          <div className="info-content">
            <span className="info-label">Schedule</span>
            <span className="info-value">{formatDate(classData.schedule)}</span>
          </div>
        </div>

        <div className="info-card">
          <div className="info-icon">
            <FaUsers />
          </div>
          <div className="info-content">
            <span className="info-label">Enrollment</span>
            <span className="info-value">{classData.enrolled_count} / {classData.capacity} Members</span>
          </div>
        </div>

        <div className="info-card">
          <div className="info-icon">
            <FaCheckCircle />
          </div>
          <div className="info-content">
            <span className="info-label">Available Slots</span>
            <span className={`info-value ${classData.available_slots === 0 ? 'full' : 'available'}`}>
              {classData.available_slots === 0 ? 'Full' : `${classData.available_slots} Slots`}
            </span>
          </div>
        </div>
      </div>

      {/* Members Section */}
      <div className="members-section">
        <div className="section-header">
          <h2>Enrolled Members ({classData.members?.length || 0})</h2>
        </div>

        {classData.members && classData.members.length > 0 ? (
          <div className="members-table-container">
            <table className="members-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Membership</th>
                  <th>Attendance</th>
                  <th>Joined Date</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {classData.members.map((member, index) => {
                  const isPresent = member.attendance?.attended || false;
                  const hasAttendance = member.attendance !== null;
                  
                  return (
                    <tr key={member.booking_id || index}>
                      <td>{index + 1}</td>
                      <td>
                        <div className="member-name-cell">
                          <div className={`member-avatar-small ${isPresent ? 'present' : hasAttendance ? 'absent' : ''}`}>
                            {member.name.charAt(0).toUpperCase()}
                            {hasAttendance && (
                              <span className="attendance-indicator-small">
                                {isPresent ? '✓' : '✗'}
                              </span>
                            )}
                          </div>
                          <span>{member.name}</span>
                        </div>
                      </td>
                      <td className="email-cell">{member.email}</td>
                      <td>
                        <span className={`membership-badge ${member.membership_plan?.toLowerCase()}`}>
                          {member.membership_plan || 'N/A'}
                        </span>
                      </td>
                      <td>
                        {hasAttendance ? (
                          <span className={`attendance-badge-table ${isPresent ? 'present' : 'absent'}`}>
                            {isPresent ? (
                              <>
                                <FaUserCheck /> Present
                              </>
                            ) : (
                              <>
                                <FaUserTimes /> Absent
                              </>
                            )}
                          </span>
                        ) : (
                          <span className="attendance-badge-table pending">
                            Not Marked
                          </span>
                        )}
                      </td>
                      <td className="date-cell">
                        {formatBookingDate(member.booking_date)}
                      </td>
                      <td>
                        <div className="action-buttons-table">
                          <button
                            className={`btn-attendance-table present ${isPresent ? 'active' : ''}`}
                            onClick={() => handleMarkAttendance(member.booking_id, member.name, true)}
                            disabled={markingAttendance?.startsWith(`${member.booking_id}-`)}
                            title="Mark as Present"
                          >
                            {markingAttendance === `${member.booking_id}-present` ? (
                              '...'
                            ) : (
                              <FaUserCheck />
                            )}
                          </button>
                          <button
                            className={`btn-attendance-table absent ${hasAttendance && !isPresent ? 'active' : ''}`}
                            onClick={() => handleMarkAttendance(member.booking_id, member.name, false)}
                            disabled={markingAttendance?.startsWith(`${member.booking_id}-`)}
                            title="Mark as Absent"
                          >
                            {markingAttendance === `${member.booking_id}-absent` ? (
                              '...'
                            ) : (
                              <FaUserTimes />
                            )}
                          </button>
                          <button
                            className="btn-remove-table"
                            onClick={() => handleRemoveMember(member.booking_id, member.name)}
                            disabled={removingMember === member.booking_id}
                            title="Remove Member"
                          >
                            <FaTrash />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="no-members">
            <div className="no-members-icon">👥</div>
            <p>No members enrolled in this class yet.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ClassDetail;
