"""
Configuration utilities
Loads environment variables and provides app configuration
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration"""
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost/gym_booking_db')
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'change-this-secret-key-in-production')
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
    JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', '24'))
    
    # Application
    APP_ENV = os.getenv('APP_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Server
    HOST = os.getenv('HOST', 'localhost')
    PORT = int(os.getenv('PORT', '6543'))
    
    @classmethod
    def is_production(cls):
        """Check if running in production mode"""
        return cls.APP_ENV == 'production'
    
    @classmethod
    def is_development(cls):
        """Check if running in development mode"""
        return cls.APP_ENV == 'development'


# Export singleton instance
config = Config()
