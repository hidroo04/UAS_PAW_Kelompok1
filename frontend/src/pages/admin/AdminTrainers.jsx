import { useState, useEffect } from 'react';
import { 
  FaUserTie, 
  FaCheck, 
  FaTimes, 
  FaClock, 
  FaSearch,
  FaFilter,
  FaEnvelope,
  FaPhone,
  FaCalendarAlt,
  FaExclamationTriangle,
  FaCheckCircle,
  FaTimesCircle,
  FaSpinner
} from 'react-icons/fa';
import apiClient from '../../services/api';
import Loading from '../../components/Loading';
import './AdminTrainers.css';

const AdminTrainers = () => {
  const [trainers, setTrainers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [counts, setCounts] = useState({ pending: 0, approved: 0, rejected: 0, total: 0 });
  const [statusFilter, setStatusFilter] = useState('pending');
  const [searchTerm, setSearchTerm] = useState('');
  const [processingId, setProcessingId] = useState(null);
  const [showRejectModal, setShowRejectModal] = useState(false);
  const [selectedTrainer, setSelectedTrainer] = useState(null);
  const [rejectReason, setRejectReason] = useState('');

  useEffect(() => {
    fetchTrainers();
  }, [statusFilter]);

  const fetchTrainers = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get(`/admin/trainers?status=${statusFilter}`);
      setTrainers(response.data.data || []);
      setCounts(response.data.counts || { pending: 0, approved: 0, rejected: 0, total: 0 });
      setError(null);
    } catch (err) {
      console.error('Error fetching trainers:', err);
      setError('Failed to load trainers');
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (trainerId) => {
    if (!window.confirm('Are you sure you want to approve this trainer?')) return;
    
    try {
      setProcessingId(trainerId);
      await apiClient.post(`/admin/trainers/${trainerId}/approve`);
      alert('Trainer approved successfully!');
      fetchTrainers();
    } catch (err) {
      console.error('Error approving trainer:', err);
      alert(err.response?.data?.message || 'Failed to approve trainer');
    } finally {
      setProcessingId(null);
    }
  };

  const openRejectModal = (trainer) => {
    setSelectedTrainer(trainer);
    setRejectReason('');
    setShowRejectModal(true);
  };

  const handleReject = async () => {
    if (!rejectReason.trim()) {
      alert('Please provide a reason for rejection');
      return;
    }

    try {
      setProcessingId(selectedTrainer.id);
      await apiClient.post(`/admin/trainers/${selectedTrainer.id}/reject`, {
        reason: rejectReason
      });
      alert('Trainer rejected.');
      setShowRejectModal(false);
      setSelectedTrainer(null);
      setRejectReason('');
      fetchTrainers();
    } catch (err) {
      console.error('Error rejecting trainer:', err);
      alert(err.response?.data?.message || 'Failed to reject trainer');
    } finally {
      setProcessingId(null);
    }
  };

  const filteredTrainers = trainers.filter(trainer => 
    trainer.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    trainer.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getStatusBadge = (status) => {
    switch (status) {
      case 'pending':
        return <span className="status-badge pending"><FaClock /> Pending</span>;
      case 'approved':
        return <span className="status-badge approved"><FaCheckCircle /> Approved</span>;
      case 'rejected':
        return <span className="status-badge rejected"><FaTimesCircle /> Rejected</span>;
      default:
        return <span className="status-badge">{status}</span>;
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString('id-ID', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading && trainers.length === 0) {
    return <Loading message="Loading trainers..." />;
  }

  return (
    <div className="admin-trainers-page">
      <div className="page-header">
        <div className="header-content">
          <h1><FaUserTie /> Trainer Management</h1>
          <p>Review and manage trainer registration requests</p>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card pending" onClick={() => setStatusFilter('pending')}>
          <div className="stat-icon"><FaClock /></div>
          <div className="stat-info">
            <h3>{counts.pending}</h3>
            <p>Pending Approval</p>
          </div>
        </div>
        <div className="stat-card approved" onClick={() => setStatusFilter('approved')}>
          <div className="stat-icon"><FaCheckCircle /></div>
          <div className="stat-info">
            <h3>{counts.approved}</h3>
            <p>Approved</p>
          </div>
        </div>
        <div className="stat-card rejected" onClick={() => setStatusFilter('rejected')}>
          <div className="stat-icon"><FaTimesCircle /></div>
          <div className="stat-info">
            <h3>{counts.rejected}</h3>
            <p>Rejected</p>
          </div>
        </div>
        <div className="stat-card total" onClick={() => setStatusFilter('all')}>
          <div className="stat-icon"><FaUserTie /></div>
          <div className="stat-info">
            <h3>{counts.total}</h3>
            <p>Total Trainers</p>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="filters-section">
        <div className="search-box">
          <FaSearch className="search-icon" />
          <input
            type="text"
            placeholder="Search by name or email..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <div className="filter-tabs">
          <button 
            className={`filter-tab ${statusFilter === 'pending' ? 'active' : ''}`}
            onClick={() => setStatusFilter('pending')}
          >
            <FaClock /> Pending ({counts.pending})
          </button>
          <button 
            className={`filter-tab ${statusFilter === 'approved' ? 'active' : ''}`}
            onClick={() => setStatusFilter('approved')}
          >
            <FaCheckCircle /> Approved ({counts.approved})
          </button>
          <button 
            className={`filter-tab ${statusFilter === 'rejected' ? 'active' : ''}`}
            onClick={() => setStatusFilter('rejected')}
          >
            <FaTimesCircle /> Rejected ({counts.rejected})
          </button>
          <button 
            className={`filter-tab ${statusFilter === 'all' ? 'active' : ''}`}
            onClick={() => setStatusFilter('all')}
          >
            All ({counts.total})
          </button>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="error-message">
          <FaExclamationTriangle /> {error}
        </div>
      )}

      {/* Trainers List */}
      <div className="trainers-list">
        {filteredTrainers.length === 0 ? (
          <div className="empty-state">
            <FaUserTie />
            <h3>No trainers found</h3>
            <p>
              {statusFilter === 'pending' 
                ? 'No pending trainer registrations at the moment.' 
                : `No ${statusFilter} trainers found.`}
            </p>
          </div>
        ) : (
          filteredTrainers.map(trainer => (
            <div key={trainer.id} className={`trainer-card ${trainer.approval_status}`}>
              <div className="trainer-avatar">
                <FaUserTie />
              </div>
              <div className="trainer-info">
                <div className="trainer-header">
                  <h3>{trainer.name}</h3>
                  {getStatusBadge(trainer.approval_status)}
                </div>
                <div className="trainer-details">
                  <span><FaEnvelope /> {trainer.email}</span>
                  {trainer.phone && <span><FaPhone /> {trainer.phone}</span>}
                  <span><FaCalendarAlt /> Registered: {formatDate(trainer.created_at)}</span>
                </div>
                {trainer.approval_status === 'approved' && trainer.approved_at && (
                  <p className="approval-date">
                    <FaCheckCircle /> Approved on {formatDate(trainer.approved_at)}
                  </p>
                )}
                {trainer.approval_status === 'rejected' && trainer.rejection_reason && (
                  <p className="rejection-reason">
                    <FaTimesCircle /> Reason: {trainer.rejection_reason}
                  </p>
                )}
              </div>
              <div className="trainer-actions">
                {trainer.approval_status === 'pending' && (
                  <>
                    <button 
                      className="btn-approve"
                      onClick={() => handleApprove(trainer.id)}
                      disabled={processingId === trainer.id}
                    >
                      {processingId === trainer.id ? (
                        <FaSpinner className="spinner" />
                      ) : (
                        <><FaCheck /> Approve</>
                      )}
                    </button>
                    <button 
                      className="btn-reject"
                      onClick={() => openRejectModal(trainer)}
                      disabled={processingId === trainer.id}
                    >
                      <FaTimes /> Reject
                    </button>
                  </>
                )}
                {trainer.approval_status === 'rejected' && (
                  <button 
                    className="btn-approve"
                    onClick={() => handleApprove(trainer.id)}
                    disabled={processingId === trainer.id}
                  >
                    {processingId === trainer.id ? (
                      <FaSpinner className="spinner" />
                    ) : (
                      <><FaCheck /> Approve</>
                    )}
                  </button>
                )}
              </div>
            </div>
          ))
        )}
      </div>

      {/* Reject Modal */}
      {showRejectModal && (
        <div className="modal-overlay" onClick={() => setShowRejectModal(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h2><FaTimesCircle /> Reject Trainer</h2>
              <button className="btn-close" onClick={() => setShowRejectModal(false)}>×</button>
            </div>
            <div className="modal-body">
              <p>You are about to reject <strong>{selectedTrainer?.name}</strong>'s trainer application.</p>
              <div className="form-group">
                <label>Reason for Rejection *</label>
                <textarea
                  value={rejectReason}
                  onChange={(e) => setRejectReason(e.target.value)}
                  placeholder="Please provide a reason for rejecting this application..."
                  rows={4}
                />
              </div>
            </div>
            <div className="modal-footer">
              <button className="btn-cancel" onClick={() => setShowRejectModal(false)}>
                Cancel
              </button>
              <button 
                className="btn-reject-confirm"
                onClick={handleReject}
                disabled={processingId === selectedTrainer?.id}
              >
                {processingId === selectedTrainer?.id ? (
                  <FaSpinner className="spinner" />
                ) : (
                  <><FaTimes /> Reject Trainer</>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminTrainers;
