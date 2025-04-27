import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com"

@pytest.fixture
def booking_url():
    return f"{BASE_URL}/booking"


def test_retrieve_existing_booking_by_id(token, booking_url):
    """
    TC-RD-01: Retrieve existing booking by ID
    """

    payload = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 200,
        "depositpaid": False,
        "bookingdates": {"checkin": "2025-05-10", "checkout": "2025-05-15"},
        "additionalneeds": "Lunch"
    }
    headers = {"Cookie": f"token={token}"}
    create_resp = requests.post(booking_url, json=payload, headers=headers)
    assert create_resp.status_code == 200, f"Booking creation failed: {create_resp.status_code}"
    created = create_resp.json()
    booking_id = created.get("bookingid")
    assert booking_id, "Response JSON missing 'bookingid'"

    get_resp = requests.get(f"{booking_url}/{booking_id}")
    assert get_resp.status_code == 200, f"Expected 200 OK, got {get_resp.status_code}"
    retrieved = get_resp.json()
    
    for field in ["firstname", "lastname", "totalprice", "depositpaid", "additionalneeds"]:
        assert retrieved[field] == payload[field], f"Field '{field}' mismatch: expected {payload[field]}, got {retrieved[field]}"
    assert retrieved["bookingdates"] == payload["bookingdates"], f"Dates mismatch: expected {payload['bookingdates']}, got {retrieved['bookingdates']}"


def test_list_bookings_with_filter_no_match(booking_url):
    """
    TC-RD-02: List bookings with filter (no match)
    """
    resp = requests.get(f"{booking_url}?firstname=NonExistentName")
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"
    data = resp.json()
    assert isinstance(data, list), "Expected JSON array"
    assert data == [], f"Expected empty list, got {data}"


def test_retrieve_nonexistent_booking_id():
    """
    TC-RD-03: Retrieve non-existent booking ID
    """
    resp = requests.get(f"{BASE_URL}/booking/999999")
    assert resp.status_code == 404, f"Expected 404, got {resp.status_code}"