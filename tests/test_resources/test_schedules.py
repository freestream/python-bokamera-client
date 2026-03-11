"""Tests for ScheduleResource."""

from __future__ import annotations

import json
from datetime import date, time

import httpx
import respx

from bokamera._client import BokaMeraHTTPClient
from bokamera.resources.schedules import ScheduleResource

BASE = "https://api.bokamera.se"
COMPANY_UUID = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"


def make_http() -> BokaMeraHTTPClient:
    return BokaMeraHTTPClient(api_key="test-key", base_url=BASE)


# ---------------------------------------------------------------------------
# list_date
# ---------------------------------------------------------------------------


def test_schedules_list_date():
    with respx.mock:
        route = respx.get(f"{BASE}/schedules/date").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {"Id": 1, "Name": "Sommarschema", "Active": True, "ScheduleDates": []},
                ],
            )
        )
        http = make_http()
        results = ScheduleResource(http).list_date(company_id=COMPANY_UUID)
        http.close()
    assert route.called
    assert len(results) == 1
    assert results[0].id == 1
    assert results[0].name == "Sommarschema"
    assert results[0].active is True


def test_schedules_list_date_empty():
    with respx.mock:
        respx.get(f"{BASE}/schedules/date").mock(
            return_value=httpx.Response(200, json=[])
        )
        http = make_http()
        results = ScheduleResource(http).list_date(company_id=COMPANY_UUID)
        http.close()
    assert results == []


# ---------------------------------------------------------------------------
# create_date
# ---------------------------------------------------------------------------


def test_schedules_create_date():
    with respx.mock:
        route = respx.post(f"{BASE}/schedules/date").mock(
            return_value=httpx.Response(
                200,
                json={"Id": 10, "Name": "Veckans schema", "Active": True, "ScheduleDates": []},
            )
        )
        http = make_http()
        result = ScheduleResource(http).create_date(
            name="Veckans schema",
            company_id=COMPANY_UUID,
        )
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["Name"] == "Veckans schema"
    assert body["Active"] is True
    assert result.id == 10
    assert result.name == "Veckans schema"


# ---------------------------------------------------------------------------
# update_date
# ---------------------------------------------------------------------------


def test_schedules_update_date():
    with respx.mock:
        route = respx.put(f"{BASE}/schedules/date/10").mock(
            return_value=httpx.Response(
                200,
                json={"Id": 10, "Name": "Uppdaterat schema", "Active": False, "ScheduleDates": []},
            )
        )
        http = make_http()
        result = ScheduleResource(http).update_date(10, company_id=COMPANY_UUID, Active=False, Name="Uppdaterat schema")
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["Active"] is False
    assert result.active is False


# ---------------------------------------------------------------------------
# delete_date
# ---------------------------------------------------------------------------


def test_schedules_delete_date():
    with respx.mock:
        route = respx.delete(f"{BASE}/schedules/date/10").mock(
            return_value=httpx.Response(
                200,
                json={"Id": 10, "Name": "Deleted", "Active": False, "ScheduleDates": []},
            )
        )
        http = make_http()
        result = ScheduleResource(http).delete_date(10, company_id=COMPANY_UUID)
        http.close()
    assert route.called
    assert result.id == 10


# ---------------------------------------------------------------------------
# create_recurring
# ---------------------------------------------------------------------------


def test_schedules_create_recurring():
    with respx.mock:
        route = respx.post(f"{BASE}/schedules/recurring").mock(
            return_value=httpx.Response(
                200,
                json={
                    "Id": 20,
                    "Name": "Vardagar",
                    "Active": True,
                    "TimeInterval": 60,
                    "ValidFrom": "2026-01-01",
                    "ValidTo": "2026-12-31",
                    "StartTime": "08:00:00",
                    "EndTime": "17:00:00",
                    "DaysOfWeek": [1, 2, 3, 4, 5],
                },
            )
        )
        http = make_http()
        result = ScheduleResource(http).create_recurring(
            name="Vardagar",
            time_interval=60,
            valid_from=date(2026, 1, 1),
            valid_to=date(2026, 12, 31),
            start_time=time(8, 0),
            end_time=time(17, 0),
            days_of_week=[1, 2, 3, 4, 5],
            company_id=COMPANY_UUID,
        )
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["Name"] == "Vardagar"
    assert body["TimeInterval"] == 60
    assert body["ValidFrom"] == "2026-01-01"
    assert body["StartTime"] == "08:00:00"
    assert body["DaysOfWeek"] == [1, 2, 3, 4, 5]
    assert result.id == 20
    assert result.time_interval == 60
    assert result.days_of_week == [1, 2, 3, 4, 5]


# ---------------------------------------------------------------------------
# update_recurring / delete_recurring
# ---------------------------------------------------------------------------


def test_schedules_update_recurring():
    with respx.mock:
        route = respx.put(f"{BASE}/schedules/recurring/20").mock(
            return_value=httpx.Response(
                200,
                json={"Id": 20, "Name": "Uppdaterat", "Active": True, "DaysOfWeek": [1, 2, 3]},
            )
        )
        http = make_http()
        result = ScheduleResource(http).update_recurring(20, company_id=COMPANY_UUID, Name="Uppdaterat")
        http.close()
    body = json.loads(route.calls[0].request.content)
    assert body["Name"] == "Uppdaterat"
    assert result.id == 20


def test_schedules_delete_recurring():
    with respx.mock:
        route = respx.delete(f"{BASE}/schedules/recurring/20").mock(
            return_value=httpx.Response(
                200,
                json={"Id": 20, "Name": "Deleted", "Active": False, "DaysOfWeek": []},
            )
        )
        http = make_http()
        result = ScheduleResource(http).delete_recurring(20, company_id=COMPANY_UUID)
        http.close()
    assert route.called
    assert result.id == 20
