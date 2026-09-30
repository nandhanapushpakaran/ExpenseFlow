from datetime import date
from fastapi import status


def get_category_id(client, headers, name):
    res = client.get("/api/v1/categories", headers=headers)
    cat = next(c for c in res.json() if c["name"] == name)
    return cat["id"]


def test_create_income_transaction(client, auth_headers):
    cat_id = get_category_id(client, auth_headers, "Salary")
    payload = {
        "category_id": cat_id,
        "type": "INCOME",
        "amount": 3500.50,
        "description": "Bi-weekly paycheck",
        "transaction_date": str(date.today()),
        "payment_method": "Bank Transfer"
    }
    response = client.post("/api/v1/transactions", json=payload, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert float(data["amount"]) == 3500.50
    assert data["type"] == "INCOME"
    assert data["category"]["name"] == "Salary"


def test_create_expense_transaction(client, auth_headers):
    cat_id = get_category_id(client, auth_headers, "Groceries")
    payload = {
        "category_id": cat_id,
        "type": "EXPENSE",
        "amount": 85.25,
        "description": "Weekly essentials",
        "transaction_date": str(date.today()),
        "payment_method": "Debit Card"
    }
    response = client.post("/api/v1/transactions", json=payload, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert float(data["amount"]) == 85.25
    assert data["type"] == "EXPENSE"


def test_validation_rejects_negative_or_zero_amount(client, auth_headers):
    cat_id = get_category_id(client, auth_headers, "Groceries")
    payload = {
        "category_id": cat_id,
        "type": "EXPENSE",
        "amount": -50.00,
        "description": "Negative expense",
        "transaction_date": str(date.today())
    }
    response = client.post("/api/v1/transactions", json=payload, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_validation_rejects_category_type_mismatch(client, auth_headers):
    # Try creating an EXPENSE with an INCOME category (Salary)
    salary_id = get_category_id(client, auth_headers, "Salary")
    payload = {
        "category_id": salary_id,
        "type": "EXPENSE",
        "amount": 100.00,
        "description": "Invalid category type",
        "transaction_date": str(date.today())
    }
    response = client.post("/api/v1/transactions", json=payload, headers=auth_headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "category" in response.json()["detail"].lower()


def test_delete_transaction(client, auth_headers):
    cat_id = get_category_id(client, auth_headers, "Groceries")
    res = client.post("/api/v1/transactions", json={
        "category_id": cat_id,
        "type": "EXPENSE",
        "amount": 25.00,
        "description": "Snacks",
        "transaction_date": str(date.today())
    }, headers=auth_headers)
    tx_id = res.json()["id"]

    del_res = client.delete(f"/api/v1/transactions/{tx_id}", headers=auth_headers)
    assert del_res.status_code == status.HTTP_200_OK

    # Ensure it no longer exists
    get_res = client.get(f"/api/v1/transactions/{tx_id}", headers=auth_headers)
    assert get_res.status_code == status.HTTP_404_NOT_FOUND
