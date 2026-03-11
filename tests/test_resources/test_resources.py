"""Tests for ResourceResource."""

from __future__ import annotations

import httpx
import respx

from bokamera._client import BokaMeraHTTPClient
from bokamera.resources.resources import ResourceResource

BASE = "https://api.bokamera.se"
RESOURCE_UUID = "11111111-2222-3333-4444-555555555555"
COMPANY_UUID = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"


def make_http() -> BokaMeraHTTPClient:
    return BokaMeraHTTPClient(api_key="test-key", base_url=BASE)


# ---------------------------------------------------------------------------
# list resources
# ---------------------------------------------------------------------------


def test_resources_list_no_filter():
    with respx.mock:
        route = respx.get(f"{BASE}/resource").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "Id": RESOURCE_UUID,
                        "Name": "John Smith",
                        "Active": True,
                    }
                ],
            )
        )
        http = make_http()
        result = ResourceResource(http).list()
        http.close()
    assert route.called
    assert len(result) == 1
    assert result[0].name == "John Smith"
    assert result[0].active is True


def test_resources_list_with_id_filter():
    with respx.mock:
        route = respx.get(f"{BASE}/resource").mock(
            return_value=httpx.Response(200, json=[])
        )
        http = make_http()
        ResourceResource(http).list(id_=RESOURCE_UUID)
        http.close()
    params = route.calls[0].request.url.params
    assert params["Id"] == RESOURCE_UUID


def test_resources_list_with_results_wrapper():
    with respx.mock:
        respx.get(f"{BASE}/resource").mock(
            return_value=httpx.Response(
                200,
                json={"Results": [{"Id": RESOURCE_UUID, "Name": "Jane Doe"}]},
            )
        )
        http = make_http()
        result = ResourceResource(http).list()
        http.close()
    assert len(result) == 1
    assert result[0].name == "Jane Doe"


# ---------------------------------------------------------------------------
# list_types
# ---------------------------------------------------------------------------


def test_resource_types_list_no_filter():
    with respx.mock:
        route = respx.get(f"{BASE}/resourcetypes").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {"Id": 1, "Name": "Therapist", "Active": True}
                ],
            )
        )
        http = make_http()
        result = ResourceResource(http).list_types()
        http.close()
    assert route.called
    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].name == "Therapist"


def test_resource_types_list_with_id_filter():
    with respx.mock:
        route = respx.get(f"{BASE}/resourcetypes").mock(
            return_value=httpx.Response(200, json=[])
        )
        http = make_http()
        ResourceResource(http).list_types(id_=3)
        http.close()
    params = route.calls[0].request.url.params
    assert params["Id"] == "3"


def test_resource_types_list_with_results_wrapper():
    with respx.mock:
        respx.get(f"{BASE}/resourcetypes").mock(
            return_value=httpx.Response(
                200,
                json={"Results": [{"Id": 2, "Name": "Room"}]},
            )
        )
        http = make_http()
        result = ResourceResource(http).list_types()
        http.close()
    assert len(result) == 1
    assert result[0].name == "Room"
