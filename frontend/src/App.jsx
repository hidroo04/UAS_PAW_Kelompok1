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
import Payment from "./pages/Payment";
import AdminDashboard from "./pages/admin/AdminDashboard";
import AdminMembers from "./pages/admin/AdminMembers";
import AdminClasses from "./pages/admin/AdminClasses";
import AdminBookings from "./pages/admin/AdminBookings";
import AdminAttendance from "./pages/admin/AdminAttendance";
import AdminPayments from "./pages/admin/AdminPayments";
import AdminTrainers from "./pages/admin/AdminTrainers";
import MyClasses from "./pages/trainer/MyClasses";
import ClassDetail from "./pages/trainer/ClassDetail";
import ManageClasses from "./pages/trainer/ManageClasses";
import Calendar from "./pages/trainer/Calendar";
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
            <Route path="/payment" element={<Payment />} />
            <Route path="/payment/:orderId" element={<Payment />} />
            
            {/* Admin Routes */}
            <Route path="/admin" element={<AdminDashboard />} />
            <Route path="/admin/dashboard" element={<AdminDashboard />} />
            <Route path="/admin/members" element={<AdminMembers />} />
            <Route path="/admin/classes" element={<AdminClasses />} />
            <Route path="/admin/bookings" element={<AdminBookings />} />
            <Route path="/admin/attendance" element={<AdminAttendance />} />
            <Route path="/admin/payments" element={<AdminPayments />} />
            <Route path="/admin/trainers" element={<AdminTrainers />} />
            
            {/* Trainer Routes */}
            <Route path="/trainer/my-classes" element={<MyClasses />} />
            <Route path="/trainer/my-classes/:id" element={<ClassDetail />} />
            <Route path="/trainer/manage-classes" element={<ManageClasses />} />
            <Route path="/trainer/calendar" element={<Calendar />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
