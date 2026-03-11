"""Tests for RebateCodeResource."""

from __future__ import annotations

import json

import httpx
import respx

from bokamera._client import BokaMeraHTTPClient
from bokamera.resources.rebate_codes import RebateCodeResource

BASE = "https://api.bokamera.se"
COMPANY_UUID = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"


def make_http() -> BokaMeraHTTPClient:
    return BokaMeraHTTPClient(api_key="test-key", base_url=BASE)


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------


def test_rebate_codes_list():
    with respx.mock:
        route = respx.get(f"{BASE}/rebatecodes").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "Id": 1,
                        "CompanyId": COMPANY_UUID,
                        "RebateCodeSign": "SUMMER26",
                        "RebateCodeValue": 20.0,
                        "Active": True,
                    }
                ],
            )
        )
        http = make_http()
        result = RebateCodeResource(http).list()
        http.close()
    assert route.called
    assert len(result) == 1
    assert result[0].rebate_code_sign == "SUMMER26"
    assert result[0].rebate_code_value == 20.0


def test_rebate_codes_list_with_id_filter():
    with respx.mock:
        route = respx.get(f"{BASE}/rebatecodes").mock(
            return_value=httpx.Response(200, json=[])
        )
        http = make_http()
        RebateCodeResource(http).list(id_=5)
        http.close()
    params = route.calls[0].request.url.params
    assert params["Id"] == "5"


# ---------------------------------------------------------------------------
# create
# ---------------------------------------------------------------------------


def test_rebate_codes_create():
    with respx.mock:
        route = respx.post(f"{BASE}/rebatecodes").mock(
            return_value=httpx.Response(
                200,
                json={
                    "Id": 10,
                    "CompanyId": COMPANY_UUID,
                    "RebateCodeSign": "AUTUMN26",
                    "RebateCodeTypeId": 1,
                    "RebateCodeValue": 15.0,
                    "Active": True,
                },
            )
        )
        http = make_http()
        result = RebateCodeResource(http).create(
            rebate_code_type_id=1,
            rebate_code_value=15.0,
            rebate_code_sign="AUTUMN26",
        )
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["RebateCodeTypeId"] == 1
    assert body["RebateCodeValue"] == 15.0
    assert body["RebateCodeSign"] == "AUTUMN26"
    assert result.id == 10
    assert result.rebate_code_sign == "AUTUMN26"


# ---------------------------------------------------------------------------
# list_statuses
# ---------------------------------------------------------------------------


def test_rebate_codes_list_statuses():
    with respx.mock:
        route = respx.get(f"{BASE}/rebatecodes/statuses").mock(
            return_value=httpx.Response(
                200,
                json={
                    "RebateCodeStatusItems": [
                        {"Id": 1, "Name": "Active"},
                        {"Id": 2, "Name": "Expired"},
                    ]
                },
            )
        )
        http = make_http()
        result = RebateCodeResource(http).list_statuses()
        http.close()
    assert route.called
    assert len(result) == 2
    assert result[0].name == "Active"
    assert result[1].name == "Expired"


def test_rebate_codes_list_statuses_with_id():
    with respx.mock:
        route = respx.get(f"{BASE}/rebatecodes/statuses").mock(
            return_value=httpx.Response(
                200, json={"RebateCodeStatusItems": [{"Id": 1, "Name": "Active"}]}
            )
        )
        http = make_http()
        result = RebateCodeResource(http).list_statuses(id_=1)
        http.close()
    params = route.calls[0].request.url.params
    assert params["Id"] == "1"
    assert len(result) == 1


# ---------------------------------------------------------------------------
# list_types
# ---------------------------------------------------------------------------


def test_rebate_codes_list_types():
    with respx.mock:
        route = respx.get(f"{BASE}/rebatecodes/types").mock(
            return_value=httpx.Response(
                200,
                json={
                    "RebateCodeTypeItems": [
                        {"Id": 1, "Name": "Percentage"},
                        {"Id": 2, "Name": "Fixed amount"},
                    ]
                },
            )
        )
        http = make_http()
        result = RebateCodeResource(http).list_types()
        http.close()
    assert len(result) == 2
    assert result[0].name == "Percentage"


def test_rebate_codes_list_types_with_id():
    with respx.mock:
        route = respx.get(f"{BASE}/rebatecodes/types").mock(
            return_value=httpx.Response(
                200,
                json={"RebateCodeTypeItems": [{"Id": 2, "Name": "Fixed amount"}]},
            )
        )
        http = make_http()
        result = RebateCodeResource(http).list_types(id_=2)
        http.close()
    params = route.calls[0].request.url.params
    assert params["Id"] == "2"
    assert result[0].id == 2
