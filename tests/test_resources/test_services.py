"""Tests for ServiceResource."""

from __future__ import annotations

import json

import httpx
import respx

from bokamera._client import BokaMeraHTTPClient
from bokamera.resources.services import ServiceResource

BASE = "https://api.bokamera.se"


def make_http() -> BokaMeraHTTPClient:
    return BokaMeraHTTPClient(api_key="test-key", base_url=BASE)


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------


def test_services_list_no_args():
    with respx.mock:
        route = respx.get(f"{BASE}/services").mock(
            return_value=httpx.Response(200, json=[{"Id": 1, "Name": "Yoga"}])
        )
        http = make_http()
        result = ServiceResource(http).list()
        http.close()
    assert route.called
    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].name == "Yoga"


def test_services_list_with_id_filter():
    with respx.mock:
        route = respx.get(f"{BASE}/services").mock(
            return_value=httpx.Response(200, json=[])
        )
        http = make_http()
        ServiceResource(http).list(id_=42)
        http.close()
    assert route.called
    assert route.calls[0].request.url.params["Id"] == "42"


def test_services_list_with_results_wrapper():
    with respx.mock:
        respx.get(f"{BASE}/services").mock(
            return_value=httpx.Response(
                200, json={"Results": [{"Id": 2, "Name": "Pilates"}]}
            )
        )
        http = make_http()
        result = ServiceResource(http).list()
        http.close()
    assert len(result) == 1
    assert result[0].name == "Pilates"


# ---------------------------------------------------------------------------
# create
# ---------------------------------------------------------------------------


def test_services_create():
    with respx.mock:
        route = respx.post(f"{BASE}/services").mock(
            return_value=httpx.Response(200, json={"Id": 1, "Name": "Yoga"})
        )
        http = make_http()
        result = ServiceResource(http).create(name="Yoga")
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["Name"] == "Yoga"
    assert result.name == "Yoga"
    assert result.id == 1


def test_services_create_with_options():
    with respx.mock:
        route = respx.post(f"{BASE}/services").mock(
            return_value=httpx.Response(200, json={"Id": 5, "Name": "Massage", "Duration": 90})
        )
        http = make_http()
        result = ServiceResource(http).create(
            name="Massage",
            duration=90,
            total_spots=5,
            is_payment_enabled=True,
        )
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["Name"] == "Massage"
    assert body["Duration"] == 90
    assert body["TotalSpots"] == 5
    assert body["IsPaymentEnabled"] is True
    assert result.id == 5


# ---------------------------------------------------------------------------
# update
# ---------------------------------------------------------------------------


def test_services_update():
    with respx.mock:
        route = respx.put(f"{BASE}/services/7").mock(
            return_value=httpx.Response(200, json={"Id": 7, "Name": "Hot Yoga"})
        )
        http = make_http()
        result = ServiceResource(http).update(7, name="Hot Yoga")
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["Name"] == "Hot Yoga"
    assert result.id == 7
    assert result.name == "Hot Yoga"


# ---------------------------------------------------------------------------
# delete
# ---------------------------------------------------------------------------


def test_services_delete():
    with respx.mock:
        route = respx.delete(f"{BASE}/services/3").mock(
            return_value=httpx.Response(200, json={"Id": 3, "Name": "Old Service"})
        )
        http = make_http()
        result = ServiceResource(http).delete(3)
        http.close()
    assert route.called
    assert result.id == 3


# ---------------------------------------------------------------------------
# list_duration_types
# ---------------------------------------------------------------------------


def test_services_list_duration_types():
    with respx.mock:
        respx.get(f"{BASE}/services/durationtypes").mock(
            return_value=httpx.Response(200, json=[{"Id": 1, "Name": "Fixed"}])
        )
        http = make_http()
        result = ServiceResource(http).list_duration_types()
        http.close()
    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].name == "Fixed"


def test_services_list_duration_types_results_wrapper():
    with respx.mock:
        respx.get(f"{BASE}/services/durationtypes").mock(
            return_value=httpx.Response(
                200, json={"Results": [{"Id": 2, "Name": "Variable"}]}
            )
        )
        http = make_http()
        result = ServiceResource(http).list_duration_types()
        http.close()
    assert len(result) == 1
    assert result[0].name == "Variable"


# ---------------------------------------------------------------------------
# calculate_price
# ---------------------------------------------------------------------------


def test_services_calculate_price():
    with respx.mock:
        route = respx.put(f"{BASE}/services/10/calculateprice").mock(
            return_value=httpx.Response(
                200, json={"Price": 450.0, "VAT": 112.5, "PriceBeforeRebate": 500.0}
            )
        )
        http = make_http()
        result = ServiceResource(http).calculate_price(
            10,
            rebate_code_ids=[1],
        )
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["RebateCodeIds"] == [1]
    assert result.price == 450.0
    assert result.vat == 112.5
    assert result.price_before_rebate == 500.0
