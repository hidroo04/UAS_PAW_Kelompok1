import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { FaDumbbell, FaBars, FaTimes, FaChevronDown } from "react-icons/fa";
import { 
  HiChartBar, 
  HiUsers, 
  HiAcademicCap, 
  HiCalendar, 
  HiClipboardCheck,
  HiCreditCard,
  HiUserGroup
} from "react-icons/hi";
import "./Navbar.css";

const Navbar = () => {
  const [user, setUser] = useState(null);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isAdminDropdownOpen, setIsAdminDropdownOpen] = useState(false);
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
    localStorage.removeItem("userRole");
    setUser(null);
    navigate("/login");
    setIsMobileMenuOpen(false);
  };

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const closeMobileMenu = () => {
    setIsMobileMenuOpen(false);
    setIsAdminDropdownOpen(false);
  };

  const toggleAdminDropdown = () => {
    setIsAdminDropdownOpen(!isAdminDropdownOpen);
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo" onClick={closeMobileMenu}>
          <FaDumbbell className="logo-icon" />
          <span>Hydroo Gym</span>
        </Link>

        <button className="mobile-menu-toggle" onClick={toggleMobileMenu}>
          {isMobileMenuOpen ? <FaTimes /> : <FaBars />}
        </button>

        <ul className={`navbar-menu ${isMobileMenuOpen ? 'active' : ''}`}>
          {(!user || (user && user.role === "member")) && (
            <>
              <li>
                <Link to="/" onClick={closeMobileMenu}>Home</Link>
              </li>
              <li>
                <Link to="/classes" onClick={closeMobileMenu}>Classes</Link>
              </li>
              <li>
                <Link to="/membership" onClick={closeMobileMenu}>Membership</Link>
              </li>
            </>
          )}

          {user ? (
            <>
              {user.role === "admin" ? (
                <>
                  <li className="admin-dropdown">
                    <button 
                      className="admin-toggle"
                      onClick={toggleAdminDropdown}
                    >
                      Admin Panel <FaChevronDown className={`dropdown-icon ${isAdminDropdownOpen ? 'open' : ''}`} />
                    </button>
                    <ul className={`admin-submenu ${isAdminDropdownOpen ? 'show' : ''}`}>
                      <li>
                        <Link to="/admin/dashboard" onClick={closeMobileMenu}>
                          <HiChartBar /> Dashboard
                        </Link>
                      </li>
                      <li>
                        <Link to="/admin/members" onClick={closeMobileMenu}>
                          <HiUsers /> Members
                        </Link>
                      </li>
                      <li>
                        <Link to="/admin/classes" onClick={closeMobileMenu}>
                          <HiAcademicCap /> Classes
                        </Link>
                      </li>
                      <li>
                        <Link to="/admin/bookings" onClick={closeMobileMenu}>
                          <HiCalendar /> All Bookings
                        </Link>
                      </li>
                      <li>
                        <Link to="/admin/attendance" onClick={closeMobileMenu}>
                          <HiClipboardCheck /> Attendance
                        </Link>
                      </li>
                      <li>
                        <Link to="/admin/payments" onClick={closeMobileMenu}>
                          <HiCreditCard /> Payments
                        </Link>
                      </li>
                      <li>
                        <Link to="/admin/trainers" onClick={closeMobileMenu}>
                          <HiUserGroup /> Trainers
                        </Link>
                      </li>
                    </ul>
                  </li>
                  <li>
                    <Link to="/profile" onClick={closeMobileMenu}>Profile</Link>
                  </li>
                </>
              ) : user.role === "trainer" ? (
                <>
                  <li>
                    <Link to="/trainer/my-classes" onClick={closeMobileMenu}>My Classes</Link>
                  </li>
                  <li>
                    <Link to="/trainer/manage-classes" onClick={closeMobileMenu}>Manage Classes</Link>
                  </li>
                  <li>
                    <Link to="/trainer/calendar" onClick={closeMobileMenu}>Calendar</Link>
                  </li>
                  <li>
                    <Link to="/profile" onClick={closeMobileMenu}>Profile</Link>
                  </li>
                </>
              ) : (
                <>
                  <li>
                    <Link to="/my-bookings" onClick={closeMobileMenu}>My Bookings</Link>
                  </li>
                  <li>
                    <Link to="/profile" onClick={closeMobileMenu}>Profile</Link>
                  </li>
                </>
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
