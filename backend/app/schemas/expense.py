"""
Expense Schemas Module

This module defines Pydantic schemas for expense-related data validation.

Why this file exists:
- Validates expense input (create, update)
- Serializes database models to JSON responses
- Enforces predefined categories
- Separates validation logic from business logic
"""

from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List


# Predefined categories
VALID_CATEGORIES = ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"]


class ExpenseCreate(BaseModel):
    """
    Schema for creating a new expense.
    
    Validates incoming expense data:
    - title: 1-200 characters
    - amount: Must be positive
    - category: Must be one of the predefined categories
    - date: Required datetime
    - notes: Optional, max 500 characters
    """
    title: str = Field(..., min_length=1, max_length=200, description="Expense title")
    amount: float = Field(..., gt=0, description="Expense amount (must be positive)")
    category: str = Field(..., description="Expense category")
    date: datetime = Field(..., description="Date of expense")
    notes: Optional[str] = Field(None, max_length=500, description="Additional notes")
    
    @validator('category')
    def validate_category(cls, v):
        """Validate that category is one of the predefined categories."""
        if v not in VALID_CATEGORIES:
            raise ValueError(
                f"Invalid category. Must be one of: {', '.join(VALID_CATEGORIES)}"
            )
        return v


class ExpenseUpdate(BaseModel):
    """
    Schema for updating an existing expense.
    
    All fields are optional - only provided fields will be updated.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None)
    date: Optional[datetime] = None
    notes: Optional[str] = Field(None, max_length=500)
    
    @validator('category')
    def validate_category(cls, v):
        """Validate that category is one of the predefined categories."""
        if v is not None and v not in VALID_CATEGORIES:
            raise ValueError(
                f"Invalid category. Must be one of: {', '.join(VALID_CATEGORIES)}"
            )
        return v


class ExpenseResponse(BaseModel):
    """
    Schema for expense response.
    
    Returns expense data including the user who created it.
    """
    id: int
    title: str
    amount: float
    category: str
    date: datetime
    notes: Optional[str]
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ExpenseListResponse(BaseModel):
    """
    Schema for list of expenses response.
    """
    expenses: List[ExpenseResponse]
    total: int
