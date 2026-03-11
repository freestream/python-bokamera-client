"""Tests for HomepageResource."""

from __future__ import annotations

import httpx
import respx

from bokamera._client import BokaMeraHTTPClient
from bokamera.resources.homepage import HomepageResource

BASE = "https://api.bokamera.se"
COMPANY_UUID = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"


def make_http() -> BokaMeraHTTPClient:
    return BokaMeraHTTPClient(api_key="test-key", base_url=BASE)


# ---------------------------------------------------------------------------
# list_images
# ---------------------------------------------------------------------------


def test_homepage_list_images():
    with respx.mock:
        route = respx.get(f"{BASE}/homepage/images").mock(
            return_value=httpx.Response(
                200,
                json={
                    "Results": [
                        {
                            "Id": 1,
                            "Title": "Reception",
                            "Description": "Our welcoming reception",
                            "ImageUrl": "https://example.com/reception.jpg",
                        },
                        {
                            "Id": 2,
                            "Title": "Treatment room",
                            "ImageUrl": "https://example.com/room.jpg",
                        },
                    ],
                    "Total": 2,
                    "Offset": 0,
                },
            )
        )
        http = make_http()
        result = HomepageResource(http).list_images(
            site_path="spa-wellness", company_id=COMPANY_UUID
        )
        http.close()
    assert route.called
    params = route.calls[0].request.url.params
    assert params["SitePath"] == "spa-wellness"
    assert result.total == 2
    assert result.results[0].id == 1
    assert result.results[0].title == "Reception"
    assert result.results[1].image_url == "https://example.com/room.jpg"


def test_homepage_list_images_with_id_filter():
    with respx.mock:
        route = respx.get(f"{BASE}/homepage/images").mock(
            return_value=httpx.Response(
                200, json={"Results": [], "Total": 0, "Offset": 0}
            )
        )
        http = make_http()
        HomepageResource(http).list_images(
            site_path="spa-wellness", company_id=COMPANY_UUID, id_=3
        )
        http.close()
    params = route.calls[0].request.url.params
    assert params["Id"] == "3"
    assert params["SitePath"] == "spa-wellness"


def test_homepage_list_images_empty():
    with respx.mock:
        respx.get(f"{BASE}/homepage/images").mock(
            return_value=httpx.Response(
                200, json={"Results": [], "Total": 0, "Offset": 0}
            )
        )
        http = make_http()
        result = HomepageResource(http).list_images(
            site_path="test-company", company_id=COMPANY_UUID
        )
        http.close()
    assert result.total == 0
    assert result.results == []
