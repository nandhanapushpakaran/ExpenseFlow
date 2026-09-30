from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password


class AuthService:
    @staticmethod
    def register_user(db: Session, user_in: UserCreate) -> User:
        """
        Registers a new user after verifying that the email is unique.
        """
        existing_user = db.query(User).filter(User.email == user_in.email.lower()).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email address already exists."
            )

        hashed_password = get_password_hash(user_in.password)
        user = User(
            email=user_in.email.lower(),
            name=user_in.name.strip(),
            hashed_password=hashed_password,
            preferred_currency=user_in.preferred_currency.upper(),
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticates a user by email and password.
        """
        user = db.query(User).filter(User.email == email.lower()).first()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
