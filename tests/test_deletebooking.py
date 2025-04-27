import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com"

@pytest.fixture
def booking_url():
    return f"{BASE_URL}/booking"

def create_booking(token, booking_url):
    payload = {
        "firstname": "Temp",
        "lastname": "User",
        "totalprice": 99,
        "depositpaid": False,
        "bookingdates": {"checkin": "2025-07-01", "checkout": "2025-07-03"},
        "additionalneeds": "None"
    }
    headers = {"Cookie": f"token={token}"}
    resp = requests.post(booking_url, json=payload, headers=headers)
    assert resp.status_code == 200, f"Booking creation failed: {resp.status_code}"
    return resp.json()["bookingid"]

def test_delete_existing_booking(token, booking_url):
    """
    TC-DEL-01: Delete existing booking (valid)
    """
    booking_id = create_booking(token, booking_url)

    resp = requests.delete(f"{booking_url}/{booking_id}", headers={"Cookie": f"token={token}"})
    assert resp.status_code in (201, 204), \
        f"Expected 201 or 204 on DELETE, got {resp.status_code}"

    
    get_resp = requests.get(f"{booking_url}/{booking_id}")
    assert get_resp.status_code == 404, \
        f"Expected 404 after delete, got {get_resp.status_code}"

def test_delete_nonexistent_booking(token, booking_url):
    """
    TC-DEL-02: Delete non-existent booking
    """
    resp = requests.delete(f"{booking_url}/999999", headers={"Cookie": f"token={token}"})
    assert resp.status_code in (404, 405), \
        f"Expected 404 or 405 for non-existent delete, got {resp.status_code}"




def test_delete_with_basic_auth(token, booking_url):
    """
    TC-DEL-03: Delete existing booking using basic authorization header 
    """
   
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

    
    basic_value = "Basic YWRtaW46cGFzc3dvcmQxMjM="
    auth_headers = {"Authorization": basic_value}
    delete_resp = requests.delete(f"{booking_url}/{booking_id}", headers=auth_headers)
    expected = (201, 204)
    actual = delete_resp.status_code


    print(f"Expected DELETE status with Basic auth: {expected}, Actual: {actual}")
    assert actual in expected, (
        f"DELETE with Basic auth failed: expected {expected}, got {actual}")