import React from "react";
import { Link } from "react-router-dom";
import "./Home.css";

const Home = () => {
  return (
    <div className="home-page">
      <section className="hero">
        <div className="hero-content">
          <h1>Welcome to GymBook</h1>
          <p className="hero-subtitle">
            Your Complete Gym Class Booking System
          </p>
          <p>Book classes, track attendance, and manage your fitness journey</p>
          <div className="hero-buttons">
            <Link to="/classes" className="btn btn-primary">
              Browse Classes
            </Link>
            <Link to="/register" className="btn btn-secondary">
              Get Started
            </Link>
          </div>
        </div>
      </section>

      <section className="features">
        <h2>Why Choose GymBook?</h2>
        <div className="features-grid">
          <div className="feature-card">
            <span className="feature-icon">📅</span>
            <h3>Easy Booking</h3>
            <p>Book your favorite classes with just a few clicks</p>
          </div>
          <div className="feature-card">
            <span className="feature-icon">👨‍🏫</span>
            <h3>Expert Trainers</h3>
            <p>Learn from certified and experienced trainers</p>
          </div>
          <div className="feature-card">
            <span className="feature-icon">📊</span>
            <h3>Track Progress</h3>
            <p>Monitor your attendance and fitness progress</p>
          </div>
          <div className="feature-card">
            <span className="feature-icon">💪</span>
            <h3>Various Classes</h3>
            <p>Choose from yoga, HIIT, strength training and more</p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
