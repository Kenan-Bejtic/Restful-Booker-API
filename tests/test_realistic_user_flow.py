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

def test_full_lifecycle_booking_flow(token, booking_url):
    """
    TC-E2E-01: Full-Lifecycle Booking Flow
    """
    headers = {"Cookie": f"token={token}"}

    # Step 1: Create
    original = {
        "firstname": "E2E",
        "lastname": "Tester",
        "totalprice": 123,
        "depositpaid": True,
        "bookingdates": {"checkin": "2025-09-01", "checkout": "2025-09-05"},
        "additionalneeds": "Breakfast"
    }
    resp = requests.post(booking_url, json=original, headers=headers)
    assert resp.status_code == 200
    booking_id = resp.json()["bookingid"]

    # Step 2: Verify Create
    resp = requests.get(f"{booking_url}/{booking_id}")
    assert resp.status_code == 200
    retrieved = resp.json()
    assert retrieved == original

    # Step 3: Full Replace
    replacement = {
        "firstname": "Replaced",
        "lastname": "Customer",
        "totalprice": 999,
        "depositpaid": False,
        "bookingdates": {"checkin": "2025-10-01", "checkout": "2025-10-10"},
        "additionalneeds": "Dinner"
    }
    resp = requests.put(f"{booking_url}/{booking_id}", json=replacement, headers=headers)
    assert resp.status_code == 200

    # Step 4: Verify Replace
    resp = requests.get(f"{booking_url}/{booking_id}")
    assert resp.status_code == 200
    assert resp.json() == replacement

    # Step 5: Partial Update
    patch = {"firstname": "PatchedE2E"}
    resp = requests.patch(f"{booking_url}/{booking_id}", json=patch, headers=headers)
    assert resp.status_code == 200

    # Step 6: Verify Patch
    resp = requests.get(f"{booking_url}/{booking_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["firstname"] == patch["firstname"]
    for k, v in replacement.items():
        if k != "firstname":
            assert data[k] == v

    # Step 7: Delete
    resp = requests.delete(f"{booking_url}/{booking_id}", headers=headers)
    assert resp.status_code in (201, 204)

    # Step 8: Verify Delete
    resp = requests.get(f"{booking_url}/{booking_id}")
    assert resp.status_code == 404

