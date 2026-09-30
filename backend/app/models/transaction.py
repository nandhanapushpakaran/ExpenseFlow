from decimal import Decimal
from datetime import date
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Text, Numeric, Date, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.category import Category


class Transaction(Base, TimestampMixin):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    type: Mapped[str] = mapped_column(String(20), nullable=False)  # 'INCOME' | 'EXPENSE'
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    payment_method: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="transactions")
    category: Mapped["Category"] = relationship("Category", back_populates="transactions")

    def __repr__(self) -> str:
        return f"<Transaction id={self.id} type='{self.type}' amount={self.amount} date={self.transaction_date}>"
