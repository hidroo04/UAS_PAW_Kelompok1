import { useState, useEffect } from 'react';
import { 
  FaMoneyBillWave, 
  FaSearch, 
  FaFilter,
  FaCheckCircle,
  FaTimesCircle,
  FaClock,
  FaEye,
  FaSync,
  FaDownload,
  FaChartBar
} from 'react-icons/fa';
import apiClient from '../../services/api';
import Loading from '../../components/Loading';
import './AdminPayments.css';

const AdminPayments = () => {
  const [payments, setPayments] = useState([]);
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [planFilter, setPlanFilter] = useState('all');
  const [selectedPayment, setSelectedPayment] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showReportModal, setShowReportModal] = useState(false);

  useEffect(() => {
    fetchPayments();
  }, [statusFilter, planFilter]);

  const fetchPayments = async () => {
    try {
      setLoading(true);
      
      // Build query params
      const params = new URLSearchParams();
      if (statusFilter !== 'all') params.append('status', statusFilter);
      if (planFilter !== 'all') params.append('plan', planFilter);
      
      const queryString = params.toString();
      const url = `/payment/report${queryString ? `?${queryString}` : ''}`;
      
      const response = await apiClient.get(url);
      const data = response.data.data;
      
      setPayments(data.payments || []);
      setStatistics(data.statistics || null);
      setError(null);
    } catch (err) {
      console.error('Error fetching payments:', err);
      // Fallback to simple endpoint
      try {
        const response = await apiClient.get('/payment/all');
        setPayments(response.data.data || []);
        setStatistics(null);
      } catch (e) {
        setError('Failed to load payments');
      }
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'success': return <FaCheckCircle className="status-icon success" />;
      case 'failed': return <FaTimesCircle className="status-icon failed" />;
      case 'expired': return <FaTimesCircle className="status-icon expired" />;
      default: return <FaClock className="status-icon pending" />;
    }
  };

  const getStatusBadge = (status) => {
    return (
      <span className={`status-badge ${status}`}>
        {getStatusIcon(status)}
        {status.toUpperCase()}
      </span>
    );
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('id-ID', {
      style: 'currency',
      currency: 'IDR',
      minimumFractionDigits: 0
    }).format(amount);
  };

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleString('id-ID', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const filteredPayments = payments.filter(payment => {
    const matchesSearch = 
      payment.order_id?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      payment.member?.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      payment.member?.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      payment.membership_plan?.toLowerCase().includes(searchTerm.toLowerCase());
    
    return matchesSearch;
  });

  // Use statistics from API or calculate locally
  const stats = statistics ? {
    total: statistics.total_payments,
    success: statistics.status_counts?.success || 0,
    pending: statistics.status_counts?.pending || 0,
    failed: (statistics.status_counts?.failed || 0) + (statistics.status_counts?.expired || 0),
    totalRevenue: statistics.successful_amount || 0,
    planCounts: statistics.plan_counts || {},
    planRevenue: statistics.plan_revenue || {},
    methodCounts: statistics.method_counts || {},
    dailyRevenue: statistics.daily_revenue || []
  } : {
    total: payments.length,
    success: payments.filter(p => p.status === 'success').length,
    pending: payments.filter(p => p.status === 'pending').length,
    failed: payments.filter(p => p.status === 'failed' || p.status === 'expired').length,
    totalRevenue: payments
      .filter(p => p.status === 'success')
      .reduce((sum, p) => sum + (parseFloat(p.amount) || 0), 0),
    planCounts: {},
    planRevenue: {},
    methodCounts: {},
    dailyRevenue: []
  };

  const exportToCSV = () => {
    const headers = ['Order ID', 'Member Name', 'Email', 'Plan', 'Amount', 'Method', 'Status', 'Date'];
    const rows = filteredPayments.map(p => [
      p.order_id,
      p.member?.name || 'N/A',
      p.member?.email || 'N/A',
      p.membership_plan,
      p.amount,
      p.payment_method || '-',
      p.status,
      p.created_at ? new Date(p.created_at).toLocaleDateString() : '-'
    ]);
    
    const csvContent = [headers, ...rows].map(row => row.join(',')).join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `payment_report_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const handleViewDetail = (payment) => {
    setSelectedPayment(payment);
    setShowModal(true);
  };

  if (loading) {
    return <Loading message="Loading payments..." />;
  }

  return (
    <div className="admin-payments-page">
      <div className="page-header">
        <div className="header-content">
          <h1><FaMoneyBillWave /> Payment Management</h1>
          <p>Monitor and manage all membership payments</p>
        </div>
        <div className="header-actions">
          <button onClick={() => setShowReportModal(true)} className="btn-report">
            <FaChartBar /> View Report
          </button>
          <button onClick={exportToCSV} className="btn-export">
            <FaDownload /> Export CSV
          </button>
          <button onClick={fetchPayments} className="btn-refresh">
            <FaSync /> Refresh
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card total">
          <div className="stat-icon">
            <FaMoneyBillWave />
          </div>
          <div className="stat-info">
            <span className="stat-value">{stats.total}</span>
            <span className="stat-label">Total Transactions</span>
          </div>
        </div>
        <div className="stat-card success">
          <div className="stat-icon">
            <FaCheckCircle />
          </div>
          <div className="stat-info">
            <span className="stat-value">{stats.success}</span>
            <span className="stat-label">Successful</span>
          </div>
        </div>
        <div className="stat-card pending">
          <div className="stat-icon">
            <FaClock />
          </div>
          <div className="stat-info">
            <span className="stat-value">{stats.pending}</span>
            <span className="stat-label">Pending</span>
          </div>
        </div>
        <div className="stat-card revenue">
          <div className="stat-icon">
            <FaMoneyBillWave />
          </div>
          <div className="stat-info">
            <span className="stat-value">{formatCurrency(stats.totalRevenue)}</span>
            <span className="stat-label">Total Revenue</span>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="filters-section">
        <div className="search-box">
          <FaSearch />
          <input
            type="text"
            placeholder="Search by order ID, member name, email..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <div className="filter-box">
          <FaFilter />
          <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
            <option value="all">All Status</option>
            <option value="pending">Pending</option>
            <option value="success">Success</option>
            <option value="failed">Failed</option>
            <option value="expired">Expired</option>
          </select>
        </div>
        <div className="filter-box">
          <FaFilter />
          <select value={planFilter} onChange={(e) => setPlanFilter(e.target.value)}>
            <option value="all">All Plans</option>
            <option value="Basic">Basic</option>
            <option value="Premium">Premium</option>
            <option value="VIP">VIP</option>
          </select>
        </div>
      </div>

      {/* Payments Table */}
      {error ? (
        <div className="error-message">{error}</div>
      ) : filteredPayments.length === 0 ? (
        <div className="no-data">
          <FaMoneyBillWave size={48} />
          <p>No payments found</p>
        </div>
      ) : (
        <div className="table-container">
          <table className="payments-table">
            <thead>
              <tr>
                <th>Order ID</th>
                <th>Member</th>
                <th>Plan</th>
                <th>Amount</th>
                <th>Method</th>
                <th>Status</th>
                <th>Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredPayments.map((payment) => (
                <tr key={payment.id}>
                  <td className="order-id">{payment.order_id}</td>
                  <td className="member-info">
                    <span className="member-name">{payment.member?.name || 'N/A'}</span>
                    <span className="member-email">{payment.member?.email || ''}</span>
                  </td>
                  <td>
                    <span className={`plan-badge ${payment.membership_plan?.toLowerCase()}`}>
                      {payment.membership_plan}
                    </span>
                  </td>
                  <td className="amount">{formatCurrency(payment.amount)}</td>
                  <td className="method">{payment.payment_method?.replace('_', ' ') || '-'}</td>
                  <td>{getStatusBadge(payment.status)}</td>
                  <td className="date">{formatDate(payment.created_at)}</td>
                  <td>
                    <button 
                      className="btn-view"
                      onClick={() => handleViewDetail(payment)}
                    >
                      <FaEye /> View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Detail Modal */}
      {showModal && selectedPayment && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Payment Details</h2>
              <button className="btn-close" onClick={() => setShowModal(false)}>×</button>
            </div>
            <div className="modal-body">
              <div className="detail-section">
                <h3>Transaction Info</h3>
                <div className="detail-grid">
                  <div className="detail-item">
                    <label>Order ID</label>
                    <span>{selectedPayment.order_id}</span>
                  </div>
                  <div className="detail-item">
                    <label>Status</label>
                    {getStatusBadge(selectedPayment.status)}
                  </div>
                  <div className="detail-item">
                    <label>Amount</label>
                    <span className="amount-large">{formatCurrency(selectedPayment.amount)}</span>
                  </div>
                  <div className="detail-item">
                    <label>Payment Method</label>
                    <span>{selectedPayment.payment_method?.replace('_', ' ').toUpperCase() || '-'}</span>
                  </div>
                  {selectedPayment.va_number && (
                    <div className="detail-item">
                      <label>VA Number</label>
                      <span className="va-number">{selectedPayment.va_number}</span>
                    </div>
                  )}
                  {selectedPayment.transaction_id && (
                    <div className="detail-item">
                      <label>Transaction ID</label>
                      <span>{selectedPayment.transaction_id}</span>
                    </div>
                  )}
                </div>
              </div>

              <div className="detail-section">
                <h3>Member Info</h3>
                <div className="detail-grid">
                  <div className="detail-item">
                    <label>Name</label>
                    <span>{selectedPayment.member?.name || 'N/A'}</span>
                  </div>
                  <div className="detail-item">
                    <label>Email</label>
                    <span>{selectedPayment.member?.email || 'N/A'}</span>
                  </div>
                </div>
              </div>

              <div className="detail-section">
                <h3>Membership</h3>
                <div className="detail-grid">
                  <div className="detail-item">
                    <label>Plan</label>
                    <span className={`plan-badge ${selectedPayment.membership_plan?.toLowerCase()}`}>
                      {selectedPayment.membership_plan}
                    </span>
                  </div>
                  <div className="detail-item">
                    <label>Duration</label>
                    <span>{selectedPayment.duration_days} days</span>
                  </div>
                </div>
              </div>

              <div className="detail-section">
                <h3>Timestamps</h3>
                <div className="detail-grid">
                  <div className="detail-item">
                    <label>Created At</label>
                    <span>{formatDate(selectedPayment.created_at)}</span>
                  </div>
                  {selectedPayment.paid_at && (
                    <div className="detail-item">
                      <label>Paid At</label>
                      <span>{formatDate(selectedPayment.paid_at)}</span>
                    </div>
                  )}
                  {selectedPayment.expired_at && (
                    <div className="detail-item">
                      <label>Expires At</label>
                      <span>{formatDate(selectedPayment.expired_at)}</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Report Modal */}
      {showReportModal && (
        <div className="modal-overlay" onClick={() => setShowReportModal(false)}>
          <div className="modal-content report-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2><FaChartBar /> Payment Report</h2>
              <button className="btn-close" onClick={() => setShowReportModal(false)}>×</button>
            </div>
            <div className="modal-body">
              {/* Summary */}
              <div className="report-section">
                <h3>Summary</h3>
                <div className="report-summary">
                  <div className="summary-item">
                    <span className="label">Total Transactions</span>
                    <span className="value">{stats.total}</span>
                  </div>
                  <div className="summary-item">
                    <span className="label">Total Revenue</span>
                    <span className="value success">{formatCurrency(stats.totalRevenue)}</span>
                  </div>
                  <div className="summary-item">
                    <span className="label">Success Rate</span>
                    <span className="value">
                      {stats.total > 0 ? ((stats.success / stats.total) * 100).toFixed(1) : 0}%
                    </span>
                  </div>
                </div>
              </div>

              {/* Revenue by Plan */}
              <div className="report-section">
                <h3>Revenue by Plan</h3>
                <div className="report-bars">
                  {Object.entries(stats.planRevenue).map(([plan, revenue]) => (
                    <div key={plan} className="bar-item">
                      <div className="bar-label">
                        <span className={`plan-badge ${plan.toLowerCase()}`}>{plan}</span>
                        <span className="bar-value">{formatCurrency(revenue)}</span>
                      </div>
                      <div className="bar-container">
                        <div 
                          className={`bar-fill ${plan.toLowerCase()}`}
                          style={{ 
                            width: `${stats.totalRevenue > 0 ? (revenue / stats.totalRevenue) * 100 : 0}%` 
                          }}
                        />
                      </div>
                      <span className="bar-count">{stats.planCounts[plan] || 0} transactions</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Payment Methods */}
              <div className="report-section">
                <h3>Payment Methods</h3>
                <div className="method-grid">
                  {Object.entries(stats.methodCounts).map(([method, count]) => (
                    <div key={method} className="method-item">
                      <span className="method-name">{method.replace('_', ' ').toUpperCase()}</span>
                      <span className="method-count">{count}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Daily Revenue Chart (Simple) */}
              {stats.dailyRevenue.length > 0 && (
                <div className="report-section">
                  <h3>Daily Revenue (Last 30 Days)</h3>
                  <div className="daily-chart">
                    {stats.dailyRevenue.slice(-14).map((day, index) => (
                      <div key={index} className="chart-bar-container">
                        <div 
                          className="chart-bar"
                          style={{ 
                            height: `${Math.max(10, (day.total / Math.max(...stats.dailyRevenue.map(d => d.total))) * 100)}%` 
                          }}
                          title={`${day.date}: ${formatCurrency(day.total)}`}
                        />
                        <span className="chart-label">{day.date.slice(-5)}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminPayments;
