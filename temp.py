# tests/test_bug_display.py

import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com"
AUTH_URL = f"{BASE_URL}/auth"


@pytest.fixture(scope="session")
def token():
    """Authenticate once and return the token."""
    resp = requests.post(
        AUTH_URL,
        json={"username": "admin", "password": "password123"}
    )
    resp.raise_for_status()
    return resp.json()["token"]


@pytest.fixture
def booking_url():
    return f"{BASE_URL}/booking"


def test_totalprice_precision_display(token, booking_url):
    """
    TC-BUG-01 DISPLAY: Create a booking with a float totalprice,
    then retrieve it and display expected vs actual.
    """
    expected_price = 123.45
    payload = {
        "firstname": "BugTest",
        "lastname":  "Precision",
        "totalprice": expected_price,
        "depositpaid": True,
        "bookingdates": {"checkin": "2025-11-01", "checkout": "2025-11-05"},
        "additionalneeds": "None"
    }
    headers = {"Cookie": f"token={token}"}

    # Create booking
    create_resp = requests.post(booking_url, json=payload, headers=headers)
    assert create_resp.status_code == 200, "Failed to create booking"
    booking_id = create_resp.json()["bookingid"]

    # Retrieve booking
    get_resp = requests.get(f"{booking_url}/{booking_id}")
    assert get_resp.status_code == 200, "Failed to retrieve booking"
    actual_price = get_resp.json()["totalprice"]

    # Display and assert
    print(f"Expected totalprice: {expected_price}, Actual totalprice: {actual_price}")
    assert actual_price == expected_price, (
        f"Total-price precision bug: expected {expected_price}, got {actual_price}"
    )


def test_delete_with_basic_auth(token, booking_url):
    """
    TC-BUG-03: DELETE /booking/{id} should accept Basic auth header
    as an alternative to Cookie, using 'Basic YWRtaW46cGFzc3dvcmQxMjM='.
    """
    # 1) Create a booking to delete
    payload = {
        "firstname": "BasicAuthTest",
        "lastname":  "User",
        "totalprice": 42,
        "depositpaid": False,
        "bookingdates": {"checkin": "2025-12-10", "checkout": "2025-12-12"},
        "additionalneeds": "None"
    }
    headers = {"Cookie": f"token={token}"}
    create_resp = requests.post(booking_url, json=payload, headers=headers)
    assert create_resp.status_code == 200, "Failed to create booking"
    booking_id = create_resp.json()["bookingid"]

    # 2) Attempt delete with Basic Authorization header
    basic_value = "Basic YWRtaW46cGFzc3dvcmQxMjM="
    auth_headers = {"Authorization": basic_value}
    delete_resp = requests.delete(f"{booking_url}/{booking_id}", headers=auth_headers)
    expected = (201, 204)
    actual = delete_resp.status_code

    # Display expected vs. actual
    print(f"Expected DELETE status with Basic auth: {expected}, Actual: {actual}")

    # Assert the API accepts Basic auth for DELETE
    assert actual in expected, (
        f"DELETE with Basic auth failed: expected {expected}, got {actual}")