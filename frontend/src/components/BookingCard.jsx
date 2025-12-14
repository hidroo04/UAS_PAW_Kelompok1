import React from "react";
import "./BookingCard.css";

const BookingCard = ({ booking, onCancel, showCancel = true }) => {
  const { id, class: gymClass, booking_date, attendance } = booking;

  const bookingDate = new Date(booking_date);
  const classSchedule = new Date(gymClass?.schedule);

  return (
    <div className="booking-card">
      <div className="booking-header">
        <h3>{gymClass?.name}</h3>
        {attendance && (
          <span
            className={`attendance-badge ${
              attendance.attended ? "attended" : "absent"
            }`}
          >
            {attendance.attended ? "✓ Attended" : "✗ Absent"}
          </span>
        )}
      </div>

      <div className="booking-info">
        <div className="info-row">
          <span className="info-label">📅 Class Date:</span>
          <span>
            {classSchedule.toLocaleDateString()}{" "}
            {classSchedule.toLocaleTimeString()}
          </span>
        </div>

        <div className="info-row">
          <span className="info-label">🎫 Booked On:</span>
          <span>{bookingDate.toLocaleDateString()}</span>
        </div>

        {gymClass?.trainer && (
          <div className="info-row">
            <span className="info-label">👨‍🏫 Trainer:</span>
            <span>{gymClass.trainer.name}</span>
          </div>
        )}
      </div>

      {showCancel && (
        <button onClick={() => onCancel(id)} className="btn-cancel">
          Cancel Booking
        </button>
      )}
    </div>
  );
};

export default BookingCard;
