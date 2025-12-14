import React, { useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import AOS from "aos";
import "aos/dist/aos.css";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Classes from "./pages/Classes";
import MyBookings from "./pages/MyBookings";
import UserProfile from "./pages/UserProfile";
import MembershipPlans from "./pages/MembershipPlans";
import "./App.css";

function App() {
  useEffect(() => {
    // Initialize AOS (Animate On Scroll)
    AOS.init({
      duration: 1000,
      once: true,
      offset: 100,
      easing: "ease-in-out",
    });
  }, []);

  return (
    <Router>
      <div className="App">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/classes" element={<Classes />} />
            <Route path="/my-bookings" element={<MyBookings />} />
            <Route path="/profile" element={<UserProfile />} />
            <Route path="/membership" element={<MembershipPlans />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
