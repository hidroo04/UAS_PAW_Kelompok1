"""
Enhanced GymClass model with additional fields
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from . import Base


class ClassType(enum.Enum):
    """Enum for class types"""
    YOGA = "Yoga"
    HIIT = "HIIT"
    STRENGTH = "Strength Training"
    CARDIO = "Cardio"
    PILATES = "Pilates"
    SPINNING = "Spinning"
    CROSSFIT = "CrossFit"
    ZUMBA = "Zumba"
    BOXING = "Boxing"
    GENERAL = "General"


class Difficulty(enum.Enum):
    """Enum for difficulty levels"""
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    ALL_LEVELS = "All Levels"


class GymClass(Base):
    __tablename__ = 'classes'
    
    id = Column(Integer, primary_key=True)
    trainer_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    schedule = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False, default=60)  # in minutes
    capacity = Column(Integer, nullable=False, default=20)
    class_type = Column(SQLEnum(ClassType), default=ClassType.GENERAL)
    difficulty = Column(SQLEnum(Difficulty), default=Difficulty.ALL_LEVELS)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    trainer = relationship("User", back_populates="trainer_classes", foreign_keys=[trainer_id])
    bookings = relationship("Booking", back_populates="gym_class", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="gym_class", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<GymClass(id={self.id}, name='{self.name}', schedule='{self.schedule}')>"
    
    def to_dict(self, include_bookings=False, include_reviews=False):
        """Convert to dictionary"""
        from sqlalchemy import func
        
        data = {
            'id': self.id,
            'trainer_id': self.trainer_id,
            'name': self.name,
            'description': self.description,
            'schedule': self.schedule.isoformat() if self.schedule else None,
            'duration': self.duration,
            'capacity': self.capacity,
            'class_type': self.class_type.value if self.class_type else 'General',
            'difficulty': self.difficulty.value if self.difficulty else 'All Levels',
            'booked_count': len([b for b in self.bookings if b.status == 'CONFIRMED']) if self.bookings else 0,
            'available_slots': self.capacity - len([b for b in self.bookings if b.status == 'CONFIRMED']) if self.bookings else self.capacity,
            'trainer': {
                'id': self.trainer.id,
                'name': self.trainer.name,
                'email': self.trainer.email
            } if self.trainer else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_bookings:
            data['bookings'] = [b.to_dict(include_member=True) for b in self.bookings]
        
        if include_reviews and self.reviews:
            data['reviews'] = [r.to_dict() for r in self.reviews]
            data['average_rating'] = sum(r.rating for r in self.reviews) / len(self.reviews) if self.reviews else 0
            data['total_reviews'] = len(self.reviews)
        
        return data
    
    def is_full(self):
        """Check if class is at full capacity"""
        confirmed_bookings = len([b for b in self.bookings if b.status == 'CONFIRMED'])
        return confirmed_bookings >= self.capacity
    
    def get_available_slots(self):
        """Get number of available slots"""
        confirmed_bookings = len([b for b in self.bookings if b.status == 'CONFIRMED'])
        return self.capacity - confirmed_bookings
    
    def get_average_rating(self):
        """Get average rating from reviews"""
        if not self.reviews:
            return 0
        return sum(r.rating for r in self.reviews) / len(self.reviews)
