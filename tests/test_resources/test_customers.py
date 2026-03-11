"""Tests for CustomerResource."""

from __future__ import annotations

import json

import httpx
import respx

from bokamera._client import BokaMeraHTTPClient
from bokamera.resources.customers import CustomerResource

BASE = "https://api.bokamera.se"
CUSTOMER_UUID = "11111111-2222-3333-4444-555555555555"
COMPANY_UUID = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"


def make_http() -> BokaMeraHTTPClient:
    return BokaMeraHTTPClient(api_key="test-key", base_url=BASE)


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------


def test_customers_list():
    with respx.mock:
        route = respx.get(f"{BASE}/customers").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "Id": CUSTOMER_UUID,
                        "Firstname": "Anna",
                        "Lastname": "Svensson",
                        "Email": "anna@example.com",
                    }
                ],
            )
        )
        http = make_http()
        result = CustomerResource(http).list()
        http.close()
    assert route.called
    assert len(result) == 1
    assert result[0].firstname == "Anna"
    assert result[0].lastname == "Svensson"


def test_customers_list_returns_list_type():
    with respx.mock:
        respx.get(f"{BASE}/customers").mock(
            return_value=httpx.Response(200, json=[])
        )
        http = make_http()
        result = CustomerResource(http).list()
        http.close()
    assert isinstance(result, list)


# ---------------------------------------------------------------------------
# create
# ---------------------------------------------------------------------------


def test_customers_create():
    with respx.mock:
        route = respx.post(f"{BASE}/customers").mock(
            return_value=httpx.Response(
                200,
                json={
                    "Id": CUSTOMER_UUID,
                    "Firstname": "Erik",
                    "Lastname": "Nilsson",
                    "Email": "erik@example.com",
                },
            )
        )
        http = make_http()
        result = CustomerResource(http).create(
            firstname="Erik",
            lastname="Nilsson",
            email="erik@example.com",
            phone="+46701112233",
        )
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["Firstname"] == "Erik"
    assert body["Lastname"] == "Nilsson"
    assert body["Email"] == "erik@example.com"
    assert body["Phone"] == "+46701112233"
    assert result.firstname == "Erik"


# ---------------------------------------------------------------------------
# list_articles
# ---------------------------------------------------------------------------


def test_customers_list_articles():
    with respx.mock:
        route = respx.get(f"{BASE}/customerarticle").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "Id": 10,
                        "ArticleId": 3,
                        "CustomerId": CUSTOMER_UUID,
                        "StatusId": 1,
                    }
                ],
            )
        )
        http = make_http()
        result = CustomerResource(http).list_articles()
        http.close()
    assert route.called
    assert len(result) == 1
    assert result[0].id == 10
    assert result[0].article_id == 3


def test_customers_list_articles_with_id_filter():
    with respx.mock:
        route = respx.get(f"{BASE}/customerarticle").mock(
            return_value=httpx.Response(200, json=[])
        )
        http = make_http()
        CustomerResource(http).list_articles(id_=7)
        http.close()
    params = route.calls[0].request.url.params
    assert params["Id"] == "7"
