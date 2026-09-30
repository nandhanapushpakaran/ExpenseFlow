from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.transaction import Transaction


class Category(Base, TimestampMixin):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # user_id is nullable: system default categories have user_id=None
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)  # 'INCOME' | 'EXPENSE'
    color: Mapped[str] = mapped_column(String(20), default="#6366f1", nullable=False)
    icon: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    user: Mapped[Optional["User"]] = relationship("User", back_populates="categories")
    transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction",
        back_populates="category"
    )

    def __repr__(self) -> str:
        return f"<Category id={self.id} name='{self.name}' type='{self.type}' is_default={self.is_default}>"
