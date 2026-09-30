import math
from datetime import date
from typing import Optional
from sqlalchemy import or_, desc, asc
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from app.models.transaction import Transaction
from app.models.category import Category
from app.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
    PaginatedTransactionsOut,
    TransactionOut
)


class TransactionService:
    @staticmethod
    def get_transactions(
        db: Session,
        user_id: int,
        page: int = 1,
        limit: int = 10,
        type: Optional[str] = None,
        category_id: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        search: Optional[str] = None,
        sort_by: str = "transaction_date",
        sort_order: str = "desc"
    ) -> PaginatedTransactionsOut:
        """
        Retrieves paginated and filtered transactions exclusively for the authenticated user.
        """
        # Strict user scoping
        query = db.query(Transaction).options(joinedload(Transaction.category)).filter(
            Transaction.user_id == user_id
        )

        if type:
            query = query.filter(Transaction.type == type.upper())

        if category_id:
            query = query.filter(Transaction.category_id == category_id)

        if start_date:
            query = query.filter(Transaction.transaction_date >= start_date)

        if end_date:
            query = query.filter(Transaction.transaction_date <= end_date)

        if search:
            search_pattern = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Transaction.description.ilike(search_pattern),
                    Transaction.notes.ilike(search_pattern)
                )
            )

        total = query.count()

        # Sorting
        sort_column = getattr(Transaction, sort_by, Transaction.transaction_date)
        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column), asc(Transaction.id))
        else:
            query = query.order_by(desc(sort_column), desc(Transaction.id))

        # Pagination calculation
        offset = (page - 1) * limit
        items = query.offset(offset).limit(limit).all()
        pages = math.ceil(total / limit) if total > 0 else 1

        return PaginatedTransactionsOut(
            items=[TransactionOut.model_validate(item) for item in items],
            total=total,
            page=page,
            limit=limit,
            pages=pages
        )

    @staticmethod
    def get_transaction_by_id(db: Session, transaction_id: int, user_id: int) -> Transaction:
        """
        Retrieves single transaction ensuring multi-tenant data isolation.
        """
        tx = db.query(Transaction).options(joinedload(Transaction.category)).filter(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id
        ).first()

        if not tx:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        return tx

    @staticmethod
    def create_transaction(
        db: Session,
        user_id: int,
        tx_in: TransactionCreate
    ) -> Transaction:
        """
        Creates a new transaction for user with exact decimal amount and valid category verification.
        """
        # Verify category exists and is accessible
        category = db.query(Category).filter(
            Category.id == tx_in.category_id,
            or_(Category.user_id == None, Category.user_id == user_id)
        ).first()

        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid category selected."
            )

        # Enforce that category type matches transaction type
        if category.type != tx_in.type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category '{category.name}' is an {category.type} category, but transaction is {tx_in.type}."
            )

        transaction = Transaction(
            user_id=user_id,
            category_id=tx_in.category_id,
            type=tx_in.type,
            amount=tx_in.amount,
            description=tx_in.description.strip(),
            notes=tx_in.notes.strip() if tx_in.notes else None,
            transaction_date=tx_in.transaction_date,
            payment_method=tx_in.payment_method
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction

    @staticmethod
    def update_transaction(
        db: Session,
        transaction_id: int,
        user_id: int,
        tx_in: TransactionUpdate
    ) -> Transaction:
        """
        Updates an existing transaction scoped strictly to the authenticated user.
        """
        tx = TransactionService.get_transaction_by_id(db, transaction_id, user_id)

        # Validate category if changed
        if tx_in.category_id is not None:
            category = db.query(Category).filter(
                Category.id == tx_in.category_id,
                or_(Category.user_id == None, Category.user_id == user_id)
            ).first()
            if not category:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category.")
            target_type = tx_in.type or tx.type
            if category.type != target_type:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Category type ({category.type}) does not match transaction type ({target_type})."
                )
            tx.category_id = tx_in.category_id

        if tx_in.type is not None:
            tx.type = tx_in.type
        if tx_in.amount is not None:
            tx.amount = tx_in.amount
        if tx_in.description is not None:
            tx.description = tx_in.description.strip()
        if tx_in.notes is not None:
            tx.notes = tx_in.notes.strip() if tx_in.notes else None
        if tx_in.transaction_date is not None:
            tx.transaction_date = tx_in.transaction_date
        if tx_in.payment_method is not None:
            tx.payment_method = tx_in.payment_method

        db.add(tx)
        db.commit()
        db.refresh(tx)
        return tx

    @staticmethod
    def delete_transaction(db: Session, transaction_id: int, user_id: int) -> None:
        """
        Deletes a transaction scoped strictly to the authenticated user.
        """
        tx = TransactionService.get_transaction_by_id(db, transaction_id, user_id)
        db.delete(tx)
        db.commit()
