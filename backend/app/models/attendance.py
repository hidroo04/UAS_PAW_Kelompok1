from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from . import Base


class Attendance(Base):
    __tablename__ = 'attendance'
    
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('bookings.id', ondelete='CASCADE'), unique=True, nullable=False)
    attended = Column(Boolean, default=False, nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    booking = relationship("Booking", back_populates="attendance")

    def __repr__(self):
        return f"<Attendance(id={self.id}, booking_id={self.booking_id}, attended={self.attended})>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'attended': self.attended,
            'date': self.date.isoformat() if self.date else None
        }
