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
import AdminDashboard from "./pages/admin/AdminDashboard";
import AdminMembers from "./pages/admin/AdminMembers";
import AdminClasses from "./pages/admin/AdminClasses";
import AdminBookings from "./pages/admin/AdminBookings";
import AdminAttendance from "./pages/admin/AdminAttendance";
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
            
            {/* Admin Routes */}
            <Route path="/admin" element={<AdminDashboard />} />
            <Route path="/admin/dashboard" element={<AdminDashboard />} />
            <Route path="/admin/members" element={<AdminMembers />} />
            <Route path="/admin/classes" element={<AdminClasses />} />
            <Route path="/admin/bookings" element={<AdminBookings />} />
            <Route path="/admin/attendance" element={<AdminAttendance />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
