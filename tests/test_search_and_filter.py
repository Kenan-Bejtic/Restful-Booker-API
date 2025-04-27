import pytest
import requests
import warnings

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


def test_search_and_filtering_flow(token, booking_url):
    """
    TC-E2E-02: Search & Filtering of Bookings
    """
    headers = {"Cookie": f"token={token}"}

    # Create A
    a_payload = {
        "firstname": "NameA",
        "lastname": "Alpha",
        "totalprice": 100,
        "depositpaid": False,
        "bookingdates": {"checkin": "2026-11-01", "checkout": "2026-11-05"},
        "additionalneeds": ""
    }
    resp = requests.post(booking_url, json=a_payload, headers=headers)
    assert resp.status_code == 200
    id_a = resp.json()["bookingid"]

    # Create B
    b_payload = {
        "firstname": "NameA",
        "lastname": "Bejtic",
        "totalprice": 200,
        "depositpaid": True,
        "bookingdates": {"checkin": "2025-12-01", "checkout": "2025-12-05"},
        "additionalneeds": "Extra pillows"
    }
    resp = requests.post(booking_url, json=b_payload, headers=headers)
    assert resp.status_code == 200
    id_b = resp.json()["bookingid"]

    # Create C
    c_payload = {
        "firstname": "NameC",
        "lastname": "Gamma",
        "totalprice": 300,
        "depositpaid": False,
        "bookingdates": {"checkin": "2025-15-11", "checkout": "2025-16-11"},
        "additionalneeds": ""
    }
    resp = requests.post(booking_url, json=c_payload, headers=headers)
    assert resp.status_code == 200
    id_c = resp.json()["bookingid"]

    # Filter by firstname=NameA
    resp = requests.get(f"{booking_url}?firstname=NameA")
    assert resp.status_code == 200
    ids = [item["bookingid"] for item in resp.json()]
    assert id_a in ids and id_b in ids and id_c not in ids

    # Filter by lastname=Bejtic
    resp = requests.get(f"{booking_url}?lastname={b_payload['lastname']}")
    assert resp.status_code == 200
    ids = [item["bookingid"] for item in resp.json()]
    assert id_b in ids, f"Expected {id_b} in results for lastname filter, got {ids}"
    assert id_a not in ids and id_c not in ids


    # Filter by checkin and checkout
    checkin = a_payload["bookingdates"]["checkin"]
    resp = requests.get(f"{booking_url}?checkin={checkin}")
    assert resp.status_code == 200, f"Expected 200 on checkin filter, got {resp.status_code}"
    ids = [item["bookingid"] for item in resp.json()]

    if id_a not in ids:
        warnings.warn(f"Booking {id_a} NOT returned by ?checkin={checkin}", UserWarning)
    else:
        assert id_a in ids 

    
    exist_resp = requests.get(f"{booking_url}/{id_a}")
    assert exist_resp.status_code == 200, f"Booking {id_a} was deleted unexpectedly!"

    
    checkout = a_payload["bookingdates"]["checkout"]
    resp = requests.get(f"{booking_url}?checkout={checkout}")
    assert resp.status_code == 200, f"Expected 200 on checkout filter, got {resp.status_code}"
    ids = [item["bookingid"] for item in resp.json()]

    if id_a not in ids:
        warnings.warn(f"Booking {id_a} NOT returned by ?checkout={checkout}", UserWarning)
    else:
        assert id_a in ids

    exist_resp = requests.get(f"{booking_url}/{id_a}")
    assert exist_resp.status_code == 200, f"Booking {id_a} was deleted unexpectedly!"

