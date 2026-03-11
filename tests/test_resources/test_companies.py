"""Tests for CompanyResource."""

from __future__ import annotations

import httpx
import respx

from bokamera._client import BokaMeraHTTPClient
from bokamera.resources.companies import CompanyResource

BASE = "https://api.bokamera.se"
COMPANY_UUID = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"


def make_http() -> BokaMeraHTTPClient:
    return BokaMeraHTTPClient(api_key="test-key", base_url=BASE)


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------


def test_companies_list_no_filter():
    with respx.mock:
        route = respx.get(f"{BASE}/companies").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "Id": COMPANY_UUID,
                        "Name": "Spa & Wellness",
                        "City": "Stockholm",
                        "CountryId": "SE",
                    }
                ],
            )
        )
        http = make_http()
        result = CompanyResource(http).list()
        http.close()
    assert route.called
    assert len(result) == 1
    assert result[0].name == "Spa & Wellness"
    assert result[0].city == "Stockholm"


def test_companies_list_with_id_filter():
    with respx.mock:
        route = respx.get(f"{BASE}/companies").mock(
            return_value=httpx.Response(200, json=[])
        )
        http = make_http()
        CompanyResource(http).list(id_=COMPANY_UUID)
        http.close()
    params = route.calls[0].request.url.params
    assert params["Id"] == COMPANY_UUID


def test_companies_list_with_results_wrapper():
    with respx.mock:
        respx.get(f"{BASE}/companies").mock(
            return_value=httpx.Response(
                200,
                json={
                    "Results": [
                        {"Id": COMPANY_UUID, "Name": "Wellness Co"}
                    ]
                },
            )
        )
        http = make_http()
        result = CompanyResource(http).list()
        http.close()
    assert len(result) == 1
    assert result[0].name == "Wellness Co"


# ---------------------------------------------------------------------------
# list_roles
# ---------------------------------------------------------------------------


def test_companies_list_roles():
    with respx.mock:
        route = respx.get(f"{BASE}/administrators/roles").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {"Name": "Administrator", "Description": "Full access"},
                    {"Name": "ReadOnly", "Description": "Read only"},
                ],
            )
        )
        http = make_http()
        result = CompanyResource(http).list_roles()
        http.close()
    assert route.called
    assert len(result) == 2
    assert result[0]["Name"] == "Administrator"


def test_companies_list_roles_results_wrapper():
    with respx.mock:
        respx.get(f"{BASE}/administrators/roles").mock(
            return_value=httpx.Response(
                200,
                json={"Results": [{"Name": "Manager"}]},
            )
        )
        http = make_http()
        result = CompanyResource(http).list_roles()
        http.close()
    assert len(result) == 1
    assert result[0]["Name"] == "Manager"
