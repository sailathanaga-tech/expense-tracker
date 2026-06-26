"""
Environment Variables Configuration Module

This module loads and manages environment variables from .env file.

Why this file exists:
- Keeps sensitive information (passwords, secret keys) out of code
- Makes it easy to configure different environments (dev, prod)
- Provides type-safe access to environment variables
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Settings class that loads environment variables.
    
    Pydantic automatically reads from .env file and environment variables.
    It also validates the types of the values.
    """
    
    # Database configuration
    DATABASE_URL: str
    
    # JWT configuration
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
# This will be imported by other modules to access settings
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get the global settings instance.
    
    This function implements a singleton pattern to ensure
    settings are loaded only once.
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
