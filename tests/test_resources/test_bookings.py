"""Tests for BookingResource."""

from __future__ import annotations

import json
from datetime import datetime, timezone

import httpx
import respx

from bokamera._client import BokaMeraHTTPClient
from bokamera.resources.bookings import BookingResource

BASE = "https://api.bokamera.se"
COMPANY_UUID = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"


def make_http() -> BokaMeraHTTPClient:
    return BokaMeraHTTPClient(api_key="test-key", base_url=BASE)


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------


def test_bookings_list_returns_query_response():
    with respx.mock:
        route = respx.get(f"{BASE}/bookings").mock(
            return_value=httpx.Response(
                200,
                json={
                    "Results": [
                        {
                            "Id": 100,
                            "CompanyId": COMPANY_UUID,
                            "Service": {"Id": 5, "Name": "Haircut"},
                        }
                    ],
                    "Total": 1,
                    "Offset": 0,
                },
            )
        )
        http = make_http()
        result = BookingResource(http).list()
        http.close()
    assert route.called
    assert result.total == 1
    assert result.offset == 0
    assert len(result.results) == 1
    assert result.results[0].id == 100
    assert result.results[0].service_name == "Haircut"


def test_bookings_list_empty():
    with respx.mock:
        respx.get(f"{BASE}/bookings").mock(
            return_value=httpx.Response(
                200, json={"Results": [], "Total": 0, "Offset": 0}
            )
        )
        http = make_http()
        result = BookingResource(http).list()
        http.close()
    assert result.total == 0
    assert result.results == []


# ---------------------------------------------------------------------------
# create
# ---------------------------------------------------------------------------


def test_bookings_create():
    from_ = datetime(2026, 3, 15, 10, 0, 0, tzinfo=timezone.utc)
    to = datetime(2026, 3, 15, 11, 0, 0, tzinfo=timezone.utc)
    with respx.mock:
        route = respx.post(f"{BASE}/bookings").mock(
            return_value=httpx.Response(
                200,
                json={
                    "Id": 200,
                    "ServiceId": 3,
                    "From": "2026-03-15T10:00:00Z",
                    "To": "2026-03-15T11:00:00Z",
                },
            )
        )
        http = make_http()
        result = BookingResource(http).create(
            from_=from_,
            to=to,
            service_id=3,
            customer={"Firstname": "Eva", "Lastname": "Larsson", "Email": "eva@example.com"},
        )
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["ServiceId"] == 3
    assert "From" in body
    assert "To" in body
    assert body["Customer"]["Firstname"] == "Eva"
    assert result.id == 200


# ---------------------------------------------------------------------------
# update
# ---------------------------------------------------------------------------


def test_bookings_update():
    with respx.mock:
        route = respx.put(f"{BASE}/bookings/55").mock(
            return_value=httpx.Response(
                200,
                json={"Id": 55, "ServiceId": 3},
            )
        )
        http = make_http()
        result = BookingResource(http).update(55, unbooked_comments="Changed by admin")
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["UnbookedComments"] == "Changed by admin"
    assert result.id == 55


# ---------------------------------------------------------------------------
# delete
# ---------------------------------------------------------------------------


def test_bookings_delete():
    with respx.mock:
        route = respx.delete(f"{BASE}/bookings/77").mock(
            return_value=httpx.Response(
                200,
                json={"Id": 77, "ServiceId": 3},
            )
        )
        http = make_http()
        result = BookingResource(http).delete(77, unbooked_comments="Cancelled by customer")
        http.close()
    assert route.called
    params = route.calls[0].request.url.params
    assert params["UnBookedComments"] == "Cancelled by customer"
    assert result.id == 77
