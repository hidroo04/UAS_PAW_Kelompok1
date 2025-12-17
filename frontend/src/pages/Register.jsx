import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { HiUser, HiMail, HiLockClosed, HiUserGroup, HiCheckCircle } from "react-icons/hi";
import apiClient from "../services/api";
import "./Auth.css";

const Register = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
    role: "member",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (formData.password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }

    setLoading(true);

    try {
      const response = await apiClient.post("/auth/register", {
        name: formData.name,
        email: formData.email,
        password: formData.password,
        role: formData.role,
      });

      if (response.data.status === "success") {
        localStorage.setItem("token", response.data.token);
        localStorage.setItem("user", JSON.stringify(response.data.data));
        localStorage.setItem("userRole", response.data.data.role);
        navigate("/");
        window.location.reload();
      }
    } catch (err) {
      setError(err.response?.data?.message || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container register-page">
      <div className="auth-card">
        <div className="auth-header">
          <div className="auth-icon">
            <HiUserGroup />
          </div>
          <h2>Create Account</h2>
          <p className="auth-subtitle">Join FitZone Gym today</p>
        </div>

        {error && <div className="alert alert-error">{error}</div>}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label><HiUser /> Full Name</label>
            <div className="input-wrapper">
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                placeholder="Enter your full name"
              />
            </div>
          </div>

          <div className="form-group">
            <label><HiMail /> Email Address</label>
            <div className="input-wrapper">
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                placeholder="Enter your email"
              />
            </div>
          </div>

          <div className="form-group">
            <label><HiLockClosed /> Password</label>
            <div className="input-wrapper">
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                placeholder="Create a password (min. 6 characters)"
              />
            </div>
          </div>

          <div className="form-group">
            <label><HiCheckCircle /> Confirm Password</label>
            <div className="input-wrapper">
              <input
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
                placeholder="Confirm your password"
              />
            </div>
          </div>

          <div className="form-group">
            <label><HiUserGroup /> Account Type</label>
            <div className="role-selection">
              <div 
                className={`role-option ${formData.role === 'member' ? 'active' : ''}`}
                onClick={() => setFormData({ ...formData, role: 'member' })}
              >
                <div className="role-icon">👤</div>
                <div className="role-info">
                  <h4>Member</h4>
                  <p>Book classes & track fitness</p>
                </div>
              </div>
              <div 
                className={`role-option ${formData.role === 'trainer' ? 'active' : ''}`}
                onClick={() => setFormData({ ...formData, role: 'trainer' })}
              >
                <div className="role-icon">💪</div>
                <div className="role-info">
                  <h4>Trainer</h4>
                  <p>Manage classes & members</p>
                </div>
              </div>
            </div>
          </div>

          <button type="submit" className="btn-submit" disabled={loading}>
            {loading ? (
              <>
                <span className="spinner"></span>
                Creating Account...
              </>
            ) : (
              <>
                <HiCheckCircle /> Create Account
              </>
            )}
          </button>
        </form>

        <div className="auth-footer">
          <p className="auth-link">
            Already have an account? <Link to="/login">Sign In</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;
