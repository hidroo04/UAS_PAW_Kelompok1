import React, { useState, useEffect } from "react";
import ClassCard from "../components/ClassCard";
import Loading from "../components/Loading";
import apiClient from "../services/api";
import "./Classes.css";

const Classes = () => {
  const [classes, setClasses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchClasses();
  }, []);

  const fetchClasses = async () => {
    try {
      const response = await apiClient.get("/classes");
      if (response.data.status === "success") {
        setClasses(response.data.data);
      }
    } catch (err) {
      setError("Failed to load classes");
    } finally {
      setLoading(false);
    }
  };

  const handleBook = async (classId) => {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("Please login to book a class");
      return;
    }

    try {
      const response = await apiClient.post("/bookings", { class_id: classId });
      if (response.data.status === "success") {
        alert("Class booked successfully!");
        fetchClasses(); // Refresh
      }
    } catch (err) {
      alert(err.response?.data?.message || "Booking failed");
    }
  };

  if (loading) return <Loading message="Loading classes..." />;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="classes-page">
      <div className="page-header">
        <h1>Available Classes</h1>
        <p>Browse and book your favorite gym classes</p>
      </div>

      <div className="classes-grid">
        {classes.length > 0 ? (
          classes.map((classData) => (
            <ClassCard
              key={classData.id}
              classData={classData}
              onBook={handleBook}
            />
          ))
        ) : (
          <p className="no-data">No classes available at the moment</p>
        )}
      </div>
    </div>
  );
};

export default Classes;
