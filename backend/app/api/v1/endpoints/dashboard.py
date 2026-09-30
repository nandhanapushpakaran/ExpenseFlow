from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.dashboard import (
    DashboardSummaryOut,
    MonthlyOverviewItem,
    CategoryBreakdownItem,
    TrendItem
)
from app.services.dashboard_service import DashboardService

router = APIRouter()


@router.get("/summary", response_model=DashboardSummaryOut)
def get_dashboard_summary(
    month: Optional[str] = Query(None, description="Month in YYYY-MM format"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get financial summary (income, expenses, net balance, savings rate) for the specified month.
    """
    return DashboardService.get_summary(
        db=db,
        user_id=current_user.id,
        month_str=month
    )


@router.get("/monthly", response_model=List[MonthlyOverviewItem])
def get_monthly_overview(
    months: int = Query(6, ge=1, le=24, description="Number of months to retrieve"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get income vs expenses over the last N months.
    """
    return DashboardService.get_monthly_overview(
        db=db,
        user_id=current_user.id,
        months_count=months
    )


@router.get("/category-breakdown", response_model=List[CategoryBreakdownItem])
def get_category_breakdown(
    month: Optional[str] = Query(None, description="Month in YYYY-MM format"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get expense distribution breakdown by category for doughnut chart.
    """
    return DashboardService.get_category_breakdown(
        db=db,
        user_id=current_user.id,
        month_str=month
    )


@router.get("/trends", response_model=List[TrendItem])
def get_spending_trends(
    months: int = Query(6, ge=1, le=24),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get spending trends over time.
    """
    return DashboardService.get_spending_trends(
        db=db,
        user_id=current_user.id,
        months_count=months
    )
