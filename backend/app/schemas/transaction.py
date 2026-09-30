from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.category import CategoryOut


class TransactionBase(BaseModel):
    category_id: int
    type: str = Field(..., pattern="^(INCOME|EXPENSE)$")
    amount: Decimal = Field(..., gt=Decimal("0.00"), decimal_places=2, max_digits=12)
    description: str = Field(..., min_length=1, max_length=255)
    notes: Optional[str] = None
    transaction_date: date
    payment_method: Optional[str] = Field("Debit Card", max_length=50)


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    category_id: Optional[int] = None
    type: Optional[str] = Field(None, pattern="^(INCOME|EXPENSE)$")
    amount: Optional[Decimal] = Field(None, gt=Decimal("0.00"), decimal_places=2, max_digits=12)
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    notes: Optional[str] = None
    transaction_date: Optional[date] = None
    payment_method: Optional[str] = Field(None, max_length=50)


class TransactionOut(TransactionBase):
    id: int
    user_id: int
    created_at: datetime
    category: Optional[CategoryOut] = None

    model_config = ConfigDict(from_attributes=True)


class PaginatedTransactionsOut(BaseModel):
    items: List[TransactionOut]
    total: int
    page: int
    limit: int
    pages: int
