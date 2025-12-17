import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  HiCalendar, 
  HiCheckCircle,
  HiXCircle,
  HiClock,
  HiUserGroup,
  HiSearch
} from 'react-icons/hi';
import apiClient from '../../services/api';
import './AdminAttendance.css';

const AdminAttendance = () => {
  const [attendanceData, setAttendanceData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [classes, setClasses] = useState([]);
  const [statistics, setStatistics] = useState({
    total: 0,
    present: 0,
    absent: 0,
    not_marked: 0
  });
  const [selectedClass, setSelectedClass] = useState('');
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
    filterData();
  }, [selectedClass, searchTerm, attendanceData]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [attendanceRes, classesRes] = await Promise.all([
        apiClient.get('/attendance'),
        apiClient.get('/classes')
      ]);

      const data = attendanceRes.data.data || [];
      const stats = attendanceRes.data.statistics || {
        total: data.length,
        present: data.filter(a => a.attended === true).length,
        absent: data.filter(a => a.attended === false).length,
        not_marked: data.filter(a => a.attended === null).length
      };

      setAttendanceData(data);
      setFilteredData(data);
      setStatistics(stats);
      setClasses(classesRes.data.data || []);
    } catch (err) {
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  const filterData = () => {
    let filtered = [...attendanceData];

    if (selectedClass) {
      filtered = filtered.filter(a => a.class?.id === parseInt(selectedClass));
    }

    if (searchTerm) {
      filtered = filtered.filter(a => 
        a.member?.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        a.class?.name?.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    setFilteredData(filtered);
  };

  const getAttendanceRate = () => {
    const marked = statistics.present + statistics.absent;
    if (marked === 0) return 0;
    return Math.round((statistics.present / marked) * 100);
  };

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString('id-ID', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    });
  };

  const formatTime = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleTimeString('id-ID', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return <div className="admin-loading">Loading attendance data...</div>;
  }

  return (
    <div className="admin-attendance">
      <div className="attendance-header">
        <h1>Attendance Monitoring</h1>
        <p className="subtitle">Pantau kehadiran dari semua class bookings (read-only)</p>
      </div>

      {/* Statistics Cards */}
      <div className="attendance-stats">
        <div className="stat-card total">
          <div className="stat-icon">
            <HiUserGroup />
          </div>
          <div className="stat-info">
            <h3>{statistics.total}</h3>
            <p>Total Bookings</p>
          </div>
        </div>

        <div className="stat-card present">
          <div className="stat-icon">
            <HiCheckCircle />
          </div>
          <div className="stat-info">
            <h3>{statistics.present}</h3>
            <p>Present</p>
          </div>
        </div>

        <div className="stat-card absent">
          <div className="stat-icon">
            <HiXCircle />
          </div>
          <div className="stat-info">
            <h3>{statistics.absent}</h3>
            <p>Absent</p>
          </div>
        </div>

        <div className="stat-card pending">
          <div className="stat-icon">
            <HiClock />
          </div>
          <div className="stat-info">
            <h3>{statistics.not_marked}</h3>
            <p>Not Marked</p>
          </div>
        </div>

        <div className="stat-card rate">
          <div className="stat-info rate-display">
            <h3>{getAttendanceRate()}%</h3>
            <p>Attendance Rate</p>
          </div>
          <div className="rate-bar">
            <div className="rate-fill" style={{ width: `${getAttendanceRate()}%` }}></div>
          </div>
        </div>
      </div>

      {/* Toolbar */}
      <div className="attendance-toolbar">
        <div className="filter-group">
          <label>Filter by Class</label>
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

        <div className="search-box">
          <HiSearch />
          <input
            type="text"
            placeholder="Search member or class..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      {/* Attendance Table - Read Only for Admin */}
      <div className="attendance-table-container">
        <table className="attendance-table">
          <thead>
            <tr>
              <th>Member</th>
              <th>Class</th>
              <th>Class Schedule</th>
              <th>Booking Date</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {filteredData.length > 0 ? (
              filteredData.map((record) => (
                <tr key={record.booking_id}>
                  <td>
                    <div className="member-info">
                      <span className="member-name">{record.member?.name || 'Unknown'}</span>
                      <span className="member-email">{record.member?.email || ''}</span>
                    </div>
                  </td>
                  <td>
                    <span className="class-name">{record.class?.name || 'Unknown'}</span>
                  </td>
                  <td>
                    <div className="schedule-info">
                      <span className="date">
                        <HiCalendar /> {formatDate(record.class?.schedule)}
                      </span>
                      <span className="time">{formatTime(record.class?.schedule)}</span>
                    </div>
                  </td>
                  <td>
                    <span className="booking-date">{formatDate(record.booking_date)}</span>
                  </td>
                  <td>
                    {record.attended === true && (
                      <span className="status-badge present">
                        <HiCheckCircle /> Present
                      </span>
                    )}
                    {record.attended === false && (
                      <span className="status-badge absent">
                        <HiXCircle /> Absent
                      </span>
                    )}
                    {record.attended === null && (
                      <span className="status-badge not-marked">
                        <HiClock /> Not Marked
                      </span>
                    )}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="5" className="no-data">
                  No booking records found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AdminAttendance;
