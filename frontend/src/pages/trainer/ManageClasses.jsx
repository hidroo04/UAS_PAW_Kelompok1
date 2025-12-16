import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import Loading from '../../components/Loading';
import { FaPlus, FaEdit, FaTrash, FaCalendar, FaUsers, FaClock } from 'react-icons/fa';
import './ManageClasses.css';

const ManageClasses = () => {
  const [classes, setClasses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [editingClass, setEditingClass] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    schedule: '',
    capacity: 15
  });
  const [submitting, setSubmitting] = useState(false);
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

  const handleOpenModal = (classData = null) => {
    if (classData) {
      setEditingClass(classData);
      setFormData({
        name: classData.name,
        description: classData.description,
        schedule: classData.schedule ? new Date(classData.schedule).toISOString().slice(0, 16) : '',
        capacity: classData.capacity
      });
    } else {
      setEditingClass(null);
      setFormData({
        name: '',
        description: '',
        schedule: '',
        capacity: 15
      });
    }
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingClass(null);
    setFormData({
      name: '',
      description: '',
      schedule: '',
      capacity: 15
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      const submitData = {
        ...formData,
        schedule: new Date(formData.schedule).toISOString()
      };

      let response;
      if (editingClass) {
        response = await api.put(`/trainer/classes/${editingClass.id}/update`, submitData);
      } else {
        response = await api.post('/trainer/classes/create', submitData);
      }

      if (response.data.status === 'success') {
        alert(response.data.message);
        handleCloseModal();
        fetchClasses();
      } else {
        alert('Failed to save class: ' + response.data.message);
      }
    } catch (err) {
      console.error('Error saving class:', err);
      alert(err.response?.data?.message || 'Failed to save class');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (classId, className) => {
    if (!window.confirm(`Are you sure you want to delete "${className}"?\n\nAll bookings for this class will be removed.`)) {
      return;
    }

    try {
      const response = await api.delete(`/trainer/classes/${classId}/delete`);
      
      if (response.data.status === 'success') {
        alert(response.data.message);
        fetchClasses();
      } else {
        alert('Failed to delete class: ' + response.data.message);
      }
    } catch (err) {
      console.error('Error deleting class:', err);
      alert(err.response?.data?.message || 'Failed to delete class');
    }
  };

  const formatDateTime = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      weekday: 'short',
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) return <Loading />;

  return (
    <div className="manage-classes-container">
      <div className="manage-classes-header">
        <div>
          <span className="header-badge">Class Management</span>
          <h1>Manage Classes</h1>
          <p>Create, edit, and manage your classes</p>
        </div>
        <button className="btn-create-class" onClick={() => handleOpenModal()}>
          <FaPlus /> Create New Class
        </button>
      </div>

      {error && (
        <div className="error-message">
          <p>{error}</p>
          <button onClick={fetchClasses}>Try Again</button>
        </div>
      )}

      {!error && classes.length === 0 && (
        <div className="no-classes">
          <div className="no-classes-icon">📚</div>
          <p>You haven't created any classes yet.</p>
          <button className="btn-create-first" onClick={() => handleOpenModal()}>
            <FaPlus /> Create Your First Class
          </button>
        </div>
      )}

      <div className="classes-grid">
        {classes.map((cls) => (
          <div key={cls.id} className="class-manage-card">
            <div className="class-card-header">
              <div className="header-icon">
                <FaUsers />
              </div>
              <div className="class-actions">
                <button 
                  className="btn-edit"
                  onClick={() => handleOpenModal(cls)}
                  title="Edit Class"
                >
                  <FaEdit />
                </button>
                <button 
                  className="btn-delete"
                  onClick={() => handleDelete(cls.id, cls.name)}
                  title="Delete Class"
                >
                  <FaTrash />
                </button>
              </div>
            </div>
            
            <div className="class-card-content">
              <h3>{cls.name}</h3>
              
              <div className="class-info-items">
                <div className="info-item">
                  <FaClock />
                  <span>{formatDateTime(cls.schedule)}</span>
                </div>
                <div className="info-item">
                  <FaUsers />
                  <span>Unknown Trainer</span>
                </div>
                <div className="info-item">
                  <FaUsers />
                  <span>Capacity: {cls.capacity}</span>
                </div>
              </div>
              
              <div className="class-id">ID: {cls.id}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Modal for Create/Edit */}
      {showModal && (
        <div className="modal-overlay" onClick={handleCloseModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>{editingClass ? 'Edit Class' : 'Create New Class'}</h2>
              <button className="btn-close-modal" onClick={handleCloseModal}>×</button>
            </div>
            
            <form onSubmit={handleSubmit} className="class-form">
              <div className="form-group">
                <label>Class Name *</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  required
                  placeholder="e.g., Morning Yoga, HIIT Training"
                />
              </div>

              <div className="form-group">
                <label>Description *</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  required
                  rows="3"
                  placeholder="Describe what this class is about..."
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Schedule *</label>
                  <input
                    type="datetime-local"
                    value={formData.schedule}
                    onChange={(e) => setFormData({...formData, schedule: e.target.value})}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Capacity *</label>
                  <input
                    type="number"
                    value={formData.capacity}
                    onChange={(e) => setFormData({...formData, capacity: parseInt(e.target.value)})}
                    required
                    min="1"
                    max="100"
                  />
                </div>
              </div>

              <div className="modal-actions">
                <button type="button" className="btn-cancel" onClick={handleCloseModal}>
                  Cancel
                </button>
                <button type="submit" className="btn-submit" disabled={submitting}>
                  {submitting ? 'Saving...' : (editingClass ? 'Update Class' : 'Create Class')}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default ManageClasses;
