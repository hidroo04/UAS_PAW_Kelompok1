import { useState, useEffect } from 'react';
import { FaCheck, FaCrown, FaStar, FaBolt } from 'react-icons/fa';
import apiClient from '../services/api';
import Loading from '../components/Loading';
import './MembershipPlans.css';

const MembershipPlans = () => {
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedPlan, setSelectedPlan] = useState(null);

  useEffect(() => {
    fetchPlans();
  }, []);

  const fetchPlans = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/membership/plans');
      // Backend returns {status, data}, so we need response.data.data
      setPlans(response.data.data || []);
      setError(null);
    } catch (err) {
      console.error('Error fetching plans:', err);
      setError('Failed to load membership plans');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectPlan = async (planId) => {
    try {
      const response = await apiClient.post('/membership/subscribe', {
        plan_id: planId
      });
      alert('Membership activated successfully!');
      window.location.href = '/profile';
    } catch (err) {
      console.error('Error subscribing:', err);
      alert(err.response?.data?.message || 'Failed to activate membership');
    }
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

      <div className="plans-grid">
        {plans.map((plan) => (
          <div 
            key={plan.id} 
            className={`plan-card ${plan.is_popular ? 'popular' : ''} ${selectedPlan === plan.id ? 'selected' : ''}`}
          >
            {plan.is_popular && <div className="popular-badge">Most Popular</div>}
            
            <div className="plan-icon">
              {getPlanIcon(plan.name)}
            </div>

            <h3 className="plan-name">{plan.name}</h3>
            
            <div className="plan-price">
              <span className="currency">Rp</span>
              <span className="amount">{plan.price.toLocaleString('id-ID')}</span>
              <span className="period">/{plan.duration_days} days</span>
            </div>

            <p className="plan-description">{plan.description}</p>

            <ul className="plan-features">
              {plan.features && plan.features.map((feature, index) => (
                <li key={index}>
                  <FaCheck /> {feature}
                </li>
              ))}
              {!plan.features && (
                <>
                  <li><FaCheck /> Access to all gym equipment</li>
                  <li><FaCheck /> {plan.class_limit === -1 ? 'Unlimited' : plan.class_limit} classes per month</li>
                  <li><FaCheck /> Locker room access</li>
                  {plan.name.toLowerCase().includes('premium') && (
                    <>
                      <li><FaCheck /> Personal trainer consultation</li>
                      <li><FaCheck /> Nutrition guidance</li>
                    </>
                  )}
                  {(plan.name.toLowerCase().includes('vip') || plan.name.toLowerCase().includes('elite')) && (
                    <>
                      <li><FaCheck /> Priority class booking</li>
                      <li><FaCheck /> Spa & sauna access</li>
                      <li><FaCheck /> Guest privileges</li>
                    </>
                  )}
                </>
              )}
            </ul>

            <button 
              className="btn-select-plan"
              onClick={() => handleSelectPlan(plan.id)}
            >
              Select Plan
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
