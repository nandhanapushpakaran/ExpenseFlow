from sqlalchemy.orm import Session
from app.db.base import Base
from app.db.session import engine
from app.models.category import Category

DEFAULT_CATEGORIES = [
    # Default Income Categories
    {"name": "Salary", "type": "INCOME", "color": "#10b981", "icon": "briefcase"},
    {"name": "Freelance", "type": "INCOME", "color": "#06b6d4", "icon": "laptop"},
    {"name": "Business", "type": "INCOME", "color": "#3b82f6", "icon": "building"},
    {"name": "Investment", "type": "INCOME", "color": "#8b5cf6", "icon": "trending-up"},
    {"name": "Gift", "type": "INCOME", "color": "#ec4899", "icon": "gift"},
    {"name": "Other Income", "type": "INCOME", "color": "#64748b", "icon": "more-horizontal"},

    # Default Expense Categories
    {"name": "Food & Dining", "type": "EXPENSE", "color": "#f97316", "icon": "utensils"},
    {"name": "Groceries", "type": "EXPENSE", "color": "#10b981", "icon": "shopping-cart"},
    {"name": "Transportation", "type": "EXPENSE", "color": "#0ea5e9", "icon": "car"},
    {"name": "Rent & Housing", "type": "EXPENSE", "color": "#6366f1", "icon": "home"},
    {"name": "Bills & Utilities", "type": "EXPENSE", "color": "#eab308", "icon": "file-text"},
    {"name": "Shopping", "type": "EXPENSE", "color": "#ec4899", "icon": "shopping-bag"},
    {"name": "Healthcare", "type": "EXPENSE", "color": "#ef4444", "icon": "activity"},
    {"name": "Entertainment", "type": "EXPENSE", "color": "#8b5cf6", "icon": "film"},
    {"name": "Education", "type": "EXPENSE", "color": "#14b8a6", "icon": "book"},
    {"name": "Travel", "type": "EXPENSE", "color": "#f59e0b", "icon": "compass"},
    {"name": "Other Expense", "type": "EXPENSE", "color": "#94a3b8", "icon": "more-horizontal"},
]


def init_db(db: Session) -> None:
    """
    Initializes database tables and seeds default categories if not already present.
    Never deletes or overwrites existing user data.
    """
    Base.metadata.create_all(bind=engine)

    # Check and seed default categories
    for cat_data in DEFAULT_CATEGORIES:
        existing = db.query(Category).filter(
            Category.user_id == None,
            Category.name == cat_data["name"],
            Category.type == cat_data["type"]
        ).first()

        if not existing:
            category = Category(
                user_id=None,
                name=cat_data["name"],
                type=cat_data["type"],
                color=cat_data["color"],
                icon=cat_data["icon"],
                is_default=True
            )
            db.add(category)

    db.commit()
