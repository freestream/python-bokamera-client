"""Tests for SupportResource."""

from __future__ import annotations

import httpx
import respx

from bokamera._client import BokaMeraHTTPClient
from bokamera.resources.support import SupportResource

BASE = "https://api.bokamera.se"
COMPANY_UUID = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"


def make_http() -> BokaMeraHTTPClient:
    return BokaMeraHTTPClient(api_key="test-key", base_url=BASE)


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------


def test_support_list_no_filter():
    with respx.mock:
        route = respx.get(f"{BASE}/support/cases").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "Id": 1,
                        "CompanyId": COMPANY_UUID,
                        "Title": "Login issue",
                        "Active": True,
                    }
                ],
            )
        )
        http = make_http()
        result = SupportResource(http).list(company_id=COMPANY_UUID)
        http.close()
    assert route.called
    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].title == "Login issue"


def test_support_list_with_id_filter():
    with respx.mock:
        route = respx.get(f"{BASE}/support/cases").mock(
            return_value=httpx.Response(200, json=[])
        )
        http = make_http()
        SupportResource(http).list(company_id=COMPANY_UUID, id_=3)
        http.close()
    params = route.calls[0].request.url.params
    assert params["Id"] == "3"


def test_support_list_with_results_wrapper():
    with respx.mock:
        respx.get(f"{BASE}/support/cases").mock(
            return_value=httpx.Response(
                200,
                json={
                    "Results": [
                        {"Id": 2, "CompanyId": COMPANY_UUID, "Title": "API question"}
                    ]
                },
            )
        )
        http = make_http()
        result = SupportResource(http).list(company_id=COMPANY_UUID)
        http.close()
    assert len(result) == 1
    assert result[0].title == "API question"


def test_support_list_include_options_params():
    with respx.mock:
        route = respx.get(f"{BASE}/support/cases").mock(
            return_value=httpx.Response(200, json=[])
        )
        http = make_http()
        SupportResource(http).list(
            company_id=COMPANY_UUID,
            include_case_status_options=True,
            include_case_type_options=True,
            include_case_area_options=True,
        )
        http.close()
    params = route.calls[0].request.url.params
    assert params["IncludeCaseStatusOptions"].lower() == "true"
    assert params["IncludeCaseTypeOptions"].lower() == "true"
    assert params["IncludeCaseAreaOptions"].lower() == "true"
