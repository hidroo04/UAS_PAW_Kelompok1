import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { FaCalendarAlt, FaUserTie, FaChartLine, FaDumbbell, FaFire, FaHeartbeat, FaUsers, FaTrophy } from "react-icons/fa";
import "./Home.css";
import homeImage from "../assets/home.jpg";
import homeImage1 from "../assets/home1.jpg";
import homeImage2 from "../assets/home2.jpg";

// Background images for hero slideshow
const heroImages = [
  homeImage,
  homeImage1,
  homeImage2
];

const Home = () => {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  // Auto-rotate background images
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentImageIndex((prevIndex) => 
        prevIndex === heroImages.length - 1 ? 0 : prevIndex + 1
      );
    }, 5000); // Change every 5 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="home-page">
      {/* Hero Section with Slideshow */}
      <section className="hero">
        {/* Background Images */}
        {heroImages.map((image, index) => (
          <div
            key={index}
            className={`hero-bg ${index === currentImageIndex ? 'active' : ''}`}
            style={{ backgroundImage: `url(${image})` }}
          />
        ))}
        <div className="hero-overlay"></div>
        <div className="hero-content container" data-aos="fade-up">
          <h1 className="hero-title">Transform Your Body, <span className="highlight">Elevate Your Mind</span></h1>
          <p className="hero-subtitle">
            Experience world-class fitness training with expert coaches and state-of-the-art facilities
          </p>
          <p className="hero-description">Join thousands of members achieving their fitness goals every day</p>
          <div className="hero-buttons">
            <Link to="/classes" className="btn btn-primary btn-large">
              <FaCalendarAlt /> Browse Classes
            </Link>
            <Link to="/register" className="btn btn-outline btn-large">
              <FaDumbbell /> Join Now
            </Link>
          </div>
          
          {/* Slideshow Indicators */}
          <div className="hero-indicators">
            {heroImages.map((_, index) => (
              <button
                key={index}
                className={`indicator ${index === currentImageIndex ? 'active' : ''}`}
                onClick={() => setCurrentImageIndex(index)}
                aria-label={`Go to slide ${index + 1}`}
              />
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats-section" data-aos="fade-up">
        <div className="container">
          <div className="stats-grid">
            <div className="stat-card" data-aos="zoom-in" data-aos-delay="100">
              <FaUsers className="stat-icon" />
              <h3 className="stat-number">5000+</h3>
              <p className="stat-label">Active Members</p>
            </div>
            <div className="stat-card" data-aos="zoom-in" data-aos-delay="200">
              <FaUserTie className="stat-icon" />
              <h3 className="stat-number">50+</h3>
              <p className="stat-label">Expert Trainers</p>
            </div>
            <div className="stat-card" data-aos="zoom-in" data-aos-delay="300">
              <FaDumbbell className="stat-icon" />
              <h3 className="stat-number">100+</h3>
              <p className="stat-label">Weekly Classes</p>
            </div>
            <div className="stat-card" data-aos="zoom-in" data-aos-delay="400">
              <FaTrophy className="stat-icon" />
              <h3 className="stat-number">10+</h3>
              <p className="stat-label">Years Experience</p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="container">
          <div className="section-header" data-aos="fade-up">
            <h2 className="section-title">Why Choose Hydroo Gym?</h2>
            <p className="section-subtitle">
              Discover the benefits that make us the premier fitness destination
            </p>
          </div>
          <div className="features-grid">
            <div className="feature-card" data-aos="fade-up" data-aos-delay="100">
              <div className="feature-icon-wrapper">
                <FaCalendarAlt className="feature-icon" />
              </div>
              <h3>Easy Booking</h3>
              <p>Book your favorite classes with just a few clicks. Simple, fast, and convenient scheduling system.</p>
            </div>
            <div className="feature-card" data-aos="fade-up" data-aos-delay="200">
              <div className="feature-icon-wrapper">
                <FaUserTie className="feature-icon" />
              </div>
              <h3>Expert Trainers</h3>
              <p>Learn from certified and experienced trainers dedicated to helping you achieve your goals.</p>
            </div>
            <div className="feature-card" data-aos="fade-up" data-aos-delay="300">
              <div className="feature-icon-wrapper">
                <FaChartLine className="feature-icon" />
              </div>
              <h3>Track Progress</h3>
              <p>Monitor your attendance, workout history, and fitness progress with detailed analytics.</p>
            </div>
            <div className="feature-card" data-aos="fade-up" data-aos-delay="400">
              <div className="feature-icon-wrapper">
                <FaDumbbell className="feature-icon" />
              </div>
              <h3>Various Classes</h3>
              <p>Choose from yoga, HIIT, strength training, cardio, and more. Something for everyone.</p>
            </div>
            <div className="feature-card" data-aos="fade-up" data-aos-delay="500">
              <div className="feature-icon-wrapper">
                <FaFire className="feature-icon" />
              </div>
              <h3>Modern Equipment</h3>
              <p>State-of-the-art facilities with the latest fitness equipment for optimal workouts.</p>
            </div>
            <div className="feature-card" data-aos="fade-up" data-aos-delay="600">
              <div className="feature-icon-wrapper">
                <FaHeartbeat className="feature-icon" />
              </div>
              <h3>Health Focused</h3>
              <p>Holistic approach to fitness combining physical training with wellness programs.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section" data-aos="fade-up">
        <div className="container">
          <div className="cta-content">
            <h2>Ready to Start Your Fitness Journey?</h2>
            <p>Join our community today and get access to unlimited classes, expert guidance, and state-of-the-art facilities.</p>
            <Link to="/register" className="btn btn-primary btn-large">
              Get Started Now
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
