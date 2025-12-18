"""
Payment Model - Untuk tracking pembayaran membership
"""
from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from . import Base


class PaymentStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    EXPIRED = "expired"
    REFUNDED = "refunded"


class PaymentMethod(enum.Enum):
    BANK_TRANSFER = "bank_transfer"
    CREDIT_CARD = "credit_card"
    E_WALLET = "e_wallet"
    QRIS = "qris"


class Payment(Base):
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey('members.id', ondelete='CASCADE'), nullable=False)
    
    # Payment details
    order_id = Column(String(100), unique=True, nullable=False)  # Unique order ID
    amount = Column(Numeric(12, 2), nullable=False)
    payment_method = Column(String(50), nullable=True)  # Using String for database compatibility
    status = Column(String(20), default='pending')  # Using String for database compatibility
    
    # Membership info
    membership_plan = Column(String(50), nullable=False)
    duration_days = Column(Integer, default=30)
    
    # Transaction details
    transaction_id = Column(String(100), nullable=True)  # From payment gateway
    payment_url = Column(String(500), nullable=True)  # Redirect URL
    va_number = Column(String(50), nullable=True)  # Virtual Account number
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)
    expired_at = Column(DateTime, nullable=True)
    
    # Relationships
    member = relationship("Member", back_populates="payments")
    
    def __repr__(self):
        return f"<Payment(id={self.id}, order_id='{self.order_id}', status='{self.status}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'member_id': self.member_id,
            'order_id': self.order_id,
            'amount': float(self.amount) if self.amount else 0,
            'payment_method': self.payment_method,
            'status': self.status,
            'membership_plan': self.membership_plan,
            'duration_days': self.duration_days,
            'transaction_id': self.transaction_id,
            'payment_url': self.payment_url,
            'va_number': self.va_number,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'paid_at': self.paid_at.isoformat() if self.paid_at else None,
            'expired_at': self.expired_at.isoformat() if self.expired_at else None
        }
