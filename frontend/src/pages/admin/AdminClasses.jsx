import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  HiSearch, 
  HiPencil, 
  HiTrash, 
  HiPlus,
  HiAcademicCap,
  HiClock,
  HiUsers,
  HiUserGroup
} from 'react-icons/hi';
import apiClient from '../../services/api';
import './AdminClasses.css';

const AdminClasses = () => {
  const [classes, setClasses] = useState([]);
  const [filteredClasses, setFilteredClasses] = useState([]);
  const [trainers, setTrainers] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [selectedClass, setSelectedClass] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    schedule: '',
    trainer_id: '',
    capacity: 20
  });
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    
    if (!token || user.role !== 'admin') {
      navigate('/login');
      return;
    }
    
    fetchClasses();
    fetchTrainers();
  }, [navigate]);

  useEffect(() => {
    filterClasses();
  }, [searchTerm, classes]);

  const fetchClasses = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/classes');
      const classData = response.data.data || [];
      setClasses(classData);
      setFilteredClasses(classData);
    } catch (err) {
      console.error('Error fetching classes:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchTrainers = async () => {
    try {
      const response = await apiClient.get('/users?role=trainer');
      setTrainers(response.data.data || []);
    } catch (err) {
      console.error('Error fetching trainers:', err);
    }
  };

  const filterClasses = () => {
    if (!searchTerm) {
      setFilteredClasses(classes);
      return;
    }

    const filtered = classes.filter(cls =>
      cls.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      cls.schedule.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredClasses(filtered);
  };

  const handleEdit = (cls) => {
    setSelectedClass(cls);
    setFormData({
      name: cls.name,
      schedule: cls.schedule,
      trainer_id: cls.trainer_id,
      capacity: cls.capacity || 20
    });
    setShowModal(true);
  };

  const handleDelete = async (classId) => {
    if (!window.confirm('Are you sure you want to delete this class? All bookings will be cancelled.')) {
      return;
    }

    try {
      await apiClient.delete(`/classes/${classId}`);
      alert('Class deleted successfully!');
      fetchClasses();
    } catch (err) {
      alert('Failed to delete class');
      console.error(err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      if (selectedClass) {
        // Update existing class
        await apiClient.put(`/classes/${selectedClass.id}`, formData);
        alert('Class updated successfully!');
      } else {
        // Create new class
        await apiClient.post('/classes', formData);
        alert('Class created successfully!');
      }
      
      setShowModal(false);
      setSelectedClass(null);
      fetchClasses();
    } catch (err) {
      alert('Failed to save class');
      console.error(err);
    }
  };

  const getTrainerName = (trainerId) => {
    const trainer = trainers.find(t => t.id === trainerId);
    return trainer ? trainer.name : 'Unknown Trainer';
  };

  if (loading) {
    return <div className="admin-loading">Loading classes...</div>;
  }

  return (
    <div className="admin-classes">
      <div className="classes-header">
        <h1>Classes Management</h1>
        <button className="btn-add" onClick={() => {
          setSelectedClass(null);
          setFormData({ name: '', schedule: '', trainer_id: '', capacity: 20 });
          setShowModal(true);
        }}>
          <HiPlus /> Add New Class
        </button>
      </div>

      {/* Search */}
      <div className="classes-search">
        <div className="search-box">
          <HiSearch />
          <input
            type="text"
            placeholder="Search classes by name or schedule..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <div className="class-stats">
          <div className="stat">
            <HiAcademicCap />
            <span>{classes.length} Total Classes</span>
          </div>
        </div>
      </div>

      {/* Classes Grid */}
      <div className="classes-grid">
        {filteredClasses.length > 0 ? (
          filteredClasses.map((cls) => (
            <div key={cls.id} className="class-card">
              <div className="class-card-header">
                <div className="class-icon">
                  <HiAcademicCap />
                </div>
                <div className="class-actions">
                  <button 
                    className="btn-edit-icon"
                    onClick={() => handleEdit(cls)}
                    title="Edit class"
                  >
                    <HiPencil />
                  </button>
                  <button 
                    className="btn-delete-icon"
                    onClick={() => handleDelete(cls.id)}
                    title="Delete class"
                  >
                    <HiTrash />
                  </button>
                </div>
              </div>

              <div className="class-card-body">
                <h3>{cls.name}</h3>
                
                <div className="class-info-row">
                  <HiClock />
                  <span>{cls.schedule}</span>
                </div>

                <div className="class-info-row">
                  <HiUserGroup />
                  <span>{getTrainerName(cls.trainer_id)}</span>
                </div>

                <div className="class-info-row">
                  <HiUsers />
                  <span>Capacity: {cls.capacity || 20}</span>
                </div>
              </div>

              <div className="class-card-footer">
                <span className="class-id">ID: {cls.id}</span>
              </div>
            </div>
          ))
        ) : (
          <div className="no-data">No classes found</div>
        )}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>{selectedClass ? 'Edit Class' : 'Add New Class'}</h2>
              <button className="modal-close" onClick={() => setShowModal(false)}>×</button>
            </div>
            
            <form onSubmit={handleSubmit} className="class-form">
              <div className="form-group">
                <label>Class Name *</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="e.g., Yoga Morning Session"
                  required
                />
              </div>

              <div className="form-group">
                <label>Schedule *</label>
                <input
                  type="text"
                  value={formData.schedule}
                  onChange={(e) => setFormData({ ...formData, schedule: e.target.value })}
                  placeholder="e.g., Mon-Wed-Fri 08:00-09:00"
                  required
                />
              </div>

              <div className="form-group">
                <label>Trainer *</label>
                <select
                  value={formData.trainer_id}
                  onChange={(e) => setFormData({ ...formData, trainer_id: e.target.value })}
                  required
                >
                  <option value="">Select a trainer</option>
                  {trainers.map(trainer => (
                    <option key={trainer.id} value={trainer.id}>
                      {trainer.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Capacity *</label>
                <input
                  type="number"
                  value={formData.capacity}
                  onChange={(e) => setFormData({ ...formData, capacity: parseInt(e.target.value) })}
                  min="1"
                  max="100"
                  required
                />
              </div>

              <div className="modal-actions">
                <button type="submit" className="btn-save">
                  {selectedClass ? 'Update Class' : 'Create Class'}
                </button>
                <button type="button" className="btn-cancel" onClick={() => setShowModal(false)}>
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

export default AdminClasses;
