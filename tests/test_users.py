import pytest
from fastapi.testclient import TestClient

def test_add_user_valid(test_client: TestClient):
    response = test_client.post("/users/add_user", json={
        "first_name": "John",
        "last_name": "Doe",
        "birthday": "1985-05-20",
        "employee_number": 123457
    })
    assert response.status_code == 200
    assert response.json() == {"message": "User added successfully"}

@pytest.mark.parametrize("data, expected_status, expected_detail", [
    ({"first_name": "", "last_name": "Doe", "birthday": "1985-05-20"}, 422, "Field required"),
    ({"first_name": "John@", "last_name": "Doe", "birthday": "1985-05-20"}, 422, "Invalid character"),
    ({"first_name": "John123", "last_name": "Doe", "birthday": "1985-05-20"}, 422, "Invalid character"),
    ({"first_name": "John", "last_name": "", "birthday": "1985-05-20"}, 422, "Field required"),
    ({"first_name": "John", "last_name": "Doe@", "birthday": "1985-05-20"}, 422, "Invalid character"),
    ({"first_name": "John", "last_name": "Doe123", "birthday": "1985-05-20"}, 422, "Invalid character"),
    ({"first_name": "John", "last_name": "Doe", "birthday": "05/20/1985"}, 422, "Invalid birthday format"),
    ({"first_name": "John", "last_name": "Doe", "birthday": "2100-05-20"}, 422, "Birthday cannot be in the future"),
    ({"first_name": "John", "last_name": "Doe", "birthday": "1800-01-01"}, 422, "Birthday cannot be before January 1, 1920"),
    ({"first_name": "John", "last_name": "Doe", "birthday": "1985-05-20", "employee_number": "001122"}, 422, "Employee number must not contain leading zeros"),
    ({"first_name": "John", "last_name": "Doe", "birthday": "1985-05-20", "employee_number": -12345}, 422, "Employee number must not be negative"),
    ({"first_name": "John", "last_name": "Doe", "birthday": "1985-05-20", "employee_number": "abc123"}, 422, "Invalid employee number"),
])
def test_add_user_invalid(test_client: TestClient, data, expected_status, expected_detail):
    response = test_client.post("/users/add_user", json=data)
    assert response.status_code == expected_status
    assert expected_detail in response.json()["detail"]

def test_get_users_empty(test_client: TestClient):
    response = test_client.get("/users/get_users")
    assert response.status_code == 200
    assert response.json() == []

def test_get_users_non_empty(test_client: TestClient):
    test_client.post("/users/add_user", json={
        "first_name": "John",
        "last_name": "Doe",
        "birthday": "1985-05-20",
        "employee_number": 123457
    })
    response = test_client.get("/users/get_users")
    assert response.status_code == 200
    assert len(response.json()) > 0
    for user in response.json():
        assert len(user["employee_number"]) == 6  # Check zero-padding
