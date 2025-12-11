from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from . import Base


class Member(Base):
    __tablename__ = 'members'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    membership_plan = Column(String(50), nullable=False)  # Basic, Premium, VIP
    expiry_date = Column(Date, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="member")
    bookings = relationship("Booking", back_populates="member", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Member(id={self.id}, user_id={self.user_id}, plan='{self.membership_plan}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'membership_plan': self.membership_plan,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'user': self.user.to_dict() if self.user else None
        }
    
    def is_active(self):
        """Check if membership is still active"""
        return self.expiry_date >= datetime.now().date()
