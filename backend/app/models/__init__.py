# Database models package
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

# Base declarative
Base = declarative_base()

# Import all models
from .user import User, UserRole
from .member import Member
from .gym_class_enhanced import GymClass, ClassType, Difficulty
from .booking import Booking
from .attendance import Attendance
from .review import Review

# Export all models
__all__ = [
    'Base',
    'User',
    'UserRole',
    'Member',
    'GymClass',
    'ClassType',
    'Difficulty',
    'Booking',
    'Attendance',
    'Review',
    'get_engine',
    'get_session_factory',
    'init_db'
]


def get_engine(db_url, echo=False):
    """Create database engine"""
    return create_engine(db_url, echo=echo)


def get_session_factory(engine):
    """Create session factory"""
    session_factory = sessionmaker(bind=engine)
    return scoped_session(session_factory)


def init_db(engine):
    """Initialize database - create all tables"""
    Base.metadata.create_all(engine)
