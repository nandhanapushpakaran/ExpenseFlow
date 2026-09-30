from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryOut, CategoryUpdate
from app.services.category_service import CategoryService

router = APIRouter()


@router.get("", response_model=List[CategoryOut])
def get_categories(
    type: Optional[str] = Query(None, pattern="^(INCOME|EXPENSE)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all categories available to the user (system defaults + user custom).
    """
    return CategoryService.get_categories(db, user_id=current_user.id, type=type)


@router.post("", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(
    category_in: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new custom category for the authenticated user.
    """
    return CategoryService.create_category(db, user_id=current_user.id, category_in=category_in)


@router.put("/{category_id}", response_model=CategoryOut)
def update_category(
    category_id: int,
    category_in: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a custom user category.
    """
    return CategoryService.update_category(
        db, category_id=category_id, user_id=current_user.id, category_in=category_in
    )


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a custom user category if no transactions reference it.
    """
    CategoryService.delete_category(db, category_id=category_id, user_id=current_user.id)
    return {"message": "Category deleted successfully"}
