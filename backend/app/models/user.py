"""
User Model Module

This module defines the User database model using SQLAlchemy ORM.

Why this file exists:
- Defines the structure of the users table in the database
- Maps Python class to database table
- Provides type-safe database operations
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database.config import Base


class User(Base):
    """
    User model representing the users table.
    
    Attributes:
        id: Primary key, auto-incremented
        username: Unique username for login
        email: Unique email address
        hashed_password: Bcrypt hashed password (never store plain text!)
        created_at: Timestamp when user was created
    """
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
