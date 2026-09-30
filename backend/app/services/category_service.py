from typing import List, Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.category import Category
from app.models.transaction import Transaction
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    @staticmethod
    def get_categories(
        db: Session,
        user_id: int,
        type: Optional[str] = None
    ) -> List[Category]:
        """
        Returns all system default categories and user custom categories.
        Optionally filtered by type ('INCOME' or 'EXPENSE').
        """
        query = db.query(Category).filter(
            or_(Category.user_id == None, Category.user_id == user_id)
        )
        if type:
            query = query.filter(Category.type == type.upper())

        return query.order_by(Category.is_default.desc(), Category.name.asc()).all()

    @staticmethod
    def get_category_by_id(db: Session, category_id: int, user_id: int) -> Optional[Category]:
        """
        Retrieves a category accessible by the user (either default or user-owned).
        """
        return db.query(Category).filter(
            Category.id == category_id,
            or_(Category.user_id == None, Category.user_id == user_id)
        ).first()

    @staticmethod
    def create_category(db: Session, user_id: int, category_in: CategoryCreate) -> Category:
        """
        Creates a custom category for the user.
        Checks for duplicate names under the same type for this user.
        """
        name_clean = category_in.name.strip()
        existing = db.query(Category).filter(
            or_(Category.user_id == None, Category.user_id == user_id),
            Category.type == category_in.type.upper(),
            Category.name.ilike(name_clean)
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"A category named '{name_clean}' already exists for {category_in.type.lower()}."
            )

        category = Category(
            user_id=user_id,
            name=name_clean,
            type=category_in.type.upper(),
            color=category_in.color or "#6366f1",
            icon=category_in.icon,
            is_default=False
        )
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def update_category(
        db: Session,
        category_id: int,
        user_id: int,
        category_in: CategoryUpdate
    ) -> Category:
        """
        Updates a user-owned custom category. Default system categories cannot be modified.
        """
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

        if category.is_default or category.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="System default categories cannot be modified"
            )

        if category_in.name is not None:
            category.name = category_in.name.strip()
        if category_in.color is not None:
            category.color = category_in.color
        if category_in.icon is not None:
            category.icon = category_in.icon

        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def delete_category(db: Session, category_id: int, user_id: int) -> None:
        """
        Safely deletes a user-owned category.
        Ensures that system default categories cannot be deleted,
        and that categories with linked transactions cannot be deleted without reassigning.
        """
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

        if category.is_default or category.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="System default categories cannot be deleted"
            )

        # Check if transactions are assigned to this category
        tx_count = db.query(Transaction).filter(
            Transaction.category_id == category_id,
            Transaction.user_id == user_id
        ).count()

        if tx_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot delete category '{category.name}' because {tx_count} transaction(s) are assigned to it. Please reassign or delete them first."
            )

        db.delete(category)
        db.commit()
