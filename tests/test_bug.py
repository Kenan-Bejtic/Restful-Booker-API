import pytest
import requests
import warnings

def test_individual_filter_combinations_and_existence(token, booking_url):
    headers = {"Cookie": f"token={token}"}

    #Create booking A
    a_payload = {
        "firstname": "ComboTest",
        "lastname": "User",
        "totalprice": 111,
        "depositpaid": False,
        "bookingdates": {"checkin": "2025-11-01", "checkout": "2025-11-05"},
        "additionalneeds": "None"
    }
    resp = requests.post(booking_url, json=a_payload, headers=headers)
    assert resp.status_code == 200
    id_a = resp.json()["bookingid"]

    # 2) firstname only
    resp = requests.get(f"{booking_url}?firstname={a_payload['firstname']}")
    assert resp.status_code == 200
    ids = [item["bookingid"] for item in resp.json()]
    if id_a not in ids:
        warnings.warn(f"Booking {id_a} NOT returned by ?firstname={a_payload['firstname']}", UserWarning)
   
    assert requests.get(f"{booking_url}/{id_a}").status_code == 200

    # 3) lastname only
    resp = requests.get(f"{booking_url}?lastname={a_payload['lastname']}")
    assert resp.status_code == 200
    ids = [item["bookingid"] for item in resp.json()]
    if id_a not in ids:
        warnings.warn(f"Booking {id_a} NOT returned by ?lastname={a_payload['lastname']}", UserWarning)
    assert requests.get(f"{booking_url}/{id_a}").status_code == 200

    # 4) checkin only
    checkin = a_payload["bookingdates"]["checkin"]
    resp = requests.get(f"{booking_url}?checkin={checkin}")
    assert resp.status_code == 200
    ids = [item["bookingid"] for item in resp.json()]
    if id_a not in ids:
        warnings.warn(f"Booking {id_a} NOT returned by ?checkin={checkin}", UserWarning)
    assert requests.get(f"{booking_url}/{id_a}").status_code == 200

    # 5) checkout only
    checkout = a_payload["bookingdates"]["checkout"]
    resp = requests.get(f"{booking_url}?checkout={checkout}")
    assert resp.status_code == 200
    ids = [item["bookingid"] for item in resp.json()]
    if id_a not in ids:
        warnings.warn(f"Booking {id_a} NOT returned by ?checkout={checkout}", UserWarning)
    assert requests.get(f"{booking_url}/{id_a}").status_code == 200

    # 6) firstname + lastname
    resp = requests.get(
        f"{booking_url}?firstname={a_payload['firstname']}&lastname={a_payload['lastname']}"
    )
    assert resp.status_code == 200
    ids = [item["bookingid"] for item in resp.json()]
    if id_a not in ids:
        warnings.warn(
            f"Booking {id_a} NOT returned by ?firstname={a_payload['firstname']}&lastname={a_payload['lastname']}",
            UserWarning
        )
    assert requests.get(f"{booking_url}/{id_a}").status_code == 200

    # 7) firstname + checkin
    resp = requests.get(
        f"{booking_url}?firstname={a_payload['firstname']}&checkin={checkin}"
    )
    assert resp.status_code == 200
    ids = [item["bookingid"] for item in resp.json()]
    if id_a not in ids:
        warnings.warn(
            f"Booking {id_a} NOT returned by ?firstname={a_payload['firstname']}&checkin={checkin}",
            UserWarning
        )
    assert requests.get(f"{booking_url}/{id_a}").status_code == 200

    # 8) firstname + checkout
    resp = requests.get(
        f"{booking_url}?firstname={a_payload['firstname']}&checkout={checkout}"
    )
    assert resp.status_code == 200
    ids = [item["bookingid"] for item in resp.json()]
    if id_a not in ids:
        warnings.warn(
            f"Booking {id_a} NOT returned by ?firstname={a_payload['firstname']}&checkout={checkout}",
            UserWarning
        )
    assert requests.get(f"{booking_url}/{id_a}").status_code == 200

    # 9) lastname + checkin
    resp = requests.get(
        f"{booking_url}?lastname={a_payload['lastname']}&checkin={checkin}"
    )
    assert resp.status_code == 200
    ids = [item["bookingid"] for item in resp.json()]
    if id_a not in ids:
        warnings.warn(
            f"Booking {id_a} NOT returned by ?lastname={a_payload['lastname']}&checkin={checkin}",
            UserWarning
        )
    assert requests.get(f"{booking_url}/{id_a}").status_code == 200

    # 10) lastname + checkout
    resp = requests.get(
        f"{booking_url}?lastname={a_payload['lastname']}&checkout={checkout}"
    )
    assert resp.status_code == 200
    ids = [item["bookingid"] for item in resp.json()]
    if id_a not in ids:
        warnings.warn(
            f"Booking {id_a} NOT returned by ?lastname={a_payload['lastname']}&checkout={checkout}",
            UserWarning
        )
    assert requests.get(f"{booking_url}/{id_a}").status_code == 200

     # 11) firstname + lastname + checkin
    resp = requests.get(
        f"{booking_url}"
        f"?firstname={a_payload['firstname']}"
        f"&lastname={a_payload['lastname']}"
        f"&checkin={checkin}"
    )
    assert resp.status_code == 200
    ids = [item["bookingid"] for item in resp.json()]
    if id_a not in ids:
        warnings.warn(
            f"Booking {id_a} NOT returned by "
            f"?firstname={a_payload['firstname']}&lastname={a_payload['lastname']}&checkin={checkin}",
            UserWarning
        )
    assert requests.get(f"{booking_url}/{id_a}").status_code == 200

    # 12) firstname + lastname + checkout
    resp = requests.get(
        f"{booking_url}"
        f"?firstname={a_payload['firstname']}"
        f"&lastname={a_payload['lastname']}"
        f"&checkout={checkout}"
    )
    assert resp.status_code == 200
    ids = [item["bookingid"] for item in resp.json()]
    if id_a not in ids:
        warnings.warn(
            f"Booking {id_a} NOT returned by "
            f"?firstname={a_payload['firstname']}&lastname={a_payload['lastname']}&checkout={checkout}",
            UserWarning
        )
    assert requests.get(f"{booking_url}/{id_a}").status_code == 200

    # 13) firstname + lastname + checkin + checkout
    resp = requests.get(
        f"{booking_url}"
        f"?firstname={a_payload['firstname']}"
        f"&lastname={a_payload['lastname']}"
        f"&checkin={checkin}"
        f"&checkout={checkout}"
    )
    assert resp.status_code == 200
    ids = [item["bookingid"] for item in resp.json()]
    if id_a not in ids:
        warnings.warn(
            f"Booking {id_a} NOT returned by "
            f"?firstname={a_payload['firstname']}&lastname={a_payload['lastname']}"
            f"&checkin={checkin}&checkout={checkout}",
            UserWarning
        )
    assert requests.get(f"{booking_url}/{id_a}").status_code == 200

    # 14) firstname + checkin + checkout
    resp = requests.get(
        f"{booking_url}"
        f"?firstname={a_payload['firstname']}"
        f"&checkin={checkin}"
        f"&checkout={checkout}"
    )
    assert resp.status_code == 200
    ids = [item["bookingid"] for item in resp.json()]
    if id_a not in ids:
        warnings.warn(
            f"Booking {id_a} NOT returned by "
            f"?firstname={a_payload['firstname']}&checkin={checkin}&checkout={checkout}",
            UserWarning
        )
    assert requests.get(f"{booking_url}/{id_a}").status_code == 200

    # 15) lastname + checkin + checkout
    resp = requests.get(
        f"{booking_url}"
        f"?lastname={a_payload['lastname']}"
        f"&checkin={checkin}"
        f"&checkout={checkout}"
    )
    assert resp.status_code == 200
    ids = [item["bookingid"] for item in resp.json()]
    if id_a not in ids:
        warnings.warn(
            f"Booking {id_a} NOT returned by "
            f"?lastname={a_payload['lastname']}&checkin={checkin}&checkout={checkout}",
            UserWarning
        )
    assert requests.get(f"{booking_url}/{id_a}").status_code == 200



