"""
User Schemas Module

This module defines Pydantic schemas for user-related data validation.
Pydantic schemas validate incoming request data and serialize outgoing response data.

Why this file exists:
- Validates user input (registration, login)
- Serializes database models to JSON responses
- Provides type safety and automatic validation
- Separates validation logic from business logic
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserRegister(BaseModel):
    """
    Schema for user registration request.
    
    Validates incoming registration data:
    - username: 3-50 characters
    - email: Must be valid email format
    - password: Minimum 6 characters
    """
    username: str = Field(..., min_length=3, max_length=50, description="Username for login")
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=6, description="Password (minimum 6 characters)")


class UserLogin(BaseModel):
    """
    Schema for user login request.
    
    User can login with either username or email.
    """
    username_or_email: str = Field(..., description="Username or email")
    password: str = Field(..., description="Password")


class UserResponse(BaseModel):
    """
    Schema for user response (safe data only).
    
    Excludes sensitive data like password.
    Used when returning user information to the client.
    """
    id: int
    username: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True  # Allows creating from ORM models


class Token(BaseModel):
    """
    Schema for JWT token response.
    
    Returns the access token and token type.
    """
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """
    Schema for token payload data.
    
    Contains the user ID extracted from the JWT token.
    """
    user_id: int | None = None
