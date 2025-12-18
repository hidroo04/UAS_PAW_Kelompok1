import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaCheck, FaCrown, FaStar, FaBolt, FaExclamationTriangle } from 'react-icons/fa';
import apiClient from '../services/api';
import Loading from '../components/Loading';
import './MembershipPlans.css';

const MembershipPlans = () => {
  const [plans, setPlans] = useState([]);
  const [currentMembership, setCurrentMembership] = useState(null);
  const [loading, setLoading] = useState(true);
  const [subscribing, setSubscribing] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  const isLoggedIn = !!localStorage.getItem('token');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      
      // Fetch plans
      const plansResponse = await apiClient.get('/membership/plans');
      setPlans(plansResponse.data.data || []);
      
      // Fetch current membership if logged in
      if (isLoggedIn && user.role === 'member') {
        try {
          const membershipResponse = await apiClient.get('/membership/my');
          setCurrentMembership(membershipResponse.data.data);
        } catch (err) {
          // Member mungkin belum punya membership
          setCurrentMembership(null);
        }
      }
      
      setError(null);
    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Failed to load membership plans');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectPlan = async (planId) => {
    // Check if logged in
    if (!isLoggedIn) {
      alert('Please login first to subscribe to a membership plan');
      navigate('/login');
      return;
    }
    
    // Check if user is member
    if (user.role !== 'member') {
      alert('Only members can subscribe to membership plans');
      return;
    }
    
    // Check if already has active membership
    if (currentMembership?.is_active) {
      alert(`You already have an active ${currentMembership.membership_plan} membership until ${currentMembership.expiry_date}`);
      return;
    }
    
    // Navigate to payment page with plan info
    const plan = plans.find(p => p.id === planId);
    navigate('/payment', { state: { plan } });
  };

  const getPlanIcon = (name) => {
    if (name.toLowerCase().includes('basic')) return <FaBolt />;
    if (name.toLowerCase().includes('premium')) return <FaStar />;
    if (name.toLowerCase().includes('vip') || name.toLowerCase().includes('elite')) return <FaCrown />;
    return <FaStar />;
  };

  if (loading) {
    return <Loading message="Loading membership plans..." />;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="membership-plans-page">
      <div className="page-header">
        <h1>Choose Your Plan</h1>
        <p>Select the perfect membership plan to achieve your fitness goals</p>
      </div>

      {/* Current Membership Status */}
      {isLoggedIn && user.role === 'member' && (
        <div className={`current-membership-banner ${currentMembership?.is_active ? 'active' : 'inactive'}`}>
          {currentMembership?.is_active ? (
            <>
              <div className="membership-status">
                <FaCheck className="status-icon" />
                <div className="status-info">
                  <h3>Active Membership: {currentMembership.membership_plan}</h3>
                  <p>Valid until: {currentMembership.expiry_date} ({currentMembership.days_remaining} days remaining)</p>
                  <p className="class-usage">
                    📅 Kelas bulan ini: {currentMembership.class_limit_text || 
                      (currentMembership.class_limit === -1 ? 'Unlimited' : 
                        `${currentMembership.monthly_bookings || 0}/${currentMembership.class_limit || 0} kelas`)}
                    {currentMembership.remaining_classes !== -1 && currentMembership.remaining_classes !== undefined && (
                      <span className="remaining"> (Sisa: {currentMembership.remaining_classes} kelas)</span>
                    )}
                  </p>
                </div>
              </div>
            </>
          ) : (
            <>
              <div className="membership-status">
                <FaExclamationTriangle className="status-icon warning" />
                <div className="status-info">
                  <h3>No Active Membership</h3>
                  <p>Subscribe to a plan below to start booking classes!</p>
                </div>
              </div>
            </>
          )}
        </div>
      )}

      <div className="plans-grid">
        {plans.map((plan) => (
          <div 
            key={plan.id} 
            className={`plan-card ${plan.is_popular ? 'popular' : ''} ${currentMembership?.membership_plan === plan.name ? 'current' : ''}`}
          >
            {plan.is_popular && <div className="popular-badge">Most Popular</div>}
            {currentMembership?.membership_plan === plan.name && currentMembership?.is_active && (
              <div className="current-badge">Current Plan</div>
            )}
            
            <div className="plan-icon">
              {getPlanIcon(plan.name)}
            </div>

            <h3 className="plan-name">{plan.name}</h3>
            
            <div className="plan-price">
              <span className="currency">Rp</span>
              <span className="amount">{plan.price.toLocaleString('id-ID')}</span>
              <span className="period">/month</span>
            </div>

            <p className="plan-description">{plan.description}</p>

            <ul className="plan-features">
              {plan.features && plan.features.map((feature, index) => (
                <li key={index}>
                  <FaCheck /> {feature}
                </li>
              ))}
            </ul>

            <button 
              className={`btn-select-plan ${currentMembership?.is_active ? 'disabled' : ''}`}
              onClick={() => handleSelectPlan(plan.id)}
              disabled={subscribing || (currentMembership?.is_active && currentMembership?.membership_plan === plan.name)}
            >
              {subscribing ? 'Processing...' : 
               currentMembership?.is_active && currentMembership?.membership_plan === plan.name ? 'Current Plan' :
               currentMembership?.is_active ? 'Already Subscribed' :
               'Select Plan'}
            </button>
          </div>
        ))}
      </div>

      <div className="membership-benefits">
        <h2>Membership Benefits</h2>
        <div className="benefits-grid">
          <div className="benefit-item" data-aos="fade-up">
            <div className="benefit-icon">🏋️</div>
            <h4>State-of-the-art Equipment</h4>
            <p>Access to top-quality gym equipment and facilities</p>
          </div>
          <div className="benefit-item" data-aos="fade-up" data-aos-delay="100">
            <div className="benefit-icon">👨‍🏫</div>
            <h4>Expert Trainers</h4>
            <p>Certified professionals to guide your fitness journey</p>
          </div>
          <div className="benefit-item" data-aos="fade-up" data-aos-delay="200">
            <div className="benefit-icon">📅</div>
            <h4>Flexible Schedule</h4>
            <p>Classes available throughout the day to fit your routine</p>
          </div>
          <div className="benefit-item" data-aos="fade-up" data-aos-delay="300">
            <div className="benefit-icon">💪</div>
            <h4>Diverse Classes</h4>
            <p>Wide variety of fitness classes for all levels</p>
          </div>
        </div>
      </div>

      <div className="faq-section">
        <h2>Frequently Asked Questions</h2>
        <div className="faq-list">
          <div className="faq-item" data-aos="fade-right">
            <h4>Can I cancel my membership?</h4>
            <p>Yes, you can cancel anytime. No long-term commitments required.</p>
          </div>
          <div className="faq-item" data-aos="fade-right" data-aos-delay="100">
            <h4>Can I upgrade my plan?</h4>
            <p>Absolutely! You can upgrade to a higher tier at any time.</p>
          </div>
          <div className="faq-item" data-aos="fade-right" data-aos-delay="200">
            <h4>Are there any hidden fees?</h4>
            <p>No hidden fees. The price you see is the price you pay.</p>
          </div>
          <div className="faq-item" data-aos="fade-right" data-aos-delay="300">
            <h4>Can I freeze my membership?</h4>
            <p>Yes, you can freeze your membership for up to 30 days per year.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MembershipPlans;
