"""
Database Seed Script: Populates development environment with realistic demo data.
Includes demo user and 3+ months of diverse income & expense transactions.
Usage: python -m app.db.seed
"""

from datetime import date, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.db.init_db import init_db
from app.models.user import User
from app.models.category import Category
from app.models.transaction import Transaction
from app.core.security import get_password_hash


def seed_demo_data(db: Session) -> None:
    # Ensure tables and default categories exist
    init_db(db)

    print("Seeding demo user...")
    demo_email = "demo@expensetracker.dev"
    demo_user = db.query(User).filter(User.email == demo_email).first()

    if not demo_user:
        demo_user = User(
            email=demo_email,
            name="Demo User",
            hashed_password=get_password_hash("DemoPass123!"),
            preferred_currency="USD",
            is_active=True
        )
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)
        print(f"Created demo user: {demo_email}")
    else:
        print(f"Demo user already exists: {demo_email}")

    # Remove previous demo transactions to allow clean re-seeding
    db.query(Transaction).filter(Transaction.user_id == demo_user.id).delete()
    db.commit()

    # Fetch default categories by name
    categories = {cat.name: cat for cat in db.query(Category).filter(Category.user_id == None).all()}

    print("Seeding realistic multi-month transactions...")
    today = date.today()

    sample_transactions = [
        # --- Current Month (Month 0) ---
        {
            "category": "Salary",
            "type": "INCOME",
            "amount": Decimal("4200.00"),
            "description": "TechCorp Monthly Direct Deposit",
            "days_ago": 2,
            "method": "Bank Transfer",
            "notes": "Base monthly salary"
        },
        {
            "category": "Freelance",
            "type": "INCOME",
            "amount": Decimal("850.00"),
            "description": "Vue.js SaaS Dashboard Consulting",
            "days_ago": 5,
            "method": "Bank Transfer",
            "notes": "Client project milestone 2"
        },
        {
            "category": "Rent & Housing",
            "type": "EXPENSE",
            "amount": Decimal("1450.00"),
            "description": "Apartment Monthly Rent",
            "days_ago": 1,
            "method": "Bank Transfer",
            "notes": "Downtown 1-bedroom flat"
        },
        {
            "category": "Groceries",
            "type": "EXPENSE",
            "amount": Decimal("142.60"),
            "description": "Weekly Groceries at Trader Joe's",
            "days_ago": 3,
            "method": "Debit Card",
            "notes": "Produce, pantry staples, coffee"
        },
        {
            "category": "Bills & Utilities",
            "type": "EXPENSE",
            "amount": Decimal("95.40"),
            "description": "High-Speed Fiber Internet & Electricity",
            "days_ago": 6,
            "method": "Credit Card",
            "notes": "Monthly recurring utility bill"
        },
        {
            "category": "Food & Dining",
            "type": "EXPENSE",
            "amount": Decimal("58.20"),
            "description": "Dinner with colleagues at Trattoria",
            "days_ago": 7,
            "method": "Credit Card",
            "notes": "Italian dinner"
        },
        {
            "category": "Transportation",
            "type": "EXPENSE",
            "amount": Decimal("65.00"),
            "description": "Monthly Metro Transit Pass",
            "days_ago": 8,
            "method": "Debit Card",
            "notes": "Subway & bus card recharge"
        },
        {
            "category": "Entertainment",
            "type": "EXPENSE",
            "amount": Decimal("24.99"),
            "description": "Streaming Subscriptions (Netflix & Spotify)",
            "days_ago": 9,
            "method": "Credit Card",
            "notes": "Monthly entertainment bundle"
        },

        # --- Previous Month (Month -1) ---
        {
            "category": "Salary",
            "type": "INCOME",
            "amount": Decimal("4200.00"),
            "description": "TechCorp Monthly Direct Deposit",
            "days_ago": 32,
            "method": "Bank Transfer",
            "notes": "Regular payroll deposit"
        },
        {
            "category": "Investment",
            "type": "INCOME",
            "amount": Decimal("320.50"),
            "description": "Quarterly Index ETF Dividend Payout",
            "days_ago": 35,
            "method": "Bank Transfer",
            "notes": "S&P 500 ETF dividend"
        },
        {
            "category": "Rent & Housing",
            "type": "EXPENSE",
            "amount": Decimal("1450.00"),
            "description": "Apartment Monthly Rent",
            "days_ago": 31,
            "method": "Bank Transfer",
            "notes": "Rent payment"
        },
        {
            "category": "Groceries",
            "type": "EXPENSE",
            "amount": Decimal("185.30"),
            "description": "Bulk Grocery Run at Costco",
            "days_ago": 36,
            "method": "Debit Card",
            "notes": "Household goods and groceries"
        },
        {
            "category": "Shopping",
            "type": "EXPENSE",
            "amount": Decimal("129.99"),
            "description": "Mechanical Keyboard & Desk Mat",
            "days_ago": 40,
            "method": "Credit Card",
            "notes": "Home office upgrade"
        },
        {
            "category": "Healthcare",
            "type": "EXPENSE",
            "amount": Decimal("75.00"),
            "description": "Annual Dental Cleaning & Checkup",
            "days_ago": 45,
            "method": "Debit Card",
            "notes": "Dental copay"
        },
        {
            "category": "Food & Dining",
            "type": "EXPENSE",
            "amount": Decimal("42.50"),
            "description": "Weekend Brunch at Cafe Lumiere",
            "days_ago": 48,
            "method": "Credit Card",
            "notes": "Coffee & brunch"
        },

        # --- Two Months Ago (Month -2) ---
        {
            "category": "Salary",
            "type": "INCOME",
            "amount": Decimal("4200.00"),
            "description": "TechCorp Monthly Direct Deposit",
            "days_ago": 62,
            "method": "Bank Transfer",
            "notes": "Regular payroll deposit"
        },
        {
            "category": "Gift",
            "type": "INCOME",
            "amount": Decimal("200.00"),
            "description": "Birthday Gift from Family",
            "days_ago": 65,
            "method": "Cash",
            "notes": "Birthday celebration"
        },
        {
            "category": "Rent & Housing",
            "type": "EXPENSE",
            "amount": Decimal("1450.00"),
            "description": "Apartment Monthly Rent",
            "days_ago": 61,
            "method": "Bank Transfer",
            "notes": "Rent payment"
        },
        {
            "category": "Travel",
            "type": "EXPENSE",
            "amount": Decimal("380.00"),
            "description": "Weekend Mountain Cabin Getaway",
            "days_ago": 68,
            "method": "Credit Card",
            "notes": "Lodging and trail passes"
        },
        {
            "category": "Education",
            "type": "EXPENSE",
            "amount": Decimal("49.00"),
            "description": "Full-Stack Web Architecture Course",
            "days_ago": 72,
            "method": "Credit Card",
            "notes": "Online technical certification"
        },
        {
            "category": "Groceries",
            "type": "EXPENSE",
            "amount": Decimal("164.20"),
            "description": "Bi-weekly Grocery Haul",
            "days_ago": 75,
            "method": "Debit Card",
            "notes": "Organic groceries"
        }
    ]

    for item in sample_transactions:
        cat = categories.get(item["category"])
        if not cat:
            print(f"Warning: Category '{item['category']}' not found, skipping...")
            continue

        tx_date = today - timedelta(days=item["days_ago"])
        tx = Transaction(
            user_id=demo_user.id,
            category_id=cat.id,
            type=item["type"],
            amount=item["amount"],
            description=item["description"],
            notes=item["notes"],
            transaction_date=tx_date,
            payment_method=item["method"]
        )
        db.add(tx)

    db.commit()
    print("Demo data successfully seeded!")
    print("\nDemo Account Credentials:")
    print("---------------------------------")
    print(f"Email:    {demo_email}")
    print("Password: DemoPass123!")
    print("---------------------------------")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_demo_data(db)
    finally:
        db.close()
