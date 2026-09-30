from fastapi import status


def test_get_categories_includes_defaults(client, auth_headers):
    response = client.get("/api/v1/categories", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    categories = response.json()
    assert len(categories) > 0
    names = [c["name"] for c in categories]
    assert "Salary" in names
    assert "Groceries" in names


def test_create_custom_category(client, auth_headers):
    payload = {
        "name": "Crypto Trading",
        "type": "INCOME",
        "color": "#f59e0b"
    }
    response = client.post("/api/v1/categories", json=payload, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Crypto Trading"
    assert data["type"] == "INCOME"
    assert data["color"] == "#f59e0b"
    assert data["is_default"] is False


def test_cannot_delete_system_default_category(client, auth_headers):
    res = client.get("/api/v1/categories", headers=auth_headers)
    salary_cat = next(c for c in res.json() if c["name"] == "Salary")
    del_res = client.delete(f"/api/v1/categories/{salary_cat['id']}", headers=auth_headers)
    assert del_res.status_code == status.HTTP_403_FORBIDDEN
