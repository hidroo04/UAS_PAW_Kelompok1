import React from "react";
import { Link } from "react-router-dom";
import { FaDumbbell, FaFacebook, FaInstagram, FaTwitter, FaYoutube, FaEnvelope, FaPhone, FaMapMarkerAlt } from "react-icons/fa";
import "./Footer.css";

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-section footer-about">
          <div className="footer-logo">
            <FaDumbbell className="footer-logo-icon" />
            <h3>Hydroo Gym</h3>
          </div>
          <p>Transform your body, elevate your mind, and achieve your fitness goals with our world-class facilities and expert trainers.</p>
          <div className="social-links">
            <a href="#" aria-label="Facebook"><FaFacebook /></a>
            <a href="#" aria-label="Instagram"><FaInstagram /></a>
            <a href="#" aria-label="Twitter"><FaTwitter /></a>
            <a href="#" aria-label="YouTube"><FaYoutube /></a>
          </div>
        </div>

        <div className="footer-section">
          <h4>Quick Links</h4>
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/classes">Classes</Link></li>
            <li><Link to="/membership">Membership</Link></li>
            <li><Link to="/register">Join Now</Link></li>
          </ul>
        </div>

        <div className="footer-section">
          <h4>Classes</h4>
          <ul>
            <li><a href="#">Yoga</a></li>
            <li><a href="#">HIIT Training</a></li>
            <li><a href="#">Strength Training</a></li>
            <li><a href="#">Cardio</a></li>
          </ul>
        </div>

        <div className="footer-section">
          <h4>Contact Us</h4>
          <ul className="contact-info">
            <li>
              <FaMapMarkerAlt className="contact-icon" />
              <span>123 Fitness Street, Jakarta</span>
            </li>
            <li>
              <FaEnvelope className="contact-icon" />
              <span>info@hydroogym.com</span>
            </li>
            <li>
              <FaPhone className="contact-icon" />
              <span>+62 123 456 7890</span>
            </li>
          </ul>
          <div className="footer-hours">
            <strong>Open Hours:</strong>
            <p>Mon - Fri: 6:00 AM - 10:00 PM</p>
            <p>Sat - Sun: 7:00 AM - 9:00 PM</p>
          </div>
        </div>
      </div>

      <div className="footer-bottom">
        <p>&copy; 2025 Hydroo Gym - UAS PAW Kelompok 1. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;
