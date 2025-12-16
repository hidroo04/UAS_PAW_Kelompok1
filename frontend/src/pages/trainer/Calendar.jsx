import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import Loading from '../../components/Loading';
import { FaChevronLeft, FaChevronRight, FaCalendarAlt, FaClock, FaUsers } from 'react-icons/fa';
import './Calendar.css';

const Calendar = () => {
  const [classes, setClasses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user || user.role !== 'trainer') {
      navigate('/login');
      return;
    }
    fetchClasses();
  }, [navigate]);

  const fetchClasses = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await api.get('/trainer/classes');
      
      if (response.data.status === 'success') {
        setClasses(response.data.data);
      } else {
        setError('Failed to load classes');
      }
    } catch (err) {
      console.error('Error fetching classes:', err);
      setError(err.response?.data?.message || 'Failed to load classes');
    } finally {
      setLoading(false);
    }
  };

  const getDaysInMonth = (date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startingDayOfWeek = firstDay.getDay();

    return { daysInMonth, startingDayOfWeek, year, month };
  };

  const getClassesForDate = (date) => {
    return classes.filter(cls => {
      if (!cls.schedule) return false;
      const classDate = new Date(cls.schedule);
      return (
        classDate.getDate() === date.getDate() &&
        classDate.getMonth() === date.getMonth() &&
        classDate.getFullYear() === date.getFullYear()
      );
    });
  };

  const previousMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1));
  };

  const nextMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1));
  };

  const goToToday = () => {
    setCurrentDate(new Date());
    setSelectedDate(new Date());
  };

  const formatTime = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    });
  };

  const { daysInMonth, startingDayOfWeek, year, month } = getDaysInMonth(currentDate);
  const monthName = currentDate.toLocaleString('en-US', { month: 'long' });
  const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  const selectedClasses = selectedDate ? getClassesForDate(selectedDate) : [];

  if (loading) return <Loading />;

  return (
    <div className="calendar-container">
      <div className="calendar-header">
        <div>
          <span className="header-badge">Class Schedule</span>
          <h1>My Calendar</h1>
          <p>View your class schedule</p>
        </div>
        <button className="btn-today" onClick={goToToday}>
          <FaCalendarAlt /> Today
        </button>
      </div>

      {error && (
        <div className="error-message">
          <p>{error}</p>
          <button onClick={fetchClasses}>Try Again</button>
        </div>
      )}

      <div className="calendar-main">
        <div className="calendar-view">
          <div className="calendar-controls">
            <button className="btn-nav" onClick={previousMonth}>
              <FaChevronLeft />
            </button>
            <h2 className="current-month">
              {monthName} {year}
            </h2>
            <button className="btn-nav" onClick={nextMonth}>
              <FaChevronRight />
            </button>
          </div>

          <div className="calendar-grid">
            {/* Day names */}
            {dayNames.map(day => (
              <div key={day} className="calendar-day-name">
                {day}
              </div>
            ))}

            {/* Empty cells before first day */}
            {Array.from({ length: startingDayOfWeek }).map((_, index) => (
              <div key={`empty-${index}`} className="calendar-day empty"></div>
            ))}

            {/* Days of month */}
            {Array.from({ length: daysInMonth }).map((_, index) => {
              const dayNumber = index + 1;
              const date = new Date(year, month, dayNumber);
              const dayClasses = getClassesForDate(date);
              const isToday = 
                date.getDate() === new Date().getDate() &&
                date.getMonth() === new Date().getMonth() &&
                date.getFullYear() === new Date().getFullYear();
              const isSelected = selectedDate &&
                date.getDate() === selectedDate.getDate() &&
                date.getMonth() === selectedDate.getMonth() &&
                date.getFullYear() === selectedDate.getFullYear();

              return (
                <div
                  key={dayNumber}
                  className={`calendar-day ${isToday ? 'today' : ''} ${isSelected ? 'selected' : ''} ${dayClasses.length > 0 ? 'has-classes' : ''}`}
                  onClick={() => setSelectedDate(date)}
                >
                  <span className="day-number">{dayNumber}</span>
                  {dayClasses.length > 0 && (
                    <div className="day-indicator">
                      <span className="class-count">{dayClasses.length}</span>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Selected Date Details */}
        <div className="calendar-sidebar">
          <h3>
            {selectedDate
              ? selectedDate.toLocaleDateString('en-US', {
                  weekday: 'long',
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric'
                })
              : 'Select a date'}
          </h3>

          {selectedDate && selectedClasses.length === 0 && (
            <div className="no-classes-day">
              <p>No classes scheduled for this day</p>
            </div>
          )}

          {selectedDate && selectedClasses.length > 0 && (
            <div className="day-classes">
              {selectedClasses.map(cls => (
                <div key={cls.id} className="calendar-class-card">
                  <div className="class-time">
                    <FaClock />
                    <span>{formatTime(cls.schedule)}</span>
                  </div>
                  <h4>{cls.name}</h4>
                  <p className="class-description">{cls.description}</p>
                  <div className="class-stats">
                    <div className="stat-item">
                      <FaUsers />
                      <span>{cls.enrolled_count || 0} / {cls.capacity}</span>
                    </div>
                    <span className={`status-badge ${cls.available_slots === 0 ? 'full' : 'available'}`}>
                      {cls.available_slots === 0 ? 'Full' : `${cls.available_slots} slots`}
                    </span>
                  </div>
                  <button 
                    className="btn-view-class"
                    onClick={() => navigate(`/trainer/my-classes/${cls.id}`)}
                  >
                    View Details
                  </button>
                </div>
              ))}
            </div>
          )}

          {!selectedDate && (
            <div className="no-classes-day">
              <FaCalendarAlt style={{ fontSize: '3rem', marginBottom: '1rem', opacity: 0.3 }} />
              <p>Click on a date to view scheduled classes</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Calendar;
