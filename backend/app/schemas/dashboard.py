from decimal import Decimal
from typing import List
from pydantic import BaseModel


class DashboardSummaryOut(BaseModel):
    total_income: Decimal
    total_expenses: Decimal
    net_balance: Decimal
    savings_rate: Decimal
    transaction_count: int
    period: str
    prev_total_income: Decimal
    prev_total_expenses: Decimal
    income_change_pct: Decimal
    expense_change_pct: Decimal


class MonthlyOverviewItem(BaseModel):
    month: str
    month_name: str
    income: Decimal
    expense: Decimal
    net: Decimal


class CategoryBreakdownItem(BaseModel):
    name: str
    color: str
    type: str
    total_amount: Decimal
    percentage: Decimal


class TrendItem(BaseModel):
    date: str
    label: str
    amount: Decimal
