from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.transaction import (
    TransactionCreate,
    TransactionOut,
    TransactionUpdate,
    PaginatedTransactionsOut
)
from app.services.transaction_service import TransactionService

router = APIRouter()


@router.get("", response_model=PaginatedTransactionsOut)
def get_transactions(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    type: Optional[str] = Query(None, pattern="^(INCOME|EXPENSE)$"),
    category_id: Optional[int] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: str = Query("transaction_date", pattern="^(transaction_date|amount|created_at)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List user transactions with filtering, pagination, and sorting.
    """
    return TransactionService.get_transactions(
        db=db,
        user_id=current_user.id,
        page=page,
        limit=limit,
        type=type,
        category_id=category_id,
        start_date=start_date,
        end_date=end_date,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order
    )


@router.post("", response_model=TransactionOut, status_code=status.HTTP_201_CREATED)
def create_transaction(
    tx_in: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new transaction (Income or Expense).
    """
    return TransactionService.create_transaction(
        db=db,
        user_id=current_user.id,
        tx_in=tx_in
    )


@router.get("/{transaction_id}", response_model=TransactionOut)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve single transaction detail.
    """
    return TransactionService.get_transaction_by_id(
        db=db,
        transaction_id=transaction_id,
        user_id=current_user.id
    )


@router.put("/{transaction_id}", response_model=TransactionOut)
def update_transaction(
    transaction_id: int,
    tx_in: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a transaction.
    """
    return TransactionService.update_transaction(
        db=db,
        transaction_id=transaction_id,
        user_id=current_user.id,
        tx_in=tx_in
    )


@router.delete("/{transaction_id}", status_code=status.HTTP_200_OK)
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a transaction.
    """
    TransactionService.delete_transaction(
        db=db,
        transaction_id=transaction_id,
        user_id=current_user.id
    )
    return {"message": "Transaction deleted successfully"}
