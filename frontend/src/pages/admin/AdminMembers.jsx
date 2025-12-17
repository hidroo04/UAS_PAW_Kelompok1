import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  HiSearch, 
  HiPencil, 
  HiTrash, 
  HiUserAdd,
  HiFilter,
  HiCheckCircle,
  HiXCircle,
  HiUsers
} from 'react-icons/hi';
import { RiMedalFill, RiUserStarFill, RiVipCrownFill } from 'react-icons/ri';
import apiClient from '../../services/api';
import './AdminMembers.css';

const AdminMembers = () => {
  const [members, setMembers] = useState([]);
  const [filteredMembers, setFilteredMembers] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [selectedMember, setSelectedMember] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    membership_plan: 'Basic',
    expiry_date: ''
  });
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    
    if (!token || user.role !== 'admin') {
      navigate('/login');
      return;
    }
    
    fetchMembers();
  }, [navigate]);

  useEffect(() => {
    filterMembers();
  }, [searchTerm, filterType, members]);

  const fetchMembers = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/users?role=member');
      const memberData = response.data.data || [];
      setMembers(memberData);
      setFilteredMembers(memberData);
    } catch (err) {
      console.error('Error fetching members:', err);
    } finally {
      setLoading(false);
    }
  };

  const filterMembers = () => {
    let filtered = [...members];

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(member =>
        member.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        member.email.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Filter by membership type
    if (filterType !== 'all') {
      filtered = filtered.filter(member => 
        member.membership_plan === filterType
      );
    }

    setFilteredMembers(filtered);
  };

  const handleEdit = (member) => {
    setSelectedMember(member);
    setFormData({
      name: member.name,
      email: member.email,
      membership_plan: member.membership_plan || 'Basic',
      expiry_date: member.expiry_date || ''
    });
    setShowModal(true);
  };

  const handleDelete = async (memberId) => {
    if (!window.confirm('Are you sure you want to delete this member?')) {
      return;
    }

    try {
      const response = await apiClient.delete(`/users/${memberId}`);
      console.log('Delete response:', response.data);
      
      // Langsung update state lokal - hapus member dari list
      setMembers(prevMembers => prevMembers.filter(m => m.id !== memberId));
      setFilteredMembers(prevFiltered => prevFiltered.filter(m => m.id !== memberId));
      
      alert('Member deleted successfully!');
    } catch (err) {
      console.error('Delete error:', err);
      console.error('Error response:', err.response?.data);
      const errorMsg = err.response?.data?.message || 'Failed to delete member';
      alert(`Error: ${errorMsg}`);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      if (selectedMember) {
        // Update existing member
        await apiClient.put(`/users/${selectedMember.id}`, formData);
        alert('Member updated successfully!');
      } else {
        // Create new member
        await apiClient.post('/auth/register', {
          ...formData,
          password: 'default123', // Default password
          role: 'member'
        });
        alert('Member created successfully!');
      }
      
      setShowModal(false);
      setSelectedMember(null);
      fetchMembers();
    } catch (err) {
      alert('Failed to save member');
      console.error(err);
    }
  };

  const getMembershipBadge = (plan) => {
    const badges = {
      'Basic': { icon: <RiMedalFill />, class: 'basic' },
      'Premium': { icon: <RiUserStarFill />, class: 'premium' },
      'VIP': { icon: <RiVipCrownFill />, class: 'vip' }
    };
    return badges[plan] || badges['Basic'];
  };

  if (loading) {
    return <div className="admin-loading">Loading members...</div>;
  }

  return (
    <div className="admin-members">
      <div className="members-header">
        <h1>Members Management</h1>
        <button className="btn-add" onClick={() => {
          setSelectedMember(null);
          setFormData({ name: '', email: '', membership_plan: 'Basic', expiry_date: '' });
          setShowModal(true);
        }}>
          <HiUserAdd /> Add New Member
        </button>
      </div>

      {/* Filters */}
      <div className="members-filters">
        <div className="search-box">
          <HiSearch />
          <input
            type="text"
            placeholder="Search members by name or email..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <div className="filter-buttons">
          <button 
            className={filterType === 'all' ? 'active' : ''}
            onClick={() => setFilterType('all')}
          >
            All ({members.length})
          </button>
          <button 
            className={filterType === 'Basic' ? 'active basic' : ''}
            onClick={() => setFilterType('Basic')}
          >
            <RiMedalFill /> Basic
          </button>
          <button 
            className={filterType === 'Premium' ? 'active premium' : ''}
            onClick={() => setFilterType('Premium')}
          >
            <RiUserStarFill /> Premium
          </button>
          <button 
            className={filterType === 'VIP' ? 'active vip' : ''}
            onClick={() => setFilterType('VIP')}
          >
            <RiVipCrownFill /> VIP
          </button>
        </div>
      </div>

      {/* Members Table */}
      <div className="members-table-container">
        <table className="members-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Membership</th>
              <th>Status</th>
              <th>Joined Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredMembers.length > 0 ? (
              filteredMembers.map((member) => {
                const badge = getMembershipBadge(member.membership_plan);
                return (
                  <tr key={member.id}>
                    <td>{member.id}</td>
                    <td className="member-name">
                      <div className="member-avatar">
                        {member.name.charAt(0).toUpperCase()}
                      </div>
                      <span>{member.name}</span>
                    </td>
                    <td>{member.email}</td>
                    <td>
                      <span className={`membership-badge ${badge.class}`}>
                        {badge.icon} {member.membership_plan || 'Basic'}
                      </span>
                    </td>
                    <td>
                      <span className={`status-badge ${member.is_active ? 'active' : 'inactive'}`}>
                        {member.is_active ? <><HiCheckCircle /> Active</> : <><HiXCircle /> Inactive</>}
                      </span>
                    </td>
                    <td>{new Date(member.created_at || Date.now()).toLocaleDateString()}</td>
                    <td className="actions">
                      <button 
                        className="btn-edit-small"
                        onClick={() => handleEdit(member)}
                        title="Edit member"
                      >
                        <HiPencil />
                      </button>
                      <button 
                        className="btn-delete-small"
                        onClick={() => handleDelete(member.id)}
                        title="Delete member"
                      >
                        <HiTrash />
                      </button>
                    </td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan="7" className="no-data">
                  No members found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>{selectedMember ? 'Edit Member' : 'Add New Member'}</h2>
              <button className="modal-close" onClick={() => setShowModal(false)}>×</button>
            </div>
            
            <form onSubmit={handleSubmit} className="member-form">
              <div className="form-group">
                <label>Full Name *</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label>Email *</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label>Membership Plan *</label>
                <select
                  value={formData.membership_plan}
                  onChange={(e) => setFormData({ ...formData, membership_plan: e.target.value })}
                  required
                >
                  <option value="Basic">💼 Basic</option>
                  <option value="Premium">⭐ Premium</option>
                  <option value="VIP">👑 VIP</option>
                </select>
              </div>

              <div className="form-group">
                <label>Expiry Date</label>
                <input
                  type="date"
                  value={formData.expiry_date}
                  onChange={(e) => setFormData({ ...formData, expiry_date: e.target.value })}
                />
              </div>

              <div className="modal-actions">
                <button type="submit" className="btn-save">
                  {selectedMember ? 'Update Member' : 'Create Member'}
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

export default AdminMembers;
