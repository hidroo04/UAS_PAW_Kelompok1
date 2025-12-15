import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  FaCalendarAlt, 
  FaUserCheck,
  FaUserTimes,
  FaCheckCircle,
  FaTimesCircle,
  FaDumbbell
} from 'react-icons/fa';
import apiClient from '../../services/api';
import './AdminAttendance.css';

const AdminAttendance = () => {
  const [attendance, setAttendance] = useState([]);
  const [classes, setClasses] = useState([]);
  const [members, setMembers] = useState([]);
  const [selectedClass, setSelectedClass] = useState('');
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [loading, setLoading] = useState(true);
  const [showMarkModal, setShowMarkModal] = useState(false);
  const [markFormData, setMarkFormData] = useState({
    member_id: '',
    class_id: '',
    date: '',
    status: 'present'
  });
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

  const fetchData = async () => {
    try {
      setLoading(true);
      const [attendanceRes, classesRes, membersRes] = await Promise.all([
        apiClient.get('/attendance'),
        apiClient.get('/classes'),
        apiClient.get('/users?role=member')
      ]);

      setAttendance(attendanceRes.data.data || []);
      setClasses(classesRes.data.data || []);
      setMembers(membersRes.data.data || []);
    } catch (err) {
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  const getClassName = (classId) => {
    const cls = classes.find(c => c.id === classId);
    return cls ? cls.name : 'Unknown Class';
  };

  const getMemberName = (memberId) => {
    const member = members.find(m => m.id === memberId);
    return member ? member.name : 'Unknown Member';
  };

  const handleMarkAttendance = async (e) => {
    e.preventDefault();
    
    try {
      await apiClient.post('/attendance', markFormData);
      alert('Attendance marked successfully!');
      setShowMarkModal(false);
      setMarkFormData({ member_id: '', class_id: '', date: '', status: 'present' });
      fetchData();
    } catch (err) {
      alert('Failed to mark attendance');
      console.error(err);
    }
  };

  const filterAttendance = () => {
    let filtered = [...attendance];

    if (selectedClass) {
      filtered = filtered.filter(a => a.class_id === parseInt(selectedClass));
    }

    if (selectedDate) {
      filtered = filtered.filter(a => {
        const attDate = new Date(a.date).toISOString().split('T')[0];
        return attDate === selectedDate;
      });
    }

    return filtered;
  };

  const filteredAttendance = filterAttendance();

  const stats = {
    total: attendance.length,
    present: attendance.filter(a => a.status === 'present').length,
    absent: attendance.filter(a => a.status === 'absent').length,
    rate: attendance.length > 0 
      ? Math.round((attendance.filter(a => a.status === 'present').length / attendance.length) * 100) 
      : 0
  };

  if (loading) {
    return <div className="admin-loading">Loading attendance data...</div>;
  }

  return (
    <div className="admin-attendance">
      <div className="attendance-header">
        <h1>Attendance Management</h1>
        <button 
          className="btn-mark-attendance"
          onClick={() => {
            setMarkFormData({ 
              member_id: '', 
              class_id: '', 
              date: new Date().toISOString().split('T')[0], 
              status: 'present' 
            });
            setShowMarkModal(true);
          }}
        >
          <FaUserCheck /> Mark Attendance
        </button>
      </div>

      {/* Statistics */}
      <div className="attendance-stats">
        <div className="stat-card total">
          <div className="stat-icon">
            <FaCalendarAlt />
          </div>
          <div className="stat-info">
            <h3>{stats.total}</h3>
            <p>Total Records</p>
          </div>
        </div>

        <div className="stat-card present">
          <div className="stat-icon">
            <FaUserCheck />
          </div>
          <div className="stat-info">
            <h3>{stats.present}</h3>
            <p>Present</p>
          </div>
        </div>

        <div className="stat-card absent">
          <div className="stat-icon">
            <FaUserTimes />
          </div>
          <div className="stat-info">
            <h3>{stats.absent}</h3>
            <p>Absent</p>
          </div>
        </div>

        <div className="stat-card rate">
          <div className="stat-icon">
            <FaCheckCircle />
          </div>
          <div className="stat-info">
            <h3>{stats.rate}%</h3>
            <p>Attendance Rate</p>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="attendance-filters">
        <div className="filter-group">
          <label>Class</label>
          <select 
            value={selectedClass} 
            onChange={(e) => setSelectedClass(e.target.value)}
          >
            <option value="">All Classes</option>
            {classes.map(cls => (
              <option key={cls.id} value={cls.id}>{cls.name}</option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label>Date</label>
          <input
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
          />
        </div>

        <button 
          className="btn-reset-filter"
          onClick={() => {
            setSelectedClass('');
            setSelectedDate(new Date().toISOString().split('T')[0]);
          }}
        >
          Reset Filters
        </button>
      </div>

      {/* Attendance Table */}
      <div className="attendance-table-container">
        <table className="attendance-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Member</th>
              <th>Class</th>
              <th>Date</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {filteredAttendance.length > 0 ? (
              filteredAttendance.map((record) => (
                <tr key={record.id}>
                  <td>{record.id}</td>
                  <td>{getMemberName(record.member_id)}</td>
                  <td>
                    <div className="class-cell">
                      <FaDumbbell />
                      <span>{getClassName(record.class_id)}</span>
                    </div>
                  </td>
                  <td>
                    <div className="date-cell">
                      <FaCalendarAlt />
                      <span>{new Date(record.date).toLocaleDateString()}</span>
                    </div>
                  </td>
                  <td>
                    <span className={`status-badge ${record.status}`}>
                      {record.status === 'present' ? (
                        <><FaCheckCircle /> Present</>
                      ) : (
                        <><FaTimesCircle /> Absent</>
                      )}
                    </span>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="5" className="no-data">
                  No attendance records found for the selected filters
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Mark Attendance Modal */}
      {showMarkModal && (
        <div className="modal-overlay" onClick={() => setShowMarkModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Mark Attendance</h2>
              <button className="modal-close" onClick={() => setShowMarkModal(false)}>×</button>
            </div>
            
            <form onSubmit={handleMarkAttendance} className="attendance-form">
              <div className="form-group">
                <label>Member *</label>
                <select
                  value={markFormData.member_id}
                  onChange={(e) => setMarkFormData({ ...markFormData, member_id: e.target.value })}
                  required
                >
                  <option value="">Select a member</option>
                  {members.map(member => (
                    <option key={member.id} value={member.id}>
                      {member.name} ({member.email})
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Class *</label>
                <select
                  value={markFormData.class_id}
                  onChange={(e) => setMarkFormData({ ...markFormData, class_id: e.target.value })}
                  required
                >
                  <option value="">Select a class</option>
                  {classes.map(cls => (
                    <option key={cls.id} value={cls.id}>
                      {cls.name} - {cls.schedule}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Date *</label>
                <input
                  type="date"
                  value={markFormData.date}
                  onChange={(e) => setMarkFormData({ ...markFormData, date: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label>Status *</label>
                <div className="status-radio-group">
                  <label className="radio-label">
                    <input
                      type="radio"
                      value="present"
                      checked={markFormData.status === 'present'}
                      onChange={(e) => setMarkFormData({ ...markFormData, status: e.target.value })}
                    />
                    <span className="radio-text present">
                      <FaCheckCircle /> Present
                    </span>
                  </label>
                  <label className="radio-label">
                    <input
                      type="radio"
                      value="absent"
                      checked={markFormData.status === 'absent'}
                      onChange={(e) => setMarkFormData({ ...markFormData, status: e.target.value })}
                    />
                    <span className="radio-text absent">
                      <FaTimesCircle /> Absent
                    </span>
                  </label>
                </div>
              </div>

              <div className="modal-actions">
                <button type="submit" className="btn-save">
                  Save Attendance
                </button>
                <button type="button" className="btn-cancel" onClick={() => setShowMarkModal(false)}>
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

export default AdminAttendance;
