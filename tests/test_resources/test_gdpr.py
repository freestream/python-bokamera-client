"""Tests for GDPRResource."""

from __future__ import annotations

from datetime import date

import httpx
import respx

from bokamera._client import BokaMeraHTTPClient
from bokamera.resources.gdpr import GDPRResource

BASE = "https://api.bokamera.se"
COMPANY_UUID = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
CUSTOMER_UUID = "11111111-2222-3333-4444-555555555555"


def make_http() -> BokaMeraHTTPClient:
    return BokaMeraHTTPClient(api_key="test-key", base_url=BASE)


# ---------------------------------------------------------------------------
# get_customer_data
# ---------------------------------------------------------------------------


def test_gdpr_get_customer_data():
    with respx.mock:
        route = respx.get(f"{BASE}/gdpr/customers/{CUSTOMER_UUID}").mock(
            return_value=httpx.Response(
                200,
                json={
                    "CustomerId": CUSTOMER_UUID,
                    "Bookings": [{"Id": 1}],
                    "MessageLog": [],
                    "Customer": {"Firstname": "Anna"},
                },
            )
        )
        http = make_http()
        result = GDPRResource(http).get_customer_data(CUSTOMER_UUID, company_id=COMPANY_UUID)
        http.close()
    assert route.called
    assert str(result.customer_id) == CUSTOMER_UUID
    assert len(result.bookings) == 1
    assert result.customer == {"Firstname": "Anna"}


# ---------------------------------------------------------------------------
# list_inactive_customers
# ---------------------------------------------------------------------------


def test_gdpr_list_inactive_customers():
    with respx.mock:
        route = respx.get(f"{BASE}/gdpr/customers/inactive").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "Id": CUSTOMER_UUID,
                        "Firstname": "Bo",
                        "Lastname": "Ek",
                        "Email": "bo@example.com",
                        "LastBooking": "2023-06-01T00:00:00Z",
                    }
                ],
            )
        )
        http = make_http()
        results = GDPRResource(http).list_inactive_customers(
            inactive_since=date(2024, 1, 1),
            company_id=COMPANY_UUID,
        )
        http.close()
    assert route.called
    params = route.calls[0].request.url.params
    assert params["InactiveSince"] == "2024-01-01"
    assert len(results) == 1
    assert results[0].firstname == "Bo"
    assert results[0].email == "bo@example.com"


def test_gdpr_list_inactive_customers_wrapped():
    with respx.mock:
        respx.get(f"{BASE}/gdpr/customers/inactive").mock(
            return_value=httpx.Response(
                200,
                json={"Results": [{"Id": CUSTOMER_UUID, "Firstname": "Karin"}]},
            )
        )
        http = make_http()
        results = GDPRResource(http).list_inactive_customers(
            inactive_since=date(2024, 1, 1),
            company_id=COMPANY_UUID,
        )
        http.close()
    assert results[0].firstname == "Karin"


# ---------------------------------------------------------------------------
# delete_inactive_customers
# ---------------------------------------------------------------------------


def test_gdpr_delete_inactive_customers():
    with respx.mock:
        route = respx.delete(f"{BASE}/gdpr/customers/inactive").mock(
            return_value=httpx.Response(200, json={"Deleted": 3})
        )
        http = make_http()
        result = GDPRResource(http).delete_inactive_customers(
            inactive_since=date(2024, 1, 1),
            company_id=COMPANY_UUID,
        )
        http.close()
    assert route.called
    params = route.calls[0].request.url.params
    assert params["InactiveSince"] == "2024-01-01"
    assert result["Deleted"] == 3
