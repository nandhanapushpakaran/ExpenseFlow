from datetime import date
from fastapi import status


def test_user_cannot_access_other_users_transaction(
    client,
    auth_headers,
    auth_headers_user2
):
    # Fetch a category using User 1
    res = client.get("/api/v1/categories", headers=auth_headers)
    cat_id = res.json()[0]["id"]

    # User 1 creates a private transaction
    create_res = client.post("/api/v1/transactions", json={
        "category_id": cat_id,
        "type": "EXPENSE",
        "amount": 99.99,
        "description": "User 1 Confidential Purchase",
        "transaction_date": str(date.today())
    }, headers=auth_headers)
    assert create_res.status_code == status.HTTP_201_CREATED
    tx_id = create_res.json()["id"]

    # User 2 tries to GET User 1's transaction
    get_res = client.get(f"/api/v1/transactions/{tx_id}", headers=auth_headers_user2)
    assert get_res.status_code == status.HTTP_404_NOT_FOUND

    # User 2 tries to UPDATE User 1's transaction
    update_res = client.put(f"/api/v1/transactions/{tx_id}", json={
        "amount": 1.00
    }, headers=auth_headers_user2)
    assert update_res.status_code == status.HTTP_404_NOT_FOUND

    # User 2 tries to DELETE User 1's transaction
    delete_res = client.delete(f"/api/v1/transactions/{tx_id}", headers=auth_headers_user2)
    assert delete_res.status_code == status.HTTP_404_NOT_FOUND

    # Verify User 1 can still access their transaction unharmed
    verify_res = client.get(f"/api/v1/transactions/{tx_id}", headers=auth_headers)
    assert verify_res.status_code == status.HTTP_200_OK
    assert float(verify_res.json()["amount"]) == 99.99
