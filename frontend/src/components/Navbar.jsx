import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Navbar.css";

const Navbar = () => {
  const [user, setUser] = useState(null);
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
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          <span className="logo-icon">💪</span>
          GymBook
        </Link>

        <ul className="navbar-menu">
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/classes">Classes</Link>
          </li>

          {user ? (
            <>
              <li>
                <Link to="/my-bookings">My Bookings</Link>
              </li>
              {user.role === "trainer" && (
                <li>
                  <Link to="/manage-classes">Manage Classes</Link>
                </li>
              )}
              {user.role === "admin" && (
                <li>
                  <Link to="/admin">Admin</Link>
                </li>
              )}
              <li>
                <Link to="/membership">Membership</Link>
              </li>
              <li className="navbar-user">
                <span>{user.name}</span>
                <button onClick={handleLogout} className="btn-logout">
                  Logout
                </button>
              </li>
            </>
          ) : (
            <>
              <li>
                <Link to="/login" className="btn-primary">
                  Login
                </Link>
              </li>
              <li>
                <Link to="/register" className="btn-secondary">
                  Register
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
