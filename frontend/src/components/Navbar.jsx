import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { FaDumbbell, FaBars, FaTimes } from "react-icons/fa";
import "./Navbar.css";

const Navbar = () => {
  const [user, setUser] = useState(null);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem("token");
    const userData = localStorage.getItem("user");

    if (token && userData) {
      setUser(JSON.parse(userData));
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setUser(null);
    navigate("/login");
    setIsMobileMenuOpen(false);
  };

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const closeMobileMenu = () => {
    setIsMobileMenuOpen(false);
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo" onClick={closeMobileMenu}>
          <FaDumbbell className="logo-icon" />
          <span>FitZone Gym</span>
        </Link>

        <button className="mobile-menu-toggle" onClick={toggleMobileMenu}>
          {isMobileMenuOpen ? <FaTimes /> : <FaBars />}
        </button>

        <ul className={`navbar-menu ${isMobileMenuOpen ? 'active' : ''}`}>
          <li>
            <Link to="/" onClick={closeMobileMenu}>Home</Link>
          </li>
          <li>
            <Link to="/classes" onClick={closeMobileMenu}>Classes</Link>
          </li>
          <li>
            <Link to="/membership" onClick={closeMobileMenu}>Membership</Link>
          </li>

          {user ? (
            <>
              <li>
                <Link to="/my-bookings" onClick={closeMobileMenu}>My Bookings</Link>
              </li>
              <li>
                <Link to="/profile" onClick={closeMobileMenu}>Profile</Link>
              </li>
              {user.role === "TRAINER" && (
                <li>
                  <Link to="/manage-classes" onClick={closeMobileMenu}>Manage</Link>
                </li>
              )}
              {user.role === "ADMIN" && (
                <li>
                  <Link to="/admin" onClick={closeMobileMenu}>Admin</Link>
                </li>
              )}
              <li className="navbar-user">
                <span className="user-name">{user.name}</span>
                <button onClick={handleLogout} className="btn-logout">
                  Logout
                </button>
              </li>
            </>
          ) : (
            <>
              <li>
                <Link to="/login" className="nav-btn btn-login" onClick={closeMobileMenu}>
                  Login
                </Link>
              </li>
              <li>
                <Link to="/register" className="nav-btn btn-register" onClick={closeMobileMenu}>
                  Join Now
                </Link>
              </li>
            </>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
