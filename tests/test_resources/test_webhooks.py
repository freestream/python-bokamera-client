"""Tests for WebhookResource."""

from __future__ import annotations

import json

import httpx
import respx

from bokamera._client import BokaMeraHTTPClient
from bokamera.resources.webhooks import WebhookResource

BASE = "https://api.bokamera.se"
COMPANY_UUID = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
ENDPOINT_UUID = "11111111-2222-3333-4444-555555555555"


def make_http() -> BokaMeraHTTPClient:
    return BokaMeraHTTPClient(api_key="test-key", base_url=BASE)


# ---------------------------------------------------------------------------
# get
# ---------------------------------------------------------------------------


def test_webhooks_get():
    with respx.mock:
        route = respx.get(f"{BASE}/webhook/endpoints/{ENDPOINT_UUID}").mock(
            return_value=httpx.Response(
                200,
                json={
                    "Id": ENDPOINT_UUID,
                    "CompanyId": COMPANY_UUID,
                    "Url": "https://myapp.example.com/hook",
                    "EventTypes": ["booking.created", "booking.cancelled"],
                    "Disabled": False,
                },
            )
        )
        http = make_http()
        result = WebhookResource(http).get(ENDPOINT_UUID, company_id=COMPANY_UUID)
        http.close()
    assert route.called
    assert str(result.id) == ENDPOINT_UUID
    assert result.url == "https://myapp.example.com/hook"
    assert result.disabled is False
    assert "booking.created" in result.event_types


def test_webhooks_get_with_secret():
    with respx.mock:
        route = respx.get(f"{BASE}/webhook/endpoints/{ENDPOINT_UUID}").mock(
            return_value=httpx.Response(
                200,
                json={
                    "Id": ENDPOINT_UUID,
                    "Url": "https://myapp.example.com/hook",
                    "EventTypes": [],
                    "Secret": "whsec_abc123",
                },
            )
        )
        http = make_http()
        result = WebhookResource(http).get(
            ENDPOINT_UUID,
            include_secret=True,
            company_id=COMPANY_UUID,
        )
        http.close()
    params = route.calls[0].request.url.params
    assert params["IncludeSecret"].lower() == "true"
    assert result.secret == "whsec_abc123"


# ---------------------------------------------------------------------------
# create
# ---------------------------------------------------------------------------


def test_webhooks_create():
    with respx.mock:
        route = respx.post(f"{BASE}/webhook/endpoints").mock(
            return_value=httpx.Response(
                200,
                json={
                    "Id": ENDPOINT_UUID,
                    "CompanyId": COMPANY_UUID,
                    "Url": "https://myapp.example.com/hook",
                    "EventTypes": ["booking.created"],
                    "Disabled": False,
                    "Description": "My webhook",
                },
            )
        )
        http = make_http()
        result = WebhookResource(http).create(
            url="https://myapp.example.com/hook",
            event_types=["booking.created"],
            description="My webhook",
            company_id=COMPANY_UUID,
        )
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["Url"] == "https://myapp.example.com/hook"
    assert body["EventTypes"] == ["booking.created"]
    assert body["Description"] == "My webhook"
    assert body["Disabled"] is False
    assert result.url == "https://myapp.example.com/hook"
    assert result.description == "My webhook"


def test_webhooks_create_disabled():
    with respx.mock:
        route = respx.post(f"{BASE}/webhook/endpoints").mock(
            return_value=httpx.Response(
                200,
                json={
                    "Id": ENDPOINT_UUID,
                    "Url": "https://myapp.example.com/hook",
                    "EventTypes": ["booking.created"],
                    "Disabled": True,
                },
            )
        )
        http = make_http()
        result = WebhookResource(http).create(
            url="https://myapp.example.com/hook",
            event_types=["booking.created"],
            disabled=True,
            company_id=COMPANY_UUID,
        )
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["Disabled"] is True
    assert result.disabled is True


# ---------------------------------------------------------------------------
# delete
# ---------------------------------------------------------------------------


def test_webhooks_delete():
    with respx.mock:
        route = respx.delete(f"{BASE}/webhook/endpoints/{ENDPOINT_UUID}").mock(
            return_value=httpx.Response(200, json={"Deleted": True})
        )
        http = make_http()
        result = WebhookResource(http).delete(ENDPOINT_UUID, company_id=COMPANY_UUID)
        http.close()
    assert route.called
    params = route.calls[0].request.url.params
    assert params["CompanyId"] == COMPANY_UUID
    assert result["Deleted"] is True
