"""
Dashboard Schemas Module

This module defines Pydantic schemas for dashboard statistics.

Why this file exists:
- Serializes dashboard statistics for API responses
- Provides type safety for dashboard data
- Separates dashboard data structures from business logic
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CategorySummary(BaseModel):
    """
    Schema for category-wise expense summary.
    
    Represents expenses grouped by category with totals and percentages.
    """
    category: str
    total_amount: float
    expense_count: int
    percentage: float  # Percentage of total expenses


class MonthlyExpense(BaseModel):
    """
    Schema for monthly expense summary.
    
    Represents expenses grouped by month.
    """
    month: str  # Format: "YYYY-MM"
    total_amount: float
    expense_count: int


class DashboardSummary(BaseModel):
    """
    Schema for complete dashboard summary.
    
    Contains all dashboard statistics in a single response.
    """
    total_expenses: float
    total_expense_count: int
    category_summary: List[CategorySummary]
    monthly_expenses: List[MonthlyExpense]
    current_month_total: float
    current_month_count: int
