from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from . import Base


class Class(Base):
    __tablename__ = 'classes'
    
    id = Column(Integer, primary_key=True)
    trainer_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    schedule = Column(DateTime, nullable=False)
    capacity = Column(Integer, nullable=False, default=20)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    trainer = relationship("User", back_populates="trainer_classes", foreign_keys=[trainer_id])
    bookings = relationship("Booking", back_populates="gym_class", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Class(id={self.id}, name='{self.name}', schedule='{self.schedule}')>"
    
    def to_dict(self, include_bookings=False):
        data = {
            'id': self.id,
            'trainer_id': self.trainer_id,
            'name': self.name,
            'description': self.description,
            'schedule': self.schedule.isoformat() if self.schedule else None,
            'capacity': self.capacity,
            'booked_count': len(self.bookings) if self.bookings else 0,
            'available_slots': self.capacity - (len(self.bookings) if self.bookings else 0),
            'trainer': self.trainer.to_dict() if self.trainer else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_bookings:
            data['bookings'] = [b.to_dict(include_member=True) for b in self.bookings]
        return data
    
    def is_full(self):
        """Check if class is at full capacity"""
        return len(self.bookings) >= self.capacity
