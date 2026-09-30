from datetime import date
from decimal import Decimal
from fastapi import status


def get_cat_id(client, headers, name):
    res = client.get("/api/v1/categories", headers=headers)
    cat = next(c for c in res.json() if c["name"] == name)
    return cat["id"]


def test_dashboard_summary_calculations(client, auth_headers):
    today = date.today()
    month_str = f"{today.year}-{str(today.month).zfill(2)}"

    salary_id = get_cat_id(client, auth_headers, "Salary")
    groceries_id = get_cat_id(client, auth_headers, "Groceries")

    # Add Income: $5,000.00
    client.post("/api/v1/transactions", json={
        "category_id": salary_id,
        "type": "INCOME",
        "amount": 5000.00,
        "description": "Monthly Salary",
        "transaction_date": str(today)
    }, headers=auth_headers)

    # Add Expense: $1,250.00
    client.post("/api/v1/transactions", json={
        "category_id": groceries_id,
        "type": "EXPENSE",
        "amount": 1250.00,
        "description": "Food & Supplies",
        "transaction_date": str(today)
    }, headers=auth_headers)

    # Get Dashboard Summary
    res = client.get(f"/api/v1/dashboard/summary?month={month_str}", headers=auth_headers)
    assert res.status_code == status.HTTP_200_OK
    data = res.json()

    assert float(data["total_income"]) == 5000.00
    assert float(data["total_expenses"]) == 1250.00
    assert float(data["net_balance"]) == 3750.00
    # Savings rate = (3750 / 5000) * 100 = 75.0%
    assert float(data["savings_rate"]) == 75.0
    assert data["transaction_count"] == 2


def test_dashboard_empty_month(client, auth_headers):
    # Query future or empty month
    res = client.get("/api/v1/dashboard/summary?month=2020-01", headers=auth_headers)
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert float(data["total_income"]) == 0.0
    assert float(data["total_expenses"]) == 0.0
    assert float(data["net_balance"]) == 0.0
    assert float(data["savings_rate"]) == 0.0
    assert data["transaction_count"] == 0
