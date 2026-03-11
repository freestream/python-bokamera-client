"""Tests for EAccountingResource."""

from __future__ import annotations

import json

import httpx
import respx

from bokamera._client import BokaMeraHTTPClient
from bokamera.resources.eaccounting import EAccountingResource

BASE = "https://api.bokamera.se"
COMPANY_UUID = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"


def make_http() -> BokaMeraHTTPClient:
    return BokaMeraHTTPClient(api_key="test-key", base_url=BASE)


# ---------------------------------------------------------------------------
# check_connection / get_token
# ---------------------------------------------------------------------------


def test_eaccounting_check_connection():
    with respx.mock:
        route = respx.get(f"{BASE}/eaccounting/check").mock(
            return_value=httpx.Response(
                200,
                json={"AccessToken": "abc123", "TokenType": "Bearer"},
            )
        )
        http = make_http()
        result = EAccountingResource(http).check_connection(company_id=COMPANY_UUID)
        http.close()
    assert route.called
    assert result.access_token == "abc123"
    assert result.token_type == "Bearer"


def test_eaccounting_get_token():
    with respx.mock:
        respx.get(f"{BASE}/eaccounting/token").mock(
            return_value=httpx.Response(
                200,
                json={"AccessToken": "tok-xyz", "RefreshToken": "ref-xyz"},
            )
        )
        http = make_http()
        result = EAccountingResource(http).get_token(company_id=COMPANY_UUID)
        http.close()
    assert result.refresh_token == "ref-xyz"


# ---------------------------------------------------------------------------
# get_settings
# ---------------------------------------------------------------------------


def test_eaccounting_get_settings():
    with respx.mock:
        respx.get(f"{BASE}/eaccounting/settings").mock(
            return_value=httpx.Response(
                200,
                json={"Active": True, "DefaultCreateType": "Invoice"},
            )
        )
        http = make_http()
        result = EAccountingResource(http).get_settings(company_id=COMPANY_UUID)
        http.close()
    assert result.active is True
    assert result.default_create_type == "Invoice"


# ---------------------------------------------------------------------------
# list_articles / create_article
# ---------------------------------------------------------------------------


def test_eaccounting_list_articles():
    with respx.mock:
        respx.get(f"{BASE}/eaccounting/articles").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {"ArticleName": "Massage", "ArticlePrice": 500.0, "VatRate": "SE25"},
                ],
            )
        )
        http = make_http()
        results = EAccountingResource(http).list_articles(company_id=COMPANY_UUID)
        http.close()
    assert len(results) == 1
    assert results[0].article_name == "Massage"
    assert results[0].article_price == 500.0


def test_eaccounting_list_articles_wrapped():
    with respx.mock:
        respx.get(f"{BASE}/eaccounting/articles").mock(
            return_value=httpx.Response(
                200,
                json={"Results": [{"ArticleName": "Haircut", "ArticlePrice": 300.0}]},
            )
        )
        http = make_http()
        results = EAccountingResource(http).list_articles(company_id=COMPANY_UUID)
        http.close()
    assert results[0].article_name == "Haircut"


def test_eaccounting_create_article():
    with respx.mock:
        route = respx.post(f"{BASE}/eaccounting/articles").mock(
            return_value=httpx.Response(
                200,
                json={"ArticleName": "New Article", "ArticlePrice": 150.0},
            )
        )
        http = make_http()
        result = EAccountingResource(http).create_article(
            service_id=7,
            article_name="New Article",
            article_price=150.0,
            company_id=COMPANY_UUID,
        )
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["ServiceId"] == 7
    assert body["ArticleName"] == "New Article"
    assert result.article_name == "New Article"


# ---------------------------------------------------------------------------
# list_invoices / create_invoice
# ---------------------------------------------------------------------------


def test_eaccounting_list_invoices():
    with respx.mock:
        respx.get(f"{BASE}/eaccounting/invoices").mock(
            return_value=httpx.Response(
                200,
                json=[{"Id": "inv-1", "BookingId": 10, "TotalAmount": 500.0, "Paid": False}],
            )
        )
        http = make_http()
        results = EAccountingResource(http).list_invoices(company_id=COMPANY_UUID)
        http.close()
    assert len(results) == 1
    assert results[0].id == "inv-1"
    assert results[0].total_amount == 500.0


def test_eaccounting_create_invoice():
    with respx.mock:
        route = respx.post(f"{BASE}/eaccounting/invoice").mock(
            return_value=httpx.Response(200, json={"InvoiceId": "inv-new"})
        )
        http = make_http()
        result = EAccountingResource(http).create_invoice(
            booking_id=55,
            invoice_customer_name="Sven Svensson",
            company_id=COMPANY_UUID,
        )
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["BookingId"] == 55
    assert body["InvoiceCustomerName"] == "Sven Svensson"
    assert result["InvoiceId"] == "inv-new"


# ---------------------------------------------------------------------------
# list_notes / create_note
# ---------------------------------------------------------------------------


def test_eaccounting_list_notes():
    with respx.mock:
        respx.get(f"{BASE}/eaccounting/notes").mock(
            return_value=httpx.Response(
                200,
                json=[{"Id": "note-1", "Text": "Hello"}],
            )
        )
        http = make_http()
        results = EAccountingResource(http).list_notes(company_id=COMPANY_UUID)
        http.close()
    assert results[0].id == "note-1"
    assert results[0].text == "Hello"


def test_eaccounting_create_note():
    with respx.mock:
        route = respx.post(f"{BASE}/eaccounting/notes").mock(
            return_value=httpx.Response(
                200,
                json={"Id": "note-new", "Text": "Important note"},
            )
        )
        http = make_http()
        result = EAccountingResource(http).create_note(
            text="Important note",
            company_id=COMPANY_UUID,
        )
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["Text"] == "Important note"
    assert result.text == "Important note"


# ---------------------------------------------------------------------------
# convert_invoice_draft
# ---------------------------------------------------------------------------


def test_eaccounting_convert_invoice_draft():
    with respx.mock:
        route = respx.post(f"{BASE}/eaccounting/invoicedrafts/convert").mock(
            return_value=httpx.Response(200, json={"InvoiceId": "final-inv"})
        )
        http = make_http()
        result = EAccountingResource(http).convert_invoice_draft(
            invoice_draft_id="draft-1",
            send_type="Email",
            booking_id=99,
            company_id=COMPANY_UUID,
        )
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["InvoiceDraftId"] == "draft-1"
    assert body["SendType"] == "Email"
    assert result["InvoiceId"] == "final-inv"
