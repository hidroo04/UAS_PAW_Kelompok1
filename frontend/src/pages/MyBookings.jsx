import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import BookingCard from "../components/BookingCard";
import Loading from "../components/Loading";
import apiClient from "../services/api";
import "./MyBookings.css";

const MyBookings = () => {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
      return;
    }
    fetchBookings();
  }, [navigate]);

  const fetchBookings = async () => {
    try {
      const response = await apiClient.get("/bookings/my");
      console.log("My Bookings Response:", response.data);
      if (response.data.status === "success") {
        setBookings(response.data.data);
      }
    } catch (err) {
      console.error("Error fetching bookings:", err);
      console.error("Error response:", err.response);
      setError("Failed to load bookings");
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = async (bookingId) => {
    if (!window.confirm("Are you sure you want to cancel this booking?")) {
      return;
    }

    try {
      const response = await apiClient.delete(`/bookings/${bookingId}`);
      if (response.data.status === "success") {
        // Hapus booking dari list
        setBookings(prevBookings => prevBookings.filter(b => b.id !== bookingId));
        alert("Booking cancelled successfully");
      }
    } catch (err) {
      alert("Failed to cancel booking");
    }
  };

  if (loading) return <Loading message="Loading your bookings..." />;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="my-bookings-page">
      <div className="page-header">
        <h1>My Bookings</h1>
        <p>View and manage your class bookings</p>
      </div>

      <div className="bookings-list">
        {bookings.length > 0 ? (
          bookings.map((booking) => (
            <BookingCard
              key={booking.id}
              booking={booking}
              onCancel={handleCancel}
            />
          ))
        ) : (
          <p className="no-data">You haven't booked any classes yet</p>
        )}
      </div>
    </div>
  );
};

export default MyBookings;
