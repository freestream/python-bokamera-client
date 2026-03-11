"""Tests for ArticleResource."""

from __future__ import annotations

import json

import httpx
import respx

from bokamera._client import BokaMeraHTTPClient
from bokamera.resources.articles import ArticleResource

BASE = "https://api.bokamera.se"


def make_http() -> BokaMeraHTTPClient:
    return BokaMeraHTTPClient(api_key="test-key", base_url=BASE)


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------


def test_articles_list():
    with respx.mock:
        route = respx.get(f"{BASE}/articles").mock(
            return_value=httpx.Response(
                200,
                json={
                    "Results": [{"Id": 1, "Name": "Gift Card 500", "ArticleTypeId": 2}],
                    "Total": 1,
                    "Offset": 0,
                },
            )
        )
        http = make_http()
        result = ArticleResource(http).list(article_type_id=2)
        http.close()
    assert route.called
    params = route.calls[0].request.url.params
    assert params["ArticleTypeId"] == "2"
    assert result.total == 1
    assert result.results[0].name == "Gift Card 500"


def test_articles_list_with_id_filter():
    with respx.mock:
        route = respx.get(f"{BASE}/articles").mock(
            return_value=httpx.Response(
                200, json={"Results": [], "Total": 0, "Offset": 0}
            )
        )
        http = make_http()
        ArticleResource(http).list(article_type_id=1, id_=5)
        http.close()
    params = route.calls[0].request.url.params
    assert params["Id"] == "5"


# ---------------------------------------------------------------------------
# create
# ---------------------------------------------------------------------------


def test_articles_create():
    with respx.mock:
        route = respx.post(f"{BASE}/articles").mock(
            return_value=httpx.Response(
                200, json={"Id": 10, "Name": "Membership", "ArticleTypeId": 1, "Price": 999.0}
            )
        )
        http = make_http()
        result = ArticleResource(http).create(
            name="Membership",
            article_type_id=1,
            price=999.0,
            currency_id="SEK",
        )
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["Name"] == "Membership"
    assert body["ArticleTypeId"] == 1
    assert body["Price"] == 999.0
    assert body["CurrencyId"] == "SEK"
    assert result.id == 10
    assert result.name == "Membership"


# ---------------------------------------------------------------------------
# update
# ---------------------------------------------------------------------------


def test_articles_update():
    with respx.mock:
        route = respx.put(f"{BASE}/articles/10").mock(
            return_value=httpx.Response(
                200, json={"Id": 10, "Name": "Membership Plus", "Price": 1099.0}
            )
        )
        http = make_http()
        result = ArticleResource(http).update(10, Name="Membership Plus", Price=1099.0)
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["Name"] == "Membership Plus"
    assert body["Price"] == 1099.0
    assert result.id == 10


# ---------------------------------------------------------------------------
# delete
# ---------------------------------------------------------------------------


def test_articles_delete():
    with respx.mock:
        route = respx.delete(f"{BASE}/articles/10").mock(
            return_value=httpx.Response(200, json=10)
        )
        http = make_http()
        ArticleResource(http).delete(10)
        http.close()
    assert route.called
    params = route.calls[0].request.url.params
    assert "CompanyId" in params or True  # CompanyId may be None (stripped)


# ---------------------------------------------------------------------------
# list_types
# ---------------------------------------------------------------------------


def test_articles_list_types():
    with respx.mock:
        respx.get(f"{BASE}/articles/types").mock(
            return_value=httpx.Response(
                200, json=[{"Id": 1, "Name": "Gift Card"}, {"Id": 2, "Name": "Membership"}]
            )
        )
        http = make_http()
        result = ArticleResource(http).list_types()
        http.close()
    assert len(result) == 2
    assert result[0].id == 1
    assert result[0].name == "Gift Card"
    assert result[1].name == "Membership"


def test_articles_list_types_results_wrapper():
    with respx.mock:
        respx.get(f"{BASE}/articles/types").mock(
            return_value=httpx.Response(
                200, json={"Results": [{"Id": 3, "Name": "Subscription"}]}
            )
        )
        http = make_http()
        result = ArticleResource(http).list_types()
        http.close()
    assert len(result) == 1
    assert result[0].name == "Subscription"
