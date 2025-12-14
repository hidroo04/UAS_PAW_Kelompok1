import React from "react";
import "./ClassCard.css";

const ClassCard = ({ classData, onBook, onView, showActions = true }) => {
  const {
    id,
    name,
    description,
    schedule,
    capacity,
    booked_count,
    available_slots,
    trainer,
  } = classData;

  const scheduleDate = new Date(schedule);
  const isFullyBooked = available_slots === 0;

  return (
    <div className="class-card">
      <div className="class-card-header">
        <h3>{name}</h3>
        <span className={`capacity-badge ${isFullyBooked ? "full" : ""}`}>
          {available_slots}/{capacity} slots
        </span>
      </div>

      <p className="class-description">{description}</p>

      <div className="class-info">
        <div className="info-item">
          <span className="info-label">📅 Schedule:</span>
          <span>
            {scheduleDate.toLocaleDateString()}{" "}
            {scheduleDate.toLocaleTimeString()}
          </span>
        </div>

        <div className="info-item">
          <span className="info-label">👨‍🏫 Trainer:</span>
          <span>{trainer?.name || "N/A"}</span>
        </div>

        <div className="info-item">
          <span className="info-label">👥 Booked:</span>
          <span>
            {booked_count} / {capacity}
          </span>
        </div>
      </div>

      {showActions && (
        <div className="class-actions">
          {onView && (
            <button onClick={() => onView(id)} className="btn-view">
              View Details
            </button>
          )}
          {onBook && (
            <button
              onClick={() => onBook(id)}
              className="btn-book"
              disabled={isFullyBooked}
            >
              {isFullyBooked ? "Fully Booked" : "Book Class"}
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default ClassCard;