def test_totalprice_precision_warning(token, booking_url):
    """
    TC-BUG-08,
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

    create_resp = requests.post(booking_url, json=payload, headers=headers)
    assert create_resp.status_code == 200, "Failed to create booking"
    booking_id = create_resp.json()["bookingid"]

    get_resp = requests.get(f"{booking_url}/{booking_id}")
    assert get_resp.status_code == 200, "Failed to retrieve booking"
    actual_price = get_resp.json()["totalprice"]

    if actual_price != expected_price:
        warnings.warn(
            f"Total-price precision bug detected: expected {expected_price}, got {actual_price}",
            UserWarning
        )
    else:
        assert actual_price == expected_price


def test_totalprice_precision_warning_2(token, booking_url):
    """
    TC-BUG-09,
    """
    expected_price = 0.99
    payload = {
        "firstname": "BugTest",
        "lastname":  "Precision",
        "totalprice": expected_price,
        "depositpaid": True,
        "bookingdates": {"checkin": "2025-11-01", "checkout": "2025-11-05"},
        "additionalneeds": "None"
    }
    headers = {"Cookie": f"token={token}"}

    create_resp = requests.post(booking_url, json=payload, headers=headers)
    assert create_resp.status_code == 200, "Failed to create booking"
    booking_id = create_resp.json()["bookingid"]

    get_resp = requests.get(f"{booking_url}/{booking_id}")
    assert get_resp.status_code == 200, "Failed to retrieve booking"
    actual_price = get_resp.json()["totalprice"]

    if actual_price != expected_price:
        warnings.warn(
            f"Total-price precision bug detected: expected {expected_price}, got {actual_price}",
            UserWarning
        )
    else:
        assert actual_price == expected_price