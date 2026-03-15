"""Tests for LicenseResource."""

from __future__ import annotations

import httpx
import respx

from bokamera._client import BokaMeraHTTPClient
from bokamera.resources.licenses import LicenseResource

BASE = "https://api.bokamera.se"
COMPANY_UUID = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"


def make_http() -> BokaMeraHTTPClient:
    return BokaMeraHTTPClient(api_key="test-key", base_url=BASE)


# ---------------------------------------------------------------------------
# list_company_licenses
# ---------------------------------------------------------------------------


def test_license_list_company_licenses():
    with respx.mock:
        route = respx.get(f"{BASE}/licenses/company").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "Id": 10,
                        "CompanyId": COMPANY_UUID,
                        "TypeId": 2,
                        "Type": {"Name": "Professional"},
                        "Active": True,
                    }
                ],
            )
        )
        http = make_http()
        result = LicenseResource(http).list_company_licenses(company_id=COMPANY_UUID)
        http.close()
    assert route.called
    assert len(result) == 1
    assert result[0].id == 10


def test_license_list_company_licenses_new_params():
    with respx.mock:
        route = respx.get(f"{BASE}/licenses/company").mock(
            return_value=httpx.Response(200, json=[])
        )
        http = make_http()
        LicenseResource(http).list_company_licenses(
            company_id=COMPANY_UUID,
            meta_data="promo2026",
            is_extra_license_option=True,
        )
        http.close()
    params = route.calls[0].request.url.params
    assert params["MetaData"] == "promo2026"
    assert params["IsExtraLicenseOption"].lower() == "true"


# ---------------------------------------------------------------------------
# list_types
# ---------------------------------------------------------------------------


def test_license_list_types():
    with respx.mock:
        route = respx.get(f"{BASE}/licenses/types/").mock(
            return_value=httpx.Response(
                200,
                json={
                    "Results": [
                        {"Id": 1, "Name": "Free", "Description": "Free plan"},
                        {"Id": 2, "Name": "Professional", "Description": "Pro plan"},
                    ],
                    "Total": 2,
                    "Offset": 0,
                },
            )
        )
        http = make_http()
        result = LicenseResource(http).list_types()
        http.close()
    assert route.called
    assert result.total == 2
    assert result.results[0].id == 1
    assert result.results[0].name == "Free"
    assert result.results[1].name == "Professional"


def test_license_list_types_empty():
    with respx.mock:
        respx.get(f"{BASE}/licenses/types/").mock(
            return_value=httpx.Response(
                200, json={"Results": [], "Total": 0, "Offset": 0}
            )
        )
        http = make_http()
        result = LicenseResource(http).list_types()
        http.close()
    assert result.total == 0
    assert result.results == []


# ---------------------------------------------------------------------------
# list_trials
# ---------------------------------------------------------------------------


def test_license_list_trials():
    with respx.mock:
        route = respx.get(f"{BASE}/trials/company/").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "Id": 5,
                        "CompanyId": COMPANY_UUID,
                        "TrialTypeId": 1,
                        "TrialType": "Premium trial",
                        "Active": True,
                    }
                ],
            )
        )
        http = make_http()
        result = LicenseResource(http).list_trials(company_id=COMPANY_UUID)
        http.close()
    assert route.called
    assert len(result) == 1
    assert result[0].id == 5
    assert result[0].trial_type == "Premium trial"


def test_license_list_trials_with_id_filter():
    with respx.mock:
        route = respx.get(f"{BASE}/trials/company/").mock(
            return_value=httpx.Response(200, json=[])
        )
        http = make_http()
        LicenseResource(http).list_trials(company_id=COMPANY_UUID, id_=5)
        http.close()
    params = route.calls[0].request.url.params
    assert params["Id"] == "5"


def test_license_list_trials_results_wrapper():
    with respx.mock:
        respx.get(f"{BASE}/trials/company/").mock(
            return_value=httpx.Response(
                200,
                json={
                    "Results": [
                        {"Id": 3, "CompanyId": COMPANY_UUID, "TrialType": "Basic trial"}
                    ]
                },
            )
        )
        http = make_http()
        result = LicenseResource(http).list_trials(company_id=COMPANY_UUID)
        http.close()
    assert len(result) == 1
    assert result[0].trial_type == "Basic trial"
