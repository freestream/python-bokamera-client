"""Tests for SystemResource."""

from __future__ import annotations

import httpx
import respx

from bokamera._client import BokaMeraHTTPClient
from bokamera.resources.system import SystemResource

BASE = "https://api.bokamera.se"
COMPANY_UUID = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"


def make_http() -> BokaMeraHTTPClient:
    return BokaMeraHTTPClient(api_key="test-key", base_url=BASE)


# ---------------------------------------------------------------------------
# list_categories
# ---------------------------------------------------------------------------


def test_system_list_categories_no_filter():
    with respx.mock:
        route = respx.get(f"{BASE}/categories").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {"Id": 1, "Name": "Health & Beauty"},
                    {"Id": 2, "Name": "Sports & Fitness"},
                ],
            )
        )
        http = make_http()
        result = SystemResource(http).list_categories()
        http.close()
    assert route.called
    assert len(result) == 2
    assert result[0]["Name"] == "Health & Beauty"


def test_system_list_categories_with_id_filter():
    with respx.mock:
        route = respx.get(f"{BASE}/categories").mock(
            return_value=httpx.Response(200, json=[{"Id": 1, "Name": "Health & Beauty"}])
        )
        http = make_http()
        SystemResource(http).list_categories(id_=1)
        http.close()
    params = route.calls[0].request.url.params
    assert params["Id"] == "1"


def test_system_list_categories_results_wrapper():
    with respx.mock:
        respx.get(f"{BASE}/categories").mock(
            return_value=httpx.Response(
                200, json={"Results": [{"Id": 3, "Name": "Wellness"}]}
            )
        )
        http = make_http()
        result = SystemResource(http).list_categories()
        http.close()
    assert len(result) == 1
    assert result[0]["Name"] == "Wellness"


# ---------------------------------------------------------------------------
# list_countries
# ---------------------------------------------------------------------------


def test_system_list_countries():
    with respx.mock:
        route = respx.get(f"{BASE}/countries").mock(
            return_value=httpx.Response(
                200,
                json={
                    "Results": [
                        {"Id": "SE", "Name": "Sweden", "Currency": "SEK"},
                        {"Id": "NO", "Name": "Norway", "Currency": "NOK"},
                    ],
                    "Total": 2,
                    "Offset": 0,
                },
            )
        )
        http = make_http()
        result = SystemResource(http).list_countries()
        http.close()
    assert route.called
    assert result.total == 2
    assert result.results[0].id == "SE"
    assert result.results[0].name == "Sweden"


def test_system_list_countries_with_id_filter():
    with respx.mock:
        route = respx.get(f"{BASE}/countries").mock(
            return_value=httpx.Response(
                200,
                json={"Results": [{"Id": "SE", "Name": "Sweden"}], "Total": 1, "Offset": 0},
            )
        )
        http = make_http()
        result = SystemResource(http).list_countries(id_="SE")
        http.close()
    params = route.calls[0].request.url.params
    assert params["Id"] == "SE"
    assert result.results[0].id == "SE"


# ---------------------------------------------------------------------------
# list_currencies
# ---------------------------------------------------------------------------


def test_system_list_currencies():
    with respx.mock:
        route = respx.get(f"{BASE}/currencies").mock(
            return_value=httpx.Response(
                200,
                json={
                    "Results": [
                        {"Id": "SEK", "Name": "Swedish Krona", "CurrencySign": "kr", "Active": True}
                    ],
                    "Total": 1,
                    "Offset": 0,
                },
            )
        )
        http = make_http()
        result = SystemResource(http).list_currencies()
        http.close()
    assert result.total == 1
    assert result.results[0].id == "SEK"


def test_system_list_currencies_with_id_and_active_filter():
    with respx.mock:
        route = respx.get(f"{BASE}/currencies").mock(
            return_value=httpx.Response(
                200,
                json={"Results": [], "Total": 0, "Offset": 0},
            )
        )
        http = make_http()
        SystemResource(http).list_currencies(id_="SEK", active=True)
        http.close()
    params = route.calls[0].request.url.params
    assert params["Id"] == "SEK"
    assert params["Active"].lower() == "true"


# ---------------------------------------------------------------------------
# list_references
# ---------------------------------------------------------------------------


def test_system_list_references():
    with respx.mock:
        route = respx.get(f"{BASE}/references").mock(
            return_value=httpx.Response(
                200,
                json=[{"Id": 1, "ReferenceType": "stripe", "ExternalData": "cus_xxx"}],
            )
        )
        http = make_http()
        result = SystemResource(http).list_references(company_id=COMPANY_UUID)
        http.close()
    assert route.called
    assert len(result) == 1
    assert result[0]["ReferenceType"] == "stripe"


def test_system_list_references_with_id_filter():
    with respx.mock:
        route = respx.get(f"{BASE}/references").mock(
            return_value=httpx.Response(200, json=[])
        )
        http = make_http()
        SystemResource(http).list_references(company_id=COMPANY_UUID, id_=5)
        http.close()
    params = route.calls[0].request.url.params
    assert params["Id"] == "5"


# ---------------------------------------------------------------------------
# report_error
# ---------------------------------------------------------------------------


def test_system_report_error_basic():
    with respx.mock:
        route = respx.post(f"{BASE}/errors/").mock(
            return_value=httpx.Response(200, json={"Success": True})
        )
        http = make_http()
        result = SystemResource(http).report_error(
            exception_name="ValueError",
            exception_message="Something went wrong",
            stack_trace="  File ...",
        )
        http.close()
    assert route.called
    import json
    body = json.loads(route.calls[0].request.content)
    assert body["ExceptionName"] == "ValueError"
    assert body["ExceptionMessage"] == "Something went wrong"


def test_system_report_error_extended_params():
    with respx.mock:
        route = respx.post(f"{BASE}/errors/").mock(
            return_value=httpx.Response(200, json={})
        )
        http = make_http()
        SystemResource(http).report_error(
            exception_name="RuntimeError",
            inner_exception_name="IOError",
            logged_in_user="user@example.com",
            ip_address="1.2.3.4",
            company_id=COMPANY_UUID,
        )
        http.close()
    import json
    body = json.loads(route.calls[0].request.content)
    assert body["InnerExceptionName"] == "IOError"
    assert body["LoggedInUser"] == "user@example.com"
    assert body["IPAddress"] == "1.2.3.4"
    assert body["CompanyId"] == COMPANY_UUID
