import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com"

@pytest.fixture(scope="session")
def auth_url():
    return f"{BASE_URL}/auth"

@pytest.fixture(scope="session")
def token(auth_url):
    creds = {"username": "admin", "password": "password123"}
    resp = requests.post(auth_url, json=creds)
    assert resp.status_code == 200, f"Failed to authenticate: {resp.status_code}"
    data = resp.json()
    assert "token" in data and data["token"], "Token not found in auth response"
    return data["token"]

@pytest.fixture
def booking_url():
    return f"{BASE_URL}/booking"

def test_create_booking_valid(token, booking_url):
    """
    TC-CR-01: Create booking (valid)
    """
    payload = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-05-01",
            "checkout": "2025-05-05"
        },
        "additionalneeds": "Breakfast"
    }
    headers = {"Cookie": f"token={token}"}
    resp = requests.post(booking_url, json=payload, headers=headers)

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"
    data = resp.json()
    assert "bookingid" in data, "Response JSON missing 'bookingid'"
    assert "booking" in data, "Response JSON missing 'booking' object"

    booking = data["booking"]
    
    assert booking["firstname"] == payload["firstname"]
    assert booking["lastname"] == payload["lastname"]
    assert booking["totalprice"] == payload["totalprice"]
    assert booking["depositpaid"] == payload["depositpaid"]
    assert booking["bookingdates"] == payload["bookingdates"]
    assert booking["additionalneeds"] == payload["additionalneeds"]



@pytest.mark.parametrize("payload, missing_field", [
    (
        {
            "lastname": "Doe",
            "totalprice": 100,
            "depositpaid": False,
            "bookingdates": {"checkin": "2025-06-01", "checkout": "2025-06-03"},
            "additionalneeds": "Lunch"
        },
        "firstname"
    ),
])

def test_create_booking_missing_data(payload, missing_field, booking_url):
    """
    TC-CR-02: Create booking (missing data)
    """
    resp = requests.post(booking_url, json=payload)

    assert resp.status_code == 500, \
        f"Expected 500 Internal Server Error for missing '{missing_field}', got {resp.status_code}"

    
    content_type = resp.headers.get("Content-Type", "")
    if "application/json" in content_type:
        data = resp.json()
        assert data, f"Expected non-empty JSON error, got {data}"
    else:
        assert "Internal Server Error" in resp.text, \
            f"Expected generic server-error text, got: {resp.text!r}"