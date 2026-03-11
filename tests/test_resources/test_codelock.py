"""Tests for CodeLockResource."""

from __future__ import annotations

import json

import httpx
import respx

from bokamera._client import BokaMeraHTTPClient
from bokamera.resources.codelock import CodeLockResource

BASE = "https://api.bokamera.se"
COMPANY_UUID = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"


def make_http() -> BokaMeraHTTPClient:
    return BokaMeraHTTPClient(api_key="test-key", base_url=BASE)


# ---------------------------------------------------------------------------
# get_settings / update_settings
# ---------------------------------------------------------------------------


def test_codelock_get_settings():
    with respx.mock:
        route = respx.get(f"{BASE}/codelock/settings").mock(
            return_value=httpx.Response(
                200,
                json={
                    "CompanyId": COMPANY_UUID,
                    "Active": True,
                    "CodeLockSystemsId": 3,
                    "CodeLockSystemName": "Accessy",
                },
            )
        )
        http = make_http()
        result = CodeLockResource(http).get_settings(company_id=COMPANY_UUID)
        http.close()
    assert route.called
    assert result.active is True
    assert result.code_lock_systems_id == 3
    assert result.code_lock_system_name == "Accessy"


def test_codelock_update_settings():
    with respx.mock:
        route = respx.put(f"{BASE}/codelock/settings").mock(
            return_value=httpx.Response(
                200,
                json={
                    "CompanyId": COMPANY_UUID,
                    "Active": False,
                    "CodeLockSystemsId": 1,
                    "CodeLockSystemName": "Zesec",
                },
            )
        )
        http = make_http()
        result = CodeLockResource(http).update_settings(
            active=False,
            code_lock_systems_id=1,
            company_id=COMPANY_UUID,
        )
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["Active"] is False
    assert body["CodeLockSystemsId"] == 1
    assert result.active is False


# ---------------------------------------------------------------------------
# Accessy
# ---------------------------------------------------------------------------


def test_codelock_get_accessy():
    with respx.mock:
        route = respx.get(f"{BASE}/codelock/accessy/settings").mock(
            return_value=httpx.Response(
                200,
                json={"ClientId": "client-abc", "ClientSecret": "secret-xyz"},
            )
        )
        http = make_http()
        result = CodeLockResource(http).get_accessy(company_id=COMPANY_UUID)
        http.close()
    assert route.called
    assert result.client_id == "client-abc"


def test_codelock_create_accessy():
    with respx.mock:
        route = respx.post(f"{BASE}/codelock/accessy/settings").mock(
            return_value=httpx.Response(
                200,
                json={"ClientId": "client-new", "ClientSecret": "secret-new"},
            )
        )
        http = make_http()
        result = CodeLockResource(http).create_accessy(
            client_id="client-new",
            client_secret="secret-new",
            company_id=COMPANY_UUID,
        )
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["ClientId"] == "client-new"
    assert body["ClientSecret"] == "secret-new"
    assert result.client_id == "client-new"


# ---------------------------------------------------------------------------
# Axema (has update)
# ---------------------------------------------------------------------------


def test_codelock_create_axema():
    with respx.mock:
        route = respx.post(f"{BASE}/codelock/axema/settings").mock(
            return_value=httpx.Response(
                200,
                json={"ApiEndpoint": "axema.local", "ApiPort": 8080, "Username": "admin"},
            )
        )
        http = make_http()
        result = CodeLockResource(http).create_axema(
            api_endpoint="axema.local",
            api_port=8080,
            username="admin",
            password="pass",
            company_id=COMPANY_UUID,
        )
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["ApiEndpoint"] == "axema.local"
    assert body["ApiPort"] == 8080
    assert result.api_endpoint == "axema.local"


def test_codelock_update_axema():
    with respx.mock:
        route = respx.put(f"{BASE}/codelock/axema/settings").mock(
            return_value=httpx.Response(
                200,
                json={"ApiEndpoint": "axema-new.local", "ApiPort": 9090, "Username": "admin"},
            )
        )
        http = make_http()
        result = CodeLockResource(http).update_axema(
            company_id=COMPANY_UUID,
            ApiEndpoint="axema-new.local",
            ApiPort=9090,
        )
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["ApiEndpoint"] == "axema-new.local"
    assert result.api_port == 9090


# ---------------------------------------------------------------------------
# Zesec (unlock)
# ---------------------------------------------------------------------------


def test_codelock_create_zesec():
    with respx.mock:
        route = respx.post(f"{BASE}/codelock/zesec/settings").mock(
            return_value=httpx.Response(
                200,
                json={"PhoneNumber": "+46701234567"},
            )
        )
        http = make_http()
        result = CodeLockResource(http).create_zesec(
            phone_number="+46701234567",
            password="secret",
            company_id=COMPANY_UUID,
        )
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["PhoneNumber"] == "+46701234567"
    assert result.phone_number == "+46701234567"


def test_codelock_zesec_unlock():
    with respx.mock:
        route = respx.post(f"{BASE}/codelock/zesec/unlock").mock(
            return_value=httpx.Response(200, json={"Status": "Unlocked"})
        )
        http = make_http()
        result = CodeLockResource(http).zesec_unlock(booking_id=42, company_id=COMPANY_UUID)
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["BookingId"] == 42
    assert result["Status"] == "Unlocked"


# ---------------------------------------------------------------------------
# delete_old_reservations
# ---------------------------------------------------------------------------


def test_codelock_delete_old_reservations():
    with respx.mock:
        route = respx.post(f"{BASE}/codelock/2/reservations/").mock(
            return_value=httpx.Response(200, json={"Deleted": 5})
        )
        http = make_http()
        result = CodeLockResource(http).delete_old_reservations(
            2,
            token="tok123",
            to="2026-01-01T00:00:00Z",
            company_id=COMPANY_UUID,
        )
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["Token"] == "tok123"
    assert result["Deleted"] == 5
