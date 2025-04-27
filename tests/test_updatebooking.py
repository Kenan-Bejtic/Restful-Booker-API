import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com"

@pytest.fixture
def booking_url():
    return f"{BASE_URL}/booking"

def create_booking(token, booking_url):
    payload = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 100,
        "depositpaid": False,
        "bookingdates": {"checkin": "2025-05-20", "checkout": "2025-05-25"},
        "additionalneeds": "None"
    }
    headers = {"Cookie": f"token={token}"}
    resp = requests.post(booking_url, json=payload, headers=headers)
    assert resp.status_code == 200, f"Booking creation failed: {resp.status_code}"
    data = resp.json()
    return data["bookingid"], payload

def test_full_update_put_valid(token, booking_url):
    """
    TC-UP-01: Full update (PUT) (valid)
    """
    booking_id, _ = create_booking(token, booking_url)

    new_payload = {
        "firstname": "Updated",
        "lastname": "Customer",
        "totalprice": 250,
        "depositpaid": True,
        "bookingdates": {"checkin": "2025-06-01", "checkout": "2025-06-10"},
        "additionalneeds": "Breakfast"
    }
    headers = {"Cookie": f"token={token}"}
    resp = requests.put(f"{booking_url}/{booking_id}", json=new_payload, headers=headers)
    assert resp.status_code == 200, f"Expected 200 OK on PUT, got {resp.status_code}"
    data = resp.json()
    assert data == new_payload, f"PUT response mismatch: expected {new_payload}, got {data}"

def test_partial_update_patch_valid(token, booking_url):
    """
    TC-UP-02: Partial update (PATCH) (valid)
    """
    booking_id, original = create_booking(token, booking_url)

    patch_payload = {"firstname": "PatchedName", "additionalneeds": "Late Checkout"}
    headers = {"Cookie": f"token={token}"}
    resp = requests.patch(f"{booking_url}/{booking_id}", json=patch_payload, headers=headers)
    assert resp.status_code == 200, f"Expected 200 OK on PATCH, got {resp.status_code}"
    data = resp.json()
    
    for key, value in patch_payload.items():
        assert data[key] == value, f"PATCH field '{key}' not updated correctly"
    for key, value in original.items():
        if key not in patch_payload:
            assert data[key] == value, f"Field '{key}' should remain '{value}', got '{data[key]}'"

def test_unauthorized_update_patch(token, booking_url):
    """
    TC-UP-03: Unauthorized update
    """
    booking_id, _ = create_booking(token, booking_url)

    patch_payload = {"lastname": "Hacker"}
    resp = requests.patch(f"{booking_url}/{booking_id}", json=patch_payload) 
    assert resp.status_code == 403, f"Expected 403 Forbidden for unauthorized PATCH, got {resp.status_code}"
