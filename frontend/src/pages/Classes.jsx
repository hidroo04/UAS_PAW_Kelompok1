import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { FaSearch, FaFilter, FaStar } from "react-icons/fa";
import ClassCard from "../components/ClassCard";
import Loading from "../components/Loading";
import apiClient from "../services/api";
import "./Classes.css";

const Classes = () => {
  const navigate = useNavigate();
  const [classes, setClasses] = useState([]);
  const [filteredClasses, setFilteredClasses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [selectedClass, setSelectedClass] = useState(null);
  
  // Filter states
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedType, setSelectedType] = useState("all");
  const [selectedDifficulty, setSelectedDifficulty] = useState("all");
  const [selectedDate, setSelectedDate] = useState("");

  useEffect(() => {
    fetchClasses();
  }, []);

  useEffect(() => {
    filterClasses();
  }, [classes, searchTerm, selectedType, selectedDifficulty, selectedDate]);

  const fetchClasses = async () => {
    try {
      const response = await apiClient.get("/classes");
      if (response.data.status === "success") {
        setClasses(response.data.data);
        setFilteredClasses(response.data.data);
      }
    } catch (err) {
      setError("Failed to load classes");
    } finally {
      setLoading(false);
    }
  };

  const filterClasses = () => {
    let filtered = [...classes];

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(
        (cls) =>
          cls.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          cls.description.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Type filter
    if (selectedType !== "all") {
      filtered = filtered.filter((cls) => cls.class_type === selectedType);
    }

    // Difficulty filter
    if (selectedDifficulty !== "all") {
      filtered = filtered.filter((cls) => cls.difficulty === selectedDifficulty);
    }

    // Date filter
    if (selectedDate) {
      filtered = filtered.filter((cls) => {
        const classDate = new Date(cls.schedule).toISOString().split("T")[0];
        return classDate === selectedDate;
      });
    }

    setFilteredClasses(filtered);
  };

  const handleBook = async (classId) => {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("Please login to book a class");
      return;
    }

    // Find the class details
    const classToBook = classes.find(cls => cls.id === classId);
    setSelectedClass(classToBook);
    setShowModal(true);
  };

  const confirmBooking = async () => {
    try {
      const response = await apiClient.post("/bookings", { class_id: selectedClass.id });
      if (response.data.status === "success") {
        setShowModal(false);
        // Show success message
        alert(`Booking berhasil! Kelas "${selectedClass.name}" telah ditambahkan ke My Bookings.`);
        // Redirect to My Bookings page
        navigate('/my-bookings');
      }
    } catch (err) {
      setShowModal(false);
      const errorMessage = err.response?.data?.message || "Booking failed";
      
      // Check if redirect to membership page
      if (err.response?.data?.redirect === '/membership') {
        if (window.confirm(`${errorMessage}\n\nKlik OK untuk memilih membership plan.`)) {
          navigate('/membership');
        }
      } else {
        alert(errorMessage);
      }
    }
  };

  const cancelBooking = () => {
    setShowModal(false);
    setSelectedClass(null);
  };

  const clearFilters = () => {
    setSearchTerm("");
    setSelectedType("all");
    setSelectedDifficulty("all");
    setSelectedDate("");
  };

  if (loading) return <Loading message="Loading classes..." />;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="classes-page">
      <div className="page-header" data-aos="fade-down">
        <h1>Available Classes</h1>
        <p>Browse and book your favorite gym classes</p>
      </div>

      {/* Search and Filter Section */}
      <div className="filter-section" data-aos="fade-up">
        <div className="container">
          <div className="search-box">
            <FaSearch className="search-icon" />
            <input
              type="text"
              placeholder="Search classes..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-input"
            />
          </div>

          <div className="filters">
            <div className="filter-group">
              <label>
                <FaFilter /> Class Type
              </label>
              <select
                value={selectedType}
                onChange={(e) => setSelectedType(e.target.value)}
              >
                <option value="all">All Types</option>
                <option value="Yoga">Yoga</option>
                <option value="HIIT">HIIT</option>
                <option value="Strength Training">Strength Training</option>
                <option value="Cardio">Cardio</option>
                <option value="Pilates">Pilates</option>
                <option value="Spinning">Spinning</option>
              </select>
            </div>

            <div className="filter-group">
              <label>
                <FaStar /> Difficulty
              </label>
              <select
                value={selectedDifficulty}
                onChange={(e) => setSelectedDifficulty(e.target.value)}
              >
                <option value="all">All Levels</option>
                <option value="Beginner">Beginner</option>
                <option value="Intermediate">Intermediate</option>
                <option value="Advanced">Advanced</option>
              </select>
            </div>

            <div className="filter-group">
              <label>Date</label>
              <input
                type="date"
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
              />
            </div>

            <button onClick={clearFilters} className="btn-clear-filters">
              Clear Filters
            </button>
          </div>
        </div>
      </div>

      {/* Classes Grid */}
      <div className="container">
        <div className="classes-stats" data-aos="fade-up">
          <p>
            Showing <strong>{filteredClasses.length}</strong> of{" "}
            <strong>{classes.length}</strong> classes
          </p>
        </div>

        <div className="classes-grid">
          {filteredClasses.length > 0 ? (
            filteredClasses.map((classData, index) => (
              <div key={classData.id} data-aos="fade-up" data-aos-delay={index * 100}>
                <ClassCard classData={classData} onBook={handleBook} />
              </div>
            ))
          ) : (
            <div className="no-data">
              <p>No classes match your criteria</p>
              <button onClick={clearFilters} className="btn-primary">
                Clear Filters
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Booking Confirmation Modal */}
      {showModal && selectedClass && (
        <div className="modal-overlay" onClick={cancelBooking}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Konfirmasi Booking</h2>
              <button className="modal-close" onClick={cancelBooking}>&times;</button>
            </div>
            <div className="modal-body">
              <p className="modal-question">
                Apakah Anda yakin ingin booking kelas ini?
              </p>
              <div className="class-info-modal">
                <h3>{selectedClass.name}</h3>
                <p><strong>Jadwal:</strong> {new Date(selectedClass.schedule).toLocaleString('id-ID', {
                  weekday: 'long',
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit'
                })}</p>
                <p><strong>Trainer:</strong> {selectedClass.trainer?.name || 'N/A'}</p>
                <p><strong>Kapasitas:</strong> {selectedClass.available_slots || selectedClass.capacity} slot tersedia</p>
              </div>
            </div>
            <div className="modal-footer">
              <button className="btn-cancel" onClick={cancelBooking}>
                Batal
              </button>
              <button className="btn-confirm" onClick={confirmBooking}>
                Ya, Booking Sekarang
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Classes;
