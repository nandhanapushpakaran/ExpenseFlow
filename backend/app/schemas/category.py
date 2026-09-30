from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., pattern="^(INCOME|EXPENSE)$")
    color: str = Field(default="#6366f1", max_length=20)
    icon: Optional[str] = Field(None, max_length=50)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    color: Optional[str] = Field(None, max_length=20)
    icon: Optional[str] = Field(None, max_length=50)


class CategoryOut(CategoryBase):
    id: int
    user_id: Optional[int] = None
    is_default: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
