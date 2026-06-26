"""
Expense Model Module

This module defines the Expense database model using SQLAlchemy ORM.

Why this file exists:
- Defines the structure of the expenses table in the database
- Maps Python class to database table
- Establishes relationship with User model
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.config import Base


class Expense(Base):
    """
    Expense model representing the expenses table.
    
    Attributes:
        id: Primary key, auto-incremented
        title: Short description of the expense
        amount: Expense amount (decimal value)
        category: Category of expense (Food, Travel, Shopping, etc.)
        date: Date when the expense occurred
        notes: Additional notes about the expense
        user_id: Foreign key to users table
        created_at: Timestamp when expense was created
        user: Relationship to User model
    """
    
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    notes = Column(String(500), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship to User model
    # This allows accessing user data from expense objects
    user = relationship("User", backref="expenses")
