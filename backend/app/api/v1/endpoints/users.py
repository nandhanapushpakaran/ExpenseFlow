from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserOut)
def read_user_me(current_user: User = Depends(get_current_user)):
    """
    Get current logged in user.
    """
    return current_user


@router.patch("/me", response_model=UserOut)
def update_user_me(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update profile of current user.
    """
    if user_update.name is not None:
        current_user.name = user_update.name.strip()
    if user_update.preferred_currency is not None:
        current_user.preferred_currency = user_update.preferred_currency.upper()

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user
