"""Tests for BokaMeraHTTPClient (low-level HTTP client)."""

from __future__ import annotations

import json
from uuid import UUID

import httpx
import pytest
import respx

from bokamera._client import BokaMeraHTTPClient, _clean
from bokamera.exceptions import (
    BokaMeraAuthError,
    BokaMeraForbiddenError,
    BokaMeraHTTPError,
    BokaMeraNotFoundError,
    BokaMeraRateLimitError,
    BokaMeraValidationError,
)

BASE = "https://api.bokamera.se"


def make_http(**kwargs) -> BokaMeraHTTPClient:
    return BokaMeraHTTPClient(api_key="test-key", base_url=BASE, **kwargs)


# ---------------------------------------------------------------------------
# _clean helper
# ---------------------------------------------------------------------------


class TestClean:
    def test_removes_none_values(self):
        result = _clean({"a": 1, "b": None, "c": "hello"})
        assert result == {"a": 1, "c": "hello"}

    def test_keeps_zero(self):
        result = _clean({"a": 0, "b": None})
        assert result == {"a": 0}

    def test_keeps_false(self):
        result = _clean({"a": False, "b": None})
        assert result == {"a": False}

    def test_keeps_empty_string(self):
        result = _clean({"a": "", "b": None})
        assert result == {"a": ""}

    def test_empty_dict(self):
        assert _clean({}) == {}

    def test_all_none(self):
        assert _clean({"x": None, "y": None}) == {}

    def test_all_kept(self):
        d = {"a": 1, "b": "x", "c": True}
        assert _clean(d) == d


# ---------------------------------------------------------------------------
# default_company_id property
# ---------------------------------------------------------------------------


class TestDefaultCompanyId:
    def test_returns_none_when_not_set(self):
        http = make_http()
        assert http.default_company_id is None
        http.close()

    def test_returns_string_when_set(self):
        uid = UUID("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")
        http = make_http(company_id=uid)
        assert http.default_company_id == "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        http.close()


# ---------------------------------------------------------------------------
# GET
# ---------------------------------------------------------------------------


class TestGet:
    def test_passes_query_params(self):
        with respx.mock:
            route = respx.get(f"{BASE}/services").mock(
                return_value=httpx.Response(200, json=[])
            )
            http = make_http()
            http.get("/services", {"Id": 42, "Active": True})
            http.close()
        assert route.called
        params = route.calls[0].request.url.params
        assert params["Id"] == "42"
        assert params["Active"].lower() == "true"

    def test_strips_none_params(self):
        with respx.mock:
            route = respx.get(f"{BASE}/services").mock(
                return_value=httpx.Response(200, json=[])
            )
            http = make_http()
            http.get("/services", {"Id": None, "Active": True})
            http.close()
        params = route.calls[0].request.url.params
        assert "Id" not in params
        assert params["Active"].lower() == "true"

    def test_returns_parsed_json(self):
        with respx.mock:
            respx.get(f"{BASE}/services").mock(
                return_value=httpx.Response(200, json={"Results": [{"Id": 1}]})
            )
            http = make_http()
            result = http.get("/services")
            http.close()
        assert result == {"Results": [{"Id": 1}]}


# ---------------------------------------------------------------------------
# POST
# ---------------------------------------------------------------------------


class TestPost:
    def test_sends_json_body(self):
        with respx.mock:
            route = respx.post(f"{BASE}/bookings").mock(
                return_value=httpx.Response(200, json={"Id": 99})
            )
            http = make_http()
            http.post("/bookings", {"ServiceId": 5, "Name": "Test"})
            http.close()
        body = json.loads(route.calls[0].request.content)
        assert body["ServiceId"] == 5
        assert body["Name"] == "Test"

    def test_strips_none_from_body(self):
        with respx.mock:
            route = respx.post(f"{BASE}/bookings").mock(
                return_value=httpx.Response(200, json={})
            )
            http = make_http()
            http.post("/bookings", {"ServiceId": 5, "Description": None})
            http.close()
        body = json.loads(route.calls[0].request.content)
        assert "Description" not in body
        assert body["ServiceId"] == 5

    def test_returns_empty_dict_on_non_json_response(self):
        with respx.mock:
            respx.post(f"{BASE}/something").mock(
                return_value=httpx.Response(200, content=b"OK")
            )
            http = make_http()
            result = http.post("/something")
            http.close()
        assert result == {}


# ---------------------------------------------------------------------------
# PUT
# ---------------------------------------------------------------------------


