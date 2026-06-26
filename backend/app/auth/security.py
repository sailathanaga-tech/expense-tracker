"""
Security Module

This module handles password hashing and JWT token operations.

Why this file exists:
- Centralizes security-related functions
- Provides consistent password hashing and verification
- Handles JWT token creation and verification
- Keeps security logic in one place for easy auditing
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.utils.env import get_settings

# Get settings
settings = get_settings()

# Password hashing context using bcrypt
# bcrypt is a slow hashing algorithm designed for passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    
    Args:
        plain_password: The password provided by the user
        hashed_password: The hashed password stored in the database
    
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a plain password using bcrypt.
    
    Args:
        password: The plain password to hash
    
    Returns:
        The hashed password (safe to store in database)
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: The payload data to encode (typically contains user_id)
        expires_delta: Optional custom expiration time
    
    Returns:
        Encoded JWT token as string
    
    The token contains:
    - user_id: The user's ID
    - exp: Expiration timestamp
    - iat: Issued at timestamp
    """
    to_encode = data.copy()
    
    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Encode the token
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and verify a JWT access token.
    
    Args:
        token: The JWT token to decode
    
    Returns:
        The decoded token payload if valid, None if invalid
    
    Raises:
        JWTError: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
