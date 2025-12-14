from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from . import Base


class Booking(Base):
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey('members.id', ondelete='CASCADE'), nullable=False)
    class_id = Column(Integer, ForeignKey('classes.id', ondelete='CASCADE'), nullable=False)
    booking_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    member = relationship("Member", back_populates="bookings")
    gym_class = relationship("Class", back_populates="bookings")
    attendance = relationship("Attendance", back_populates="booking", uselist=False, cascade="all, delete-orphan")
    
    # Ensure one member can only book a class once
    __table_args__ = (
        UniqueConstraint('member_id', 'class_id', name='unique_member_class_booking'),
    )

    def __repr__(self):
        return f"<Booking(id={self.id}, member_id={self.member_id}, class_id={self.class_id})>"
    
    def to_dict(self, include_member=False, include_class=False):
        data = {
            'id': self.id,
            'member_id': self.member_id,
            'class_id': self.class_id,
            'booking_date': self.booking_date.isoformat() if self.booking_date else None
        }
        if include_member and self.member:
            data['member'] = self.member.to_dict()
        if include_class and self.gym_class:
            data['class'] = self.gym_class.to_dict()
        if self.attendance:
            data['attendance'] = self.attendance.to_dict()
        return data
