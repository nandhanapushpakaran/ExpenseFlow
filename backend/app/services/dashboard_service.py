import calendar
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.models.category import Category
from app.schemas.dashboard import (
    DashboardSummaryOut,
    MonthlyOverviewItem,
    CategoryBreakdownItem,
    TrendItem
)


class DashboardService:
    @staticmethod
    def _parse_month(month_str: Optional[str] = None):
        """
        Parses 'YYYY-MM' string or returns current year and month.
        """
        if month_str:
            try:
                parts = month_str.split("-")
                year = int(parts[0])
                month = int(parts[1])
                return year, month
            except Exception:
                pass
        today = date.today()
        return today.year, today.month

    @staticmethod
    def get_summary(
        db: Session,
        user_id: int,
        month_str: Optional[str] = None
    ) -> DashboardSummaryOut:
        """
        Calculates exact monthly financial summary for authenticated user:
        Total income, total expenses, net balance, savings rate, and MoM trends.
        """
        year, month = DashboardService._parse_month(month_str)

        # Current Month Range
        _, last_day = calendar.monthrange(year, month)
        start_date = date(year, month, 1)
        end_date = date(year, month, last_day)

        # Previous Month Range
        if month == 1:
            prev_year, prev_month = year - 1, 12
        else:
            prev_year, prev_month = year, month - 1
        _, prev_last_day = calendar.monthrange(prev_year, prev_month)
        prev_start_date = date(prev_year, prev_month, 1)
        prev_end_date = date(prev_year, prev_month, prev_last_day)

        # Current Month Queries
        income_sum = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.type == "INCOME",
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).scalar() or Decimal("0.00")

        expense_sum = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.type == "EXPENSE",
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).scalar() or Decimal("0.00")

        tx_count = db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).count()

        # Previous Month Queries
        prev_income_sum = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.type == "INCOME",
            Transaction.transaction_date >= prev_start_date,
            Transaction.transaction_date <= prev_end_date
        ).scalar() or Decimal("0.00")

        prev_expense_sum = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.type == "EXPENSE",
            Transaction.transaction_date >= prev_start_date,
            Transaction.transaction_date <= prev_end_date
        ).scalar() or Decimal("0.00")

        # Conversions to Decimal with 2 decimal places
        total_income = Decimal(str(income_sum)).quantize(Decimal("0.01"))
        total_expenses = Decimal(str(expense_sum)).quantize(Decimal("0.01"))
        net_balance = (total_income - total_expenses).quantize(Decimal("0.01"))

        prev_total_income = Decimal(str(prev_income_sum)).quantize(Decimal("0.01"))
        prev_total_expenses = Decimal(str(prev_expense_sum)).quantize(Decimal("0.01"))

        # Savings Rate Calculation
        if total_income > Decimal("0.00") and net_balance > Decimal("0.00"):
            savings_rate = ((net_balance / total_income) * Decimal("100.00")).quantize(Decimal("0.1"))
        else:
            savings_rate = Decimal("0.0")

        # MoM percentage changes
        if prev_total_income > Decimal("0.00"):
            income_change_pct = (
                ((total_income - prev_total_income) / prev_total_income) * Decimal("100.00")
            ).quantize(Decimal("0.1"))
        else:
            income_change_pct = Decimal("0.0")

        if prev_total_expenses > Decimal("0.00"):
            expense_change_pct = (
                ((total_expenses - prev_total_expenses) / prev_total_expenses) * Decimal("100.00")
            ).quantize(Decimal("0.1"))
        else:
            expense_change_pct = Decimal("0.0")

        period_label = f"{year}-{str(month).zfill(2)}"

        return DashboardSummaryOut(
            total_income=total_income,
            total_expenses=total_expenses,
            net_balance=net_balance,
            savings_rate=savings_rate,
            transaction_count=tx_count,
            period=period_label,
            prev_total_income=prev_total_income,
            prev_total_expenses=prev_total_expenses,
            income_change_pct=income_change_pct,
            expense_change_pct=expense_change_pct
        )

    @staticmethod
    def get_monthly_overview(
        db: Session,
        user_id: int,
        months_count: int = 6
    ) -> List[MonthlyOverviewItem]:
        """
        Returns monthly income vs expenses for the past N months.
        """
        today = date.today()
        result = []

        # Iterate backwards from current month
        for i in range(months_count - 1, -1, -1):
            target_date = today - timedelta(days=i * 30)
            year = target_date.year
            month = target_date.month
            _, last_day = calendar.monthrange(year, month)
            start_date = date(year, month, 1)
            end_date = date(year, month, last_day)

            inc = db.query(func.sum(Transaction.amount)).filter(
                Transaction.user_id == user_id,
                Transaction.type == "INCOME",
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date
            ).scalar() or Decimal("0.00")

            exp = db.query(func.sum(Transaction.amount)).filter(
                Transaction.user_id == user_id,
                Transaction.type == "EXPENSE",
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date
            ).scalar() or Decimal("0.00")

            income_val = Decimal(str(inc)).quantize(Decimal("0.01"))
            expense_val = Decimal(str(exp)).quantize(Decimal("0.01"))
            net_val = (income_val - expense_val).quantize(Decimal("0.01"))

            month_key = f"{year}-{str(month).zfill(2)}"
            month_name = calendar.month_abbr[month]

            result.append(
                MonthlyOverviewItem(
                    month=month_key,
                    month_name=month_name,
                    income=income_val,
                    expense=expense_val,
                    net=net_val
                )
            )

        return result

    @staticmethod
    def get_category_breakdown(
        db: Session,
        user_id: int,
        month_str: Optional[str] = None
    ) -> List[CategoryBreakdownItem]:
        """
        Returns expense breakdown by category for the selected month with percentage of total.
        """
        year, month = DashboardService._parse_month(month_str)
        _, last_day = calendar.monthrange(year, month)
        start_date = date(year, month, 1)
        end_date = date(year, month, last_day)

        # Total expenses for percentage calculation
        total_exp = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.type == "EXPENSE",
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).scalar() or Decimal("0.00")
        total_exp_decimal = Decimal(str(total_exp))

        # Query grouped by category
        rows = db.query(
            Category.name,
            Category.color,
            Category.type,
            func.sum(Transaction.amount).label("category_total")
        ).join(
            Transaction, Transaction.category_id == Category.id
        ).filter(
            Transaction.user_id == user_id,
            Transaction.type == "EXPENSE",
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).group_by(
            Category.id, Category.name, Category.color, Category.type
        ).order_by(
            func.sum(Transaction.amount).desc()
        ).all()

        items = []
        for name, color, cat_type, cat_total in rows:
            amt = Decimal(str(cat_total)).quantize(Decimal("0.01"))
            pct = (
                ((amt / total_exp_decimal) * Decimal("100.00")).quantize(Decimal("0.1"))
                if total_exp_decimal > Decimal("0.00")
                else Decimal("0.0")
            )
            items.append(
                CategoryBreakdownItem(
                    name=name,
                    color=color,
                    type=cat_type,
                    total_amount=amt,
                    percentage=pct
                )
            )

        return items

    @staticmethod
    def get_spending_trends(
        db: Session,
        user_id: int,
        months_count: int = 6
    ) -> List[TrendItem]:
        """
        Returns chronological expense trend data points.
        """
        monthly_data = DashboardService.get_monthly_overview(db, user_id, months_count)
        return [
            TrendItem(
                date=item.month,
                label=item.month_name,
                amount=item.expense
            )
            for item in monthly_data
        ]
