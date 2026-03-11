"""Tests for BillingResource."""

from __future__ import annotations

import json

import httpx
import respx

from bokamera._client import BokaMeraHTTPClient
from bokamera.resources.billing import BillingResource

BASE = "https://api.bokamera.se"


def make_http() -> BokaMeraHTTPClient:
    return BokaMeraHTTPClient(api_key="test-key", base_url=BASE)


# ---------------------------------------------------------------------------
# list_methods
# ---------------------------------------------------------------------------


def test_billing_list_methods():
    with respx.mock:
        route = respx.get(f"{BASE}/billing/methods").mock(
            return_value=httpx.Response(
                200,
                json={
                    "Results": [
                        {"Id": 1, "Name": "Invoice"},
                        {"Id": 2, "Name": "Credit card"},
                    ],
                    "Total": 2,
                    "Offset": 0,
                },
            )
        )
        http = make_http()
        result = BillingResource(http).list_methods()
        http.close()
    assert route.called
    assert result.total == 2
    assert result.results[0].name == "Invoice"
    assert result.results[1].name == "Credit card"


def test_billing_list_methods_with_country():
    with respx.mock:
        route = respx.get(f"{BASE}/billing/methods").mock(
            return_value=httpx.Response(
                200, json={"Results": [], "Total": 0, "Offset": 0}
            )
        )
        http = make_http()
        BillingResource(http).list_methods(country_id="SE")
        http.close()
    params = route.calls[0].request.url.params
    assert params["CountryId"] == "SE"


# ---------------------------------------------------------------------------
# list_invoices
# ---------------------------------------------------------------------------


def test_billing_list_invoices():
    company_id = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    with respx.mock:
        route = respx.get(f"{BASE}/billing/company/invoices").mock(
            return_value=httpx.Response(
                200,
                json={
                    "Results": [
                        {
                            "Id": 500,
                            "CompanyId": company_id,
                            "Total": 1299.0,
                            "Currency": "SEK",
                            "Status": "Paid",
                        }
                    ],
                    "Total": 1,
                    "Offset": 0,
                },
            )
        )
        http = make_http()
        result = BillingResource(http).list_invoices(company_id=company_id)
        http.close()
    assert route.called
    assert result.total == 1
    assert result.results[0].id == 500
    assert result.results[0].total == 1299.0


def test_billing_list_invoices_with_id_filter():
    company_id = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    with respx.mock:
        route = respx.get(f"{BASE}/billing/company/invoices").mock(
            return_value=httpx.Response(
                200, json={"Results": [], "Total": 0, "Offset": 0}
            )
        )
        http = make_http()
        BillingResource(http).list_invoices(company_id=company_id, id_=42)
        http.close()
    params = route.calls[0].request.url.params
    assert params["Id"] == "42"


# ---------------------------------------------------------------------------
# create_qvickly_settings
# ---------------------------------------------------------------------------


def test_billing_create_qvickly_settings():
    company_id = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    with respx.mock:
        route = respx.post(f"{BASE}/payment/billmate/apisettings").mock(
            return_value=httpx.Response(200, json={"Success": True})
        )
        http = make_http()
        result = BillingResource(http).create_qvickly_settings(
            id_="MERCHANT123",
            secret="mysecret",
            receiver_email="payments@spa.se",
            company_id=company_id,
        )
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["Id"] == "MERCHANT123"
    assert body["Secret"] == "mysecret"
    assert body["ReceiverEmail"] == "payments@spa.se"
    assert result == {"Success": True}
