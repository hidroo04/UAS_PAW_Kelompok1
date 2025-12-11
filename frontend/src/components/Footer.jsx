import React from "react";
import "./Footer.css";

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-section">
          <h3>GymBook</h3>
          <p>Your complete gym class booking solution</p>
        </div>

        <div className="footer-section">
          <h4>Quick Links</h4>
          <ul>
            <li>
              <a href="/">Home</a>
            </li>
            <li>
              <a href="/classes">Classes</a>
            </li>
            <li>
              <a href="/membership">Membership</a>
            </li>
          </ul>
        </div>

        <div className="footer-section">
          <h4>Contact</h4>
          <p>📧 info@gymbook.com</p>
          <p>📱 +62 123 456 7890</p>
        </div>
      </div>

      <div className="footer-bottom">
        <p>&copy; 2025 GymBook - UAS Pengweb. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;
