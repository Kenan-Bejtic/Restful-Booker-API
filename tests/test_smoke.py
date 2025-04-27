import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com"

@pytest.fixture(scope="session")
def ping_url():
    return f"{BASE_URL}/ping"

@pytest.fixture(scope="session")
def auth_url():
    return f"{BASE_URL}/auth"

@pytest.fixture(scope="session")
def booking_url():
    return f"{BASE_URL}/booking"

def login():
    resp = requests.post(
        f"{BASE_URL}/auth",
        json={"username": "admin", "password": "password123"}
    )
    assert resp.status_code == 200, f"Auth failed: {resp.status_code}"
    data = resp.json()
    token = data.get("token")
    assert token and token.strip(), "Auth response missing token"
    return token

def test_tc_sm_01_health_check_and_auth(ping_url, auth_url):
    """
    TC-SM-01: Health Check & Authentication
    """
    resp_ping = requests.get(ping_url)
    assert resp_ping.status_code == 201, f"Expected 201 from /ping, got {resp_ping.status_code}"

    resp_auth = requests.post(auth_url, json={"username": "admin", "password": "password123"})
    assert resp_auth.status_code == 200, f"Expected 200 from /auth, got {resp_auth.status_code}"
    auth_data = resp_auth.json()
    assert "token" in auth_data and auth_data["token"].strip(), "Auth response missing non-empty token"

def test_tc_sm_02_create_retrieve_delete_booking(booking_url):
    """
    TC-SM-02: Create, Retrieve, and Delete Booking
    """
    token = login()
    headers = {"Cookie": f"token={token}"}
    payload = {
        "firstname": "Smoke",
        "lastname": "Test",
        "totalprice": 50,
        "depositpaid": False,
        "bookingdates": {"checkin": "2025-08-01", "checkout": "2025-08-02"},
        "additionalneeds": "None"
    }

    # Create
    resp_create = requests.post(booking_url, json=payload, headers=headers)
    assert resp_create.status_code == 200, f"Expected 200 on booking create, got {resp_create.status_code}"
    create_data = resp_create.json()
    assert "bookingid" in create_data, "Create response missing 'bookingid'"
    booking_id = create_data["bookingid"]

    # Retrieve
    resp_get = requests.get(f"{booking_url}/{booking_id}")
    assert resp_get.status_code == 200, f"Expected 200 on booking get, got {resp_get.status_code}"
    retrieved = resp_get.json()
    for field, value in payload.items():
        assert retrieved[field] == value, f"Mismatch on '{field}': expected {value}, got {retrieved[field]}"

    # Delete
    resp_delete = requests.delete(f"{booking_url}/{booking_id}", headers=headers)
    assert resp_delete.status_code in (201, 204), f"Expected 201/204 on delete, got {resp_delete.status_code}"

    # Confirm Deletion
    resp_get2 = requests.get(f"{booking_url}/{booking_id}")
    assert resp_get2.status_code == 404, f"Expected 404 after deletion, got {resp_get2.status_code}"

def test_tc_sm_03_list_bookings_basic(booking_url):
    """
    TC-SM-03: List Bookings (Basic)
    """
    resp = requests.get(booking_url)
    assert resp.status_code == 200, f"Expected 200 on list bookings, got {resp.status_code}"
    data = resp.json()
    assert isinstance(data, list), f"Expected list of IDs, got {type(data)}"