class TestPut:
    def test_sends_json_body(self):
        with respx.mock:
            route = respx.put(f"{BASE}/services/1").mock(
                return_value=httpx.Response(200, json={"Id": 1, "Name": "Updated"})
            )
            http = make_http()
            http.put("/services/1", {"Name": "Updated"})
            http.close()
        body = json.loads(route.calls[0].request.content)
        assert body["Name"] == "Updated"

    def test_returns_parsed_json(self):
        with respx.mock:
            respx.put(f"{BASE}/services/1").mock(
                return_value=httpx.Response(200, json={"Id": 1})
            )
            http = make_http()
            result = http.put("/services/1", {})
            http.close()
        assert result == {"Id": 1}


# ---------------------------------------------------------------------------
# DELETE
# ---------------------------------------------------------------------------


class TestDelete:
    def test_passes_params(self):
        with respx.mock:
            route = respx.delete(f"{BASE}/services/1").mock(
                return_value=httpx.Response(200, json={"Id": 1})
            )
            http = make_http()
            http.delete("/services/1", {"CompanyId": "abc"})
            http.close()
        params = route.calls[0].request.url.params
        assert params["CompanyId"] == "abc"

    def test_strips_none_params(self):
        with respx.mock:
            route = respx.delete(f"{BASE}/services/1").mock(
                return_value=httpx.Response(200, json={})
            )
            http = make_http()
            http.delete("/services/1", {"CompanyId": "abc", "Extra": None})
            http.close()
        params = route.calls[0].request.url.params
        assert "Extra" not in params


# ---------------------------------------------------------------------------
# _raise_for_status
# ---------------------------------------------------------------------------


class TestRaiseForStatus:
    def _make_response(self, status: int, body: dict | None = None) -> httpx.Response:
        if body is not None:
            return httpx.Response(status, json=body)
        return httpx.Response(status, content=b"error text")

    def test_400_raises_validation_error(self):
        with respx.mock:
            respx.get(f"{BASE}/services").mock(
                return_value=httpx.Response(400, json={"ResponseStatus": {"Message": "bad request"}})
            )
            http = make_http()
            with pytest.raises(BokaMeraValidationError) as exc_info:
                http.get("/services")
            http.close()
        assert exc_info.value.status_code == 400
        assert "bad request" in exc_info.value.message

    def test_401_raises_auth_error(self):
        with respx.mock:
            respx.get(f"{BASE}/services").mock(return_value=httpx.Response(401, content=b"Unauthorized"))
            http = make_http()
            with pytest.raises(BokaMeraAuthError) as exc_info:
                http.get("/services")
            http.close()
        assert exc_info.value.status_code == 401

    def test_403_raises_forbidden_error(self):
        with respx.mock:
            respx.get(f"{BASE}/services").mock(return_value=httpx.Response(403, content=b"Forbidden"))
            http = make_http()
            with pytest.raises(BokaMeraForbiddenError) as exc_info:
                http.get("/services")
            http.close()
        assert exc_info.value.status_code == 403

    def test_404_raises_not_found_error(self):
        with respx.mock:
            respx.get(f"{BASE}/services").mock(return_value=httpx.Response(404, content=b"Not Found"))
            http = make_http()
            with pytest.raises(BokaMeraNotFoundError) as exc_info:
                http.get("/services")
            http.close()
        assert exc_info.value.status_code == 404

    def test_429_raises_rate_limit_error(self):
        with respx.mock:
            respx.get(f"{BASE}/services").mock(return_value=httpx.Response(429, content=b"Too Many Requests"))
            http = make_http()
            with pytest.raises(BokaMeraRateLimitError) as exc_info:
                http.get("/services")
            http.close()
        assert exc_info.value.status_code == 429

    def test_500_raises_generic_http_error(self):
        with respx.mock:
            respx.get(f"{BASE}/services").mock(return_value=httpx.Response(500, content=b"Server Error"))
            http = make_http()
            with pytest.raises(BokaMeraHTTPError) as exc_info:
                http.get("/services")
            http.close()
        assert exc_info.value.status_code == 500

    def test_200_does_not_raise(self):
        with respx.mock:
            respx.get(f"{BASE}/services").mock(return_value=httpx.Response(200, json=[]))
            http = make_http()
            result = http.get("/services")
            http.close()
        assert result == []

    def test_error_message_from_response_status(self):
        with respx.mock:
            respx.get(f"{BASE}/services").mock(
                return_value=httpx.Response(
                    400, json={"ResponseStatus": {"Message": "Field required"}}
                )
            )
            http = make_http()
            with pytest.raises(BokaMeraValidationError) as exc_info:
                http.get("/services")
            http.close()
        assert exc_info.value.message == "Field required"

    def test_is_subclass_of_base_http_error(self):
        with respx.mock:
            respx.get(f"{BASE}/services").mock(return_value=httpx.Response(404, content=b"nf"))
            http = make_http()
            with pytest.raises(BokaMeraHTTPError):
                http.get("/services")
            http.close()
