"""
Authentication Dependencies Module

This module provides FastAPI dependencies for authentication.
These dependencies are used to protect routes that require authentication.

Why this file exists:
- Provides reusable authentication logic
- Extracts and validates JWT tokens
- Retrieves current user from database
- Can be used as a dependency in any protected route
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database.config import get_db
from app.models.user import User
from app.auth.security import decode_access_token

# HTTPBearer security scheme for extracting Bearer token from Authorization header
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency function to get the current authenticated user.
    
    Usage in FastAPI:
    @app.get("/protected-route")
    def protected_route(current_user: User = Depends(get_current_user)):
        return {"user_id": current_user.id}
    
    Args:
        credentials: The HTTPAuthorizationCredentials containing the Bearer token
        db: Database session
    
    Returns:
        The authenticated User object
    
    Raises:
        HTTPException: If token is invalid or user not found
    """
    # Extract token from credentials
    token = credentials.credentials
    
    # Decode and verify token
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract user_id from token payload
    user_id: int = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Retrieve user from database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user
