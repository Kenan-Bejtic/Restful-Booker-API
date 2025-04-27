import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com"

@pytest.fixture(scope="session")
def token():
    resp = requests.post(
        f"{BASE_URL}/auth",
        json={"username": "admin", "password": "password123"}
    )
    assert resp.status_code == 200, f"Auth failed: {resp.status_code}"
    data = resp.json()
    assert "token" in data and data["token"].strip(), "Missing token in auth response"
    return data["token"]

@pytest.fixture
def booking_url():
    return f"{BASE_URL}/booking"
