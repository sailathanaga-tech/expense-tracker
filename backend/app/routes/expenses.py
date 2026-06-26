"""
Expense Routes Module

This module handles expense CRUD endpoints.

Why this file exists:
- Separates expense management logic from other routes
- Organizes related endpoints together
- Makes the codebase maintainable
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database.config import get_db
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse, ExpenseListResponse
from app.models.expense import Expense
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense_data: ExpenseCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new expense for the authenticated user.
    
    Process:
    1. Validate expense data with Pydantic schema
    2. Create expense with current user's ID
    3. Save to database
    4. Return created expense
    
    Args:
        expense_data: Expense creation data (title, amount, category, date, notes)
        db: Database session
        current_user: Authenticated user (from JWT token)
    
    Returns:
        Created expense data
    
    Raises:
        HTTPException: If validation fails
    """
    # Create new expense with current user's ID
    new_expense = Expense(
        title=expense_data.title,
        amount=expense_data.amount,
        category=expense_data.category,
        date=expense_data.date,
        notes=expense_data.notes,
        user_id=current_user.id
    )
    
    # Save to database
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    
    return new_expense


@router.get("/", response_model=ExpenseListResponse)
def get_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    category: Optional[str] = Query(None, description="Filter by category"),
    skip: int = Query(0, ge=0, description="Number of expenses to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of expenses to return")
):
    """
    Get all expenses for the authenticated user.
    
    Supports optional filtering by category and pagination.
    
    Process:
    1. Query expenses filtered by current user's ID
    2. Apply category filter if provided
    3. Apply pagination (skip and limit)
    4. Return expenses and total count
    
    Args:
        db: Database session
        current_user: Authenticated user (from JWT token)
        category: Optional category filter
        skip: Number of expenses to skip (for pagination)
        limit: Maximum number of expenses to return
    
    Returns:
        List of expenses and total count
    """
    # Build query - only get expenses for current user
    query = db.query(Expense).filter(Expense.user_id == current_user.id)
    
    # Apply category filter if provided
    if category:
        query = query.filter(Expense.category == category)
    
    # Order by date (newest first)
    query = query.order_by(Expense.date.desc())
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    expenses = query.offset(skip).limit(limit).all()
    
    return {"expenses": expenses, "total": total}


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a single expense by ID.
    
    Process:
    1. Find expense by ID
    2. Verify expense belongs to current user
    3. Return expense data
    
    Args:
        expense_id: ID of the expense to retrieve
        db: Database session
        current_user: Authenticated user (from JWT token)
    
    Returns:
        Expense data
    
    Raises:
        HTTPException: If expense not found or doesn't belong to user
    """
    # Find expense by ID
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    
    # Check if expense exists
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    # Verify expense belongs to current user
    if expense.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this expense"
        )
    
    return expense


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing expense.
    
    Only updates fields that are provided in the request body.
    
    Process:
    1. Find expense by ID
    2. Verify expense belongs to current user
    3. Update provided fields
    4. Save changes to database
    5. Return updated expense
    
    Args:
        expense_id: ID of the expense to update
        expense_data: Expense update data (all fields optional)
        db: Database session
        current_user: Authenticated user (from JWT token)
    
    Returns:
        Updated expense data
    
    Raises:
        HTTPException: If expense not found or doesn't belong to user
    """
    # Find expense by ID
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    
    # Check if expense exists
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    # Verify expense belongs to current user
    if expense.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to modify this expense"
        )
    
    # Update only provided fields
    update_data = expense_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(expense, field, value)
    
    # Save changes
    db.commit()
    db.refresh(expense)
    
    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete an expense.
    
    Process:
    1. Find expense by ID
    2. Verify expense belongs to current user
    3. Delete expense from database
    
    Args:
        expense_id: ID of the expense to delete
        db: Database session
        current_user: Authenticated user (from JWT token)
    
    Returns:
        204 No Content on success
    
    Raises:
        HTTPException: If expense not found or doesn't belong to user
    """
    # Find expense by ID
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    
    # Check if expense exists
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    # Verify expense belongs to current user
    if expense.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this expense"
        )
    
    # Delete expense
    db.delete(expense)
    db.commit()
    
    return None
