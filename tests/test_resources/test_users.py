"""Tests for UserResource."""

from __future__ import annotations

import json

import httpx
import respx

from bokamera._client import BokaMeraHTTPClient
from bokamera.resources.users import UserResource

BASE = "https://api.bokamera.se"
USER_UUID = "cccccccc-dddd-eeee-ffff-000000000000"


def make_http() -> BokaMeraHTTPClient:
    return BokaMeraHTTPClient(api_key="test-key", base_url=BASE)


# ---------------------------------------------------------------------------
# get_current
# ---------------------------------------------------------------------------


def test_users_get_current():
    with respx.mock:
        route = respx.get(f"{BASE}/users").mock(
            return_value=httpx.Response(
                200,
                json={
                    "UserId": USER_UUID,
                    "UserProfile": {
                        "UserId": USER_UUID,
                        "Firstname": "Lisa",
                        "Lastname": "Larsson",
                        "Email": "lisa@example.com",
                    },
                },
            )
        )
        http = make_http()
        result = UserResource(http).get_current()
        http.close()
    assert route.called
    assert str(result.user_id) == USER_UUID
    assert result.user_profile is not None
    assert result.user_profile.firstname == "Lisa"


# ---------------------------------------------------------------------------
# create
# ---------------------------------------------------------------------------


def test_users_create():
    with respx.mock:
        route = respx.post(f"{BASE}/users").mock(
            return_value=httpx.Response(
                200,
                json={
                    "Id": 1,
                    "UserId": USER_UUID,
                    "Email": "new@example.com",
                },
            )
        )
        http = make_http()
        result = UserResource(http).create(
            firstname="Erik",
            lastname="Eriksson",
            email="new@example.com",
            phone="+46701234567",
        )
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["Firstname"] == "Erik"
    assert body["Email"] == "new@example.com"
    assert result.email == "new@example.com"
    assert str(result.user_id) == USER_UUID


# ---------------------------------------------------------------------------
# delete
# ---------------------------------------------------------------------------


def test_users_delete():
    with respx.mock:
        route = respx.delete(f"{BASE}/users").mock(
            return_value=httpx.Response(200, json={"Deleted": True})
        )
        http = make_http()
        result = UserResource(http).delete(
            username="old@example.com",
            realm="BokaMera",
        )
        http.close()
    assert route.called
    params = route.calls[0].request.url.params
    assert params["UserName"] == "old@example.com"
    assert result["Deleted"] is True


# ---------------------------------------------------------------------------
# get_agreement / accept_agreement
# ---------------------------------------------------------------------------


def test_users_get_agreement():
    with respx.mock:
        route = respx.get(f"{BASE}/users/agreement").mock(
            return_value=httpx.Response(
                200,
                json={"Id": 5, "UserId": USER_UUID, "AgreementId": 2, "Accepted": True},
            )
        )
        http = make_http()
        result = UserResource(http).get_agreement(user_id=USER_UUID)
        http.close()
    assert route.called
    assert result.id == 5
    assert result.accepted is True


def test_users_accept_agreement():
    with respx.mock:
        route = respx.post(f"{BASE}/users/agreement").mock(
            return_value=httpx.Response(
                200,
                json={"Id": 6, "UserId": USER_UUID, "AgreementId": 3, "Accepted": True},
            )
        )
        http = make_http()
        result = UserResource(http).accept_agreement(user_id=USER_UUID, agreement_id=3)
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["AgreementId"] == 3
    assert result.accepted is True


# ---------------------------------------------------------------------------
# forgot_password / confirm_email
# ---------------------------------------------------------------------------


def test_users_forgot_password():
    with respx.mock:
        route = respx.post(f"{BASE}/users/forgotpassword").mock(
            return_value=httpx.Response(200, json={"Sent": True})
        )
        http = make_http()
        result = UserResource(http).forgot_password(email="user@example.com", realm="BokaMera")
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["Email"] == "user@example.com"
    assert result["Sent"] is True


def test_users_confirm_email():
    with respx.mock:
        route = respx.post(f"{BASE}/users/confirmemail").mock(
            return_value=httpx.Response(200, json={"Confirmed": True})
        )
        http = make_http()
        result = UserResource(http).confirm_email(token="tok123", realm="BokaMera")
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["Token"] == "tok123"
    assert result["Confirmed"] is True


# ---------------------------------------------------------------------------
# add_favorite / remove_favorite
# ---------------------------------------------------------------------------


def test_users_add_favorite():
    company = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    with respx.mock:
        route = respx.post(f"{BASE}/users/favorite").mock(
            return_value=httpx.Response(200, json={"Added": True})
        )
        http = make_http()
        result = UserResource(http).add_favorite(company)
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["CompanyId"] == company
    assert result["Added"] is True


def test_users_remove_favorite():
    company = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    with respx.mock:
        route = respx.delete(f"{BASE}/users/favorite").mock(
            return_value=httpx.Response(200, json={"Removed": True})
        )
        http = make_http()
        result = UserResource(http).remove_favorite(company)
        http.close()
    assert route.called
    assert result["Removed"] is True


# ---------------------------------------------------------------------------
# list_agreements
# ---------------------------------------------------------------------------


def test_users_list_agreements():
    with respx.mock:
        respx.get(f"{BASE}/agreements").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {"Id": 1, "Name": "Terms of Service", "Version": "1.0"},
                    {"Id": 2, "Name": "Privacy Policy", "Version": "2.0"},
                ],
            )
        )
        http = make_http()
        results = UserResource(http).list_agreements()
        http.close()
    assert len(results) == 2
    assert results[0].id == 1
    assert results[0].name == "Terms of Service"
    assert results[1].version == "2.0"
