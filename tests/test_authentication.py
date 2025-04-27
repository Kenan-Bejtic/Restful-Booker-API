import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com"

@pytest.fixture(scope="session")
def auth_url():
    return f"{BASE_URL}/auth"

def test_auth_valid_credentials(auth_url):
    """
    TC-Auth-01: Valid credentials
    """
    payload = {
        "username": "admin",
        "password": "password123"
    }
    resp = requests.post(auth_url, json=payload)

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"
    data = resp.json()
    assert "token" in data, "Response JSON must contain a 'token' field"
    assert isinstance(data["token"], str) and data["token"].strip() != "", "Token must be a non-empty string"


@pytest.mark.parametrize("payload", [
    ({"username": "invalid", "password": "password123"}),
    ({"username": "admin",   "password": "wrong"}),
])
def test_auth_invalid_credentials(auth_url, payload):
    """
    TC-Auth-02: Invalid credentials
    """
    resp = requests.post(auth_url, json=payload)
    
    assert resp.status_code == 200, f"Expected 200 on bad credentials, got {resp.status_code}"

    
    data = resp.json()
   
    assert "reason" in data, f"Expected 'reason' field in response, got {data}"
    assert data["reason"] == "Bad credentials", f"Expected reason='Bad credentials', got '{data['reason']}'"