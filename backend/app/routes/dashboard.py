"""
Dashboard Routes Module

This module handles dashboard statistics endpoints.

Why this file exists:
- Separates dashboard logic from other routes
- Organizes related endpoints together
- Makes the codebase maintainable
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from app.database.config import get_db
from app.schemas.dashboard import DashboardSummary, CategorySummary, MonthlyExpense
from app.models.expense import Expense
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get dashboard summary for the authenticated user.
    
    Provides:
    - Total expenses (sum of all amounts)
    - Total expense count
    - Category-wise summary (grouped by category with totals and percentages)
    - Monthly expenses (grouped by month)
    - Current month totals
    
    Process:
    1. Calculate total expenses and count
    2. Group expenses by category with totals
    3. Calculate percentage for each category
    4. Group expenses by month
    5. Calculate current month totals
    
    Args:
        db: Database session
        current_user: Authenticated user (from JWT token)
    
    Returns:
        Complete dashboard summary
    """
    # Get current date for current month calculations
    current_date = datetime.utcnow()
    current_month = current_date.month
    current_year = current_date.year
    
    # Calculate total expenses and count for the user
    total_result = db.query(
        func.sum(Expense.amount).label('total_amount'),
        func.count(Expense.id).label('total_count')
    ).filter(Expense.user_id == current_user.id).first()
    
    total_expenses = total_result.total_amount or 0.0
    total_expense_count = total_result.total_count or 0
    
    # Get category-wise summary
    category_results = db.query(
        Expense.category,
        func.sum(Expense.amount).label('total_amount'),
        func.count(Expense.id).label('expense_count')
    ).filter(
        Expense.user_id == current_user.id
    ).group_by(Expense.category).all()
    
    # Calculate category summaries with percentages
    category_summary = []
    for category, amount, count in category_results:
        percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0.0
        category_summary.append(CategorySummary(
            category=category,
            total_amount=amount or 0.0,
            expense_count=count,
            percentage=round(percentage, 2)
        ))
    
    # Sort by total amount (descending)
    category_summary.sort(key=lambda x: x.total_amount, reverse=True)
    
    # Get monthly expenses (last 12 months)
    monthly_results = db.query(
        func.date_format(Expense.date, '%Y-%m').label('month'),
        func.sum(Expense.amount).label('total_amount'),
        func.count(Expense.id).label('expense_count')
    ).filter(
        Expense.user_id == current_user.id,
        Expense.date >= (current_date - timedelta(days=365))
    ).group_by(
        func.date_format(Expense.date, '%Y-%m')
    ).order_by(
        func.date_format(Expense.date, '%Y-%m').desc()
    ).all()
    
    monthly_expenses = [
        MonthlyExpense(
            month=month,
            total_amount=amount or 0.0,
            expense_count=count
        )
        for month, amount, count in monthly_results
    ]
    
    # Calculate current month totals
    current_month_result = db.query(
        func.sum(Expense.amount).label('total_amount'),
        func.count(Expense.id).label('total_count')
    ).filter(
        Expense.user_id == current_user.id,
        extract('year', Expense.date) == current_year,
        extract('month', Expense.date) == current_month
    ).first()
    
    current_month_total = current_month_result.total_amount or 0.0
    current_month_count = current_month_result.total_count or 0
    
    return DashboardSummary(
        total_expenses=total_expenses,
        total_expense_count=total_expense_count,
        category_summary=category_summary,
        monthly_expenses=monthly_expenses,
        current_month_total=current_month_total,
        current_month_count=current_month_count
    )
