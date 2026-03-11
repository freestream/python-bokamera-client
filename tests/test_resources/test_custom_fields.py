"""Tests for CustomFieldResource."""

from __future__ import annotations

import json

import httpx
import respx

from bokamera._client import BokaMeraHTTPClient
from bokamera.resources.custom_fields import CustomFieldResource

BASE = "https://api.bokamera.se"
COMPANY_UUID = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"


def make_http() -> BokaMeraHTTPClient:
    return BokaMeraHTTPClient(api_key="test-key", base_url=BASE)


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------


def test_custom_fields_list():
    with respx.mock:
        route = respx.get(f"{BASE}/customfields").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "Id": 1,
                        "Name": "Allergy info",
                        "Datatype": "TextBox",
                        "IsMandatory": False,
                        "Active": True,
                    }
                ],
            )
        )
        http = make_http()
        result = CustomFieldResource(http).list(table="Booking", company_id=COMPANY_UUID)
        http.close()
    assert route.called
    params = route.calls[0].request.url.params
    assert params["Table"] == "Booking"
    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].name == "Allergy info"


def test_custom_fields_list_with_results_wrapper():
    with respx.mock:
        respx.get(f"{BASE}/customfields").mock(
            return_value=httpx.Response(
                200,
                json={"Results": [{"Id": 2, "Name": "Preferences", "Active": True}]},
            )
        )
        http = make_http()
        result = CustomFieldResource(http).list(table="Customer", company_id=COMPANY_UUID)
        http.close()
    assert len(result) == 1
    assert result[0].name == "Preferences"


# ---------------------------------------------------------------------------
# list_validations
# ---------------------------------------------------------------------------


def test_custom_fields_list_validations():
    with respx.mock:
        route = respx.get(f"{BASE}/customfields/validations").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {"Id": 1, "Name": "Email", "RegExCode": r"^[\w]+@[\w]+\.\w+$"},
                    {"Id": 2, "Name": "Phone", "RegExCode": r"^\+?[\d]{8,15}$"},
                ],
            )
        )
        http = make_http()
        result = CustomFieldResource(http).list_validations()
        http.close()
    assert route.called
    assert len(result) == 2
    assert result[0].name == "Email"
    assert result[1].id == 2


def test_custom_fields_list_validations_with_id_filter():
    with respx.mock:
        route = respx.get(f"{BASE}/customfields/validations").mock(
            return_value=httpx.Response(
                200, json=[{"Id": 1, "Name": "Email"}]
            )
        )
        http = make_http()
        result = CustomFieldResource(http).list_validations(id_=1)
        http.close()
    params = route.calls[0].request.url.params
    assert params["Id"] == "1"
    assert result[0].id == 1
