import { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { 
  FaCreditCard, 
  FaUniversity, 
  FaWallet, 
  FaQrcode, 
  FaCheckCircle, 
  FaTimesCircle,
  FaClock,
  FaCopy,
  FaSpinner,
  FaArrowLeft
} from 'react-icons/fa';
import apiClient from '../services/api';
import Loading from '../components/Loading';
import './Payment.css';

const Payment = () => {
  const { orderId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  
  const [step, setStep] = useState('select'); // select, process, status
  const [paymentMethods, setPaymentMethods] = useState([]);
  const [selectedMethod, setSelectedMethod] = useState(null);
  const [selectedDetail, setSelectedDetail] = useState(null);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [payment, setPayment] = useState(null);
  const [plan, setPlan] = useState(null);
  const [error, setError] = useState(null);
  const [countdown, setCountdown] = useState(null);
  const [copied, setCopied] = useState(false);
  
  // Get plan from location state or URL params
  const planFromState = location.state?.plan;
  const planIdFromParams = new URLSearchParams(location.search).get('plan_id');

  useEffect(() => {
    if (orderId) {
      // If we have orderId, show payment status
      setStep('status');
      fetchPaymentStatus();
    } else if (planFromState) {
      setPlan(planFromState);
      fetchPaymentMethods();
    } else if (planIdFromParams) {
      // Fetch plan info
      fetchPlanAndMethods();
    } else {
      // No plan selected, redirect to membership page
      navigate('/membership');
    }
  }, [orderId, planFromState, planIdFromParams]);

  // Countdown timer for pending payment
  useEffect(() => {
    if (payment?.status === 'pending' && payment?.expired_at) {
      const interval = setInterval(() => {
        const expiredAt = new Date(payment.expired_at);
        const now = new Date();
        const diff = expiredAt - now;
        
        if (diff <= 0) {
          setCountdown('Expired');
          clearInterval(interval);
          fetchPaymentStatus(); // Refresh status
        } else {
          const hours = Math.floor(diff / (1000 * 60 * 60));
          const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
          const seconds = Math.floor((diff % (1000 * 60)) / 1000);
          setCountdown(`${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`);
        }
      }, 1000);
      
      return () => clearInterval(interval);
    }
  }, [payment]);

  const fetchPaymentMethods = async () => {
    try {
      const response = await apiClient.get('/payment/methods');
      setPaymentMethods(response.data.data || []);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching payment methods:', err);
      setError('Failed to load payment methods');
      setLoading(false);
    }
  };

  const fetchPlanAndMethods = async () => {
    try {
      const [plansResponse, methodsResponse] = await Promise.all([
        apiClient.get('/membership/plans'),
        apiClient.get('/payment/methods')
      ]);
      
      const plans = plansResponse.data.data || [];
      const selectedPlan = plans.find(p => p.id === parseInt(planIdFromParams));
      
      if (selectedPlan) {
        setPlan(selectedPlan);
        setPaymentMethods(methodsResponse.data.data || []);
      } else {
        navigate('/membership');
      }
      
      setLoading(false);
    } catch (err) {
      console.error('Error:', err);
      setError('Failed to load data');
      setLoading(false);
    }
  };

  const fetchPaymentStatus = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get(`/payment/${orderId}/status`);
      setPayment(response.data.data);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching payment status:', err);
      setError('Payment not found');
      setLoading(false);
    }
  };

  const handleMethodSelect = (method) => {
    setSelectedMethod(method);
    setSelectedDetail(null);
  };

  const handleDetailSelect = (detail) => {
    setSelectedDetail(detail);
  };

  const handleCreatePayment = async () => {
    if (!selectedMethod) {
      alert('Please select a payment method');
      return;
    }
    
    try {
      setProcessing(true);
      
      const response = await apiClient.post('/payment/create', {
        plan_id: plan.id,
        payment_method: selectedMethod.id,
        payment_detail: selectedDetail?.code || null
      });
      
      if (response.data.status === 'success') {
        setPayment(response.data.data);
        setStep('process');
      }
    } catch (err) {
      console.error('Error creating payment:', err);
      alert(err.response?.data?.message || 'Failed to create payment');
    } finally {
      setProcessing(false);
    }
  };

  const handleSimulatePayment = async (action) => {
    try {
      setProcessing(true);
      const response = await apiClient.post(`/payment/${payment.order_id}/simulate`, {
        action: action
      });
      
      if (response.data.status === 'success') {
        setPayment(response.data.data.payment || response.data.data);
        if (action === 'success') {
          alert('🎉 Payment successful! Your membership is now active.');
        }
      }
    } catch (err) {
      console.error('Error:', err);
      alert(err.response?.data?.message || 'Failed to process');
    } finally {
      setProcessing(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getMethodIcon = (methodId) => {
    switch (methodId) {
      case 'bank_transfer': return <FaUniversity />;
      case 'e_wallet': return <FaWallet />;
      case 'qris': return <FaQrcode />;
      case 'credit_card': return <FaCreditCard />;
      default: return <FaCreditCard />;
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

  if (loading) {
    return <Loading message="Loading..." />;
  }

  if (error) {
    return (
      <div className="payment-page">
        <div className="error-container">
          <FaTimesCircle size={48} />
          <h2>{error}</h2>
          <button onClick={() => navigate('/membership')} className="btn-primary">
            Back to Membership
          </button>
        </div>
      </div>
    );
  }

  // Payment Status View (when we have orderId)
  if (step === 'status' && payment) {
    return (
      <div className="payment-page">
        <div className="payment-status-container">
          <div className="status-header">
            {getStatusIcon(payment.status)}
            <h1>
              {payment.status === 'success' && 'Payment Successful!'}
              {payment.status === 'pending' && 'Waiting for Payment'}
              {payment.status === 'processing' && 'Processing Payment'}
              {payment.status === 'failed' && 'Payment Failed'}
              {payment.status === 'expired' && 'Payment Expired'}
            </h1>
          </div>

          <div className="payment-details-card">
            <div className="detail-row">
              <span className="label">Order ID</span>
              <span className="value">{payment.order_id}</span>
            </div>
            <div className="detail-row">
              <span className="label">Plan</span>
              <span className="value">{payment.membership_plan}</span>
            </div>
            <div className="detail-row">
              <span className="label">Amount</span>
              <span className="value amount">Rp {payment.amount?.toLocaleString('id-ID')}</span>
            </div>
            <div className="detail-row">
              <span className="label">Status</span>
              <span className={`status-badge ${payment.status}`}>{payment.status.toUpperCase()}</span>
            </div>
            {payment.status === 'pending' && countdown && (
              <div className="detail-row">
                <span className="label">Time Remaining</span>
                <span className="value countdown">{countdown}</span>
              </div>
            )}
            {payment.va_number && payment.status === 'pending' && (
              <div className="va-section">
                <h4>Virtual Account Number</h4>
                <div className="va-number">
                  <span>{payment.va_number}</span>
                  <button onClick={() => copyToClipboard(payment.va_number)} className="btn-copy">
                    <FaCopy /> {copied ? 'Copied!' : 'Copy'}
                  </button>
                </div>
              </div>
            )}
            {payment.transaction_id && (
              <div className="detail-row">
                <span className="label">Transaction ID</span>
                <span className="value">{payment.transaction_id}</span>
              </div>
            )}
            {payment.paid_at && (
              <div className="detail-row">
                <span className="label">Paid At</span>
                <span className="value">{new Date(payment.paid_at).toLocaleString('id-ID')}</span>
              </div>
            )}
          </div>

          {/* Simulation buttons for testing */}
          {payment.status === 'pending' && (
            <div className="simulation-section">
              <p className="simulation-note">🧪 Testing Mode: Simulate payment result</p>
              <div className="simulation-buttons">
                <button 
                  onClick={() => handleSimulatePayment('success')} 
                  className="btn-simulate success"
                  disabled={processing}
                >
                  {processing ? <FaSpinner className="spin" /> : <FaCheckCircle />}
                  Simulate Success
                </button>
                <button 
                  onClick={() => handleSimulatePayment('failed')} 
                  className="btn-simulate failed"
                  disabled={processing}
                >
                  {processing ? <FaSpinner className="spin" /> : <FaTimesCircle />}
                  Simulate Failed
                </button>
              </div>
            </div>
          )}

          <div className="action-buttons">
            {payment.status === 'success' && (
              <button onClick={() => navigate('/profile')} className="btn-primary">
                View My Membership
              </button>
            )}
            {(payment.status === 'failed' || payment.status === 'expired') && (
              <button onClick={() => navigate('/membership')} className="btn-primary">
                Try Again
              </button>
            )}
            <button onClick={() => navigate('/membership')} className="btn-secondary">
              Back to Membership
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Payment Process View (after creating payment)
  if (step === 'process' && payment) {
    return (
      <div className="payment-page">
        <div className="payment-process-container">
          <div className="process-header">
            <FaClock className="process-icon" />
            <h1>Complete Your Payment</h1>
            <p className="order-id">Order ID: {payment.order_id}</p>
          </div>

          <div className="payment-summary-card">
            <h3>Payment Summary</h3>
            <div className="summary-row">
              <span>{plan?.name || payment.membership_plan} Membership</span>
              <span>Rp {payment.subtotal?.toLocaleString('id-ID') || payment.amount?.toLocaleString('id-ID')}</span>
            </div>
            {payment.admin_fee > 0 && (
              <div className="summary-row">
                <span>Admin Fee</span>
                <span>Rp {payment.admin_fee?.toLocaleString('id-ID')}</span>
              </div>
            )}
            <div className="summary-row total">
              <span>Total</span>
              <span>Rp {payment.total?.toLocaleString('id-ID') || payment.amount?.toLocaleString('id-ID')}</span>
            </div>
          </div>

          {payment.va_number && (
            <div className="va-card">
              <h3>Virtual Account Number</h3>
              <div className="va-display">
                <span className="va-number-large">{payment.va_number}</span>
                <button onClick={() => copyToClipboard(payment.va_number)} className="btn-copy-large">
                  <FaCopy /> {copied ? 'Copied!' : 'Copy'}
                </button>
              </div>
            </div>
          )}

          {payment.instructions && (
            <div className="instructions-card">
              <h3>Payment Instructions</h3>
              <ol className="instructions-list">
                {payment.instructions.map((instruction, index) => (
                  <li key={index}>{instruction}</li>
                ))}
              </ol>
            </div>
          )}

          {countdown && (
            <div className="countdown-section">
              <p>Pay before</p>
              <div className="countdown-timer">{countdown}</div>
            </div>
          )}

          {/* Simulation for testing */}
          <div className="simulation-section">
            <p className="simulation-note">🧪 Testing Mode: Simulate payment</p>
            <div className="simulation-buttons">
              <button 
                onClick={() => handleSimulatePayment('success')} 
                className="btn-simulate success"
                disabled={processing}
              >
                {processing ? <FaSpinner className="spin" /> : <FaCheckCircle />}
                Pay Now (Simulate Success)
              </button>
            </div>
          </div>

          <button onClick={() => navigate('/membership')} className="btn-back">
            <FaArrowLeft /> Cancel Payment
          </button>
        </div>
      </div>
    );
  }

  // Payment Method Selection View
  return (
    <div className="payment-page">
      <div className="payment-container">
        <button onClick={() => navigate('/membership')} className="btn-back-top">
          <FaArrowLeft /> Back
        </button>

        <div className="payment-header">
          <h1>Choose Payment Method</h1>
          <p>Select your preferred payment method</p>
        </div>

        {/* Plan Summary */}
        {plan && (
          <div className="plan-summary-card">
            <h3>{plan.name} Membership</h3>
            <p className="plan-duration">{plan.duration_days} Days</p>
            <p className="plan-price">Rp {plan.price?.toLocaleString('id-ID')}</p>
          </div>
        )}

        {/* Payment Methods */}
        <div className="payment-methods">
          {paymentMethods.map((method) => (
            <div key={method.id} className="method-section">
              <div 
                className={`method-header ${selectedMethod?.id === method.id ? 'selected' : ''}`}
                onClick={() => handleMethodSelect(method)}
              >
                <div className="method-info">
                  {getMethodIcon(method.id)}
                  <div>
                    <h4>{method.name}</h4>
                    <p>{method.description}</p>
                  </div>
                </div>
                <div className={`radio-circle ${selectedMethod?.id === method.id ? 'checked' : ''}`} />
              </div>

              {/* Sub-options for banks/wallets */}
              {selectedMethod?.id === method.id && (method.banks || method.wallets) && (
                <div className="method-options">
                  {(method.banks || method.wallets)?.map((option) => (
                    <div 
                      key={option.code}
                      className={`option-item ${selectedDetail?.code === option.code ? 'selected' : ''}`}
                      onClick={() => handleDetailSelect(option)}
                    >
                      <span className="option-name">{option.name}</span>
                      {option.admin_fee > 0 && (
                        <span className="option-fee">+Rp {option.admin_fee.toLocaleString('id-ID')}</span>
                      )}
                      <div className={`radio-circle small ${selectedDetail?.code === option.code ? 'checked' : ''}`} />
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Total & Pay Button */}
        <div className="payment-footer">
          <div className="total-section">
            <span>Total Payment</span>
            <span className="total-amount">
              Rp {((plan?.price || 0) + (selectedDetail?.admin_fee || 0)).toLocaleString('id-ID')}
            </span>
          </div>
          <button 
            onClick={handleCreatePayment} 
            className="btn-pay"
            disabled={!selectedMethod || processing || (selectedMethod?.banks && !selectedDetail) || (selectedMethod?.wallets && !selectedDetail)}
          >
            {processing ? (
              <>
                <FaSpinner className="spin" /> Processing...
              </>
            ) : (
              'Pay Now'
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Payment;
