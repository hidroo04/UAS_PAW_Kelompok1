from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from . import Base


class UserRole(enum.Enum):
    ADMIN = "admin"
    TRAINER = "trainer"
    MEMBER = "member"


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    address = Column(String, nullable=True)
    avatar_url = Column(String(255), nullable=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.MEMBER)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    member = relationship("Member", back_populates="user", uselist=False, cascade="all, delete-orphan")
    trainer_classes = relationship("GymClass", back_populates="trainer", foreign_keys="GymClass.trainer_id")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}', role='{self.role.value}')>"
    
    def to_dict(self):
        user_dict = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'avatar_url': self.avatar_url,
            'role': self.role.value,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        # Include membership info if user is a member
        if self.member:
            user_dict['membership_plan'] = self.member.membership_plan
            user_dict['membership_expiry'] = self.member.expiry_date.isoformat() if self.member.expiry_date else None
            user_dict['membership_status'] = 'Active' if self.member.is_active() else 'Expired'
        
        return user_dict
