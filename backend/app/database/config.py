"""
Database Configuration Module

This module handles the database connection and session management.
It uses SQLAlchemy to create a database engine and session factory.

Why this file exists:
- Centralizes database configuration
- Manages database connections efficiently
- Provides a consistent way to access the database across the application
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.utils.env import get_settings

# Get database settings from environment variables
settings = get_settings()

# Create database engine
# The engine manages the connection pool to MySQL
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using them
    echo=False  # Set to True to see SQL queries in console (useful for debugging)
)

# Create SessionLocal class for database sessions
# Each session represents a transaction with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for database models
# All model classes will inherit from this Base
Base = declarative_base()


# Dependency function to get database session
# This will be used in FastAPI endpoints to get a database session
def get_db():
    """
    Dependency function that yields a database session.
    
    Usage in FastAPI:
    @app.get("/expenses")
    def get_expenses(db: Session = Depends(get_db)):
        ...
    
    The 'yield' statement ensures the session is closed after the request is complete
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
