"""
Data models for the schedules resource.

Contains dataclasses for date schedules (explicit calendar dates) and recurring
schedules (weekly patterns with optional exceptions).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time
from uuid import UUID

from .common import _uuid


@dataclass(slots=True)
class ScheduleDate:
    """A single date entry within a date schedule.

    Attributes:
        date: The calendar date for this schedule entry.
        start_time: Opening time on this date.
        end_time: Closing time on this date.
    """

    date: date | None = None
    start_time: time | None = None
    end_time: time | None = None

    @classmethod
    def from_dict(cls, d: dict) -> ScheduleDate:
        """Construct a ScheduleDate from a raw API response dict."""
        return cls(
            date=date.fromisoformat(d["Date"]) if d.get("Date") else None,
            start_time=time.fromisoformat(d["StartTime"]) if d.get("StartTime") else None,
            end_time=time.fromisoformat(d["EndTime"]) if d.get("EndTime") else None,
        )

    def to_dict(self) -> dict:
        return {k: v for k, v in {
            "Date": self.date.isoformat() if self.date else None,
            "StartTime": self.start_time.isoformat() if self.start_time else None,
            "EndTime": self.end_time.isoformat() if self.end_time else None,
        }.items() if v is not None}


@dataclass(slots=True)
class DateScheduleResponse:
    """A schedule defined by explicit calendar dates and opening hours.

    Attributes:
        id: Schedule ID.
        name: Display name of the schedule.
        description: Optional longer description.
        active: Whether this schedule is currently active.
        number_of_schedule_days: Pre-computed count of individual schedule dates.
        schedule_dates: The explicit date/time entries for this schedule.
        resources: Resources connected to this schedule.
        services: Services connected to this schedule.
    """

    id: int | None = None
    name: str | None = None
    description: str | None = None
    active: bool = True
    number_of_schedule_days: int | None = None
    schedule_dates: list[ScheduleDate] = field(default_factory=list)
    resources: list[dict] = field(default_factory=list)
    services: list[dict] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> DateScheduleResponse:
        """Construct a DateScheduleResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            name=d.get("Name"),
            description=d.get("Description"),
            active=d.get("Active", True),
            number_of_schedule_days=d.get("NumberOfScheduleDays"),
            schedule_dates=[ScheduleDate.from_dict(s) for s in d.get("ScheduleDates", [])],
            resources=d.get("Resources", []),
            services=d.get("Services", []),
        )


@dataclass(slots=True)
class RecurringScheduleResponse:
    """A schedule defined by a weekly repeating pattern.

    Attributes:
        id: Schedule ID.
        name: Display name of the schedule.
        description: Optional longer description.
        active: Whether this schedule is currently active.
        time_interval: Slot duration in minutes used to split the daily window
            into individual bookable slots.
        valid_from: The first date this schedule is valid.
        valid_to: The last date this schedule is valid.
        start_time: Daily opening time.
        end_time: Daily closing time.
        days_of_week: Days on which this schedule applies (1 = Monday, 7 = Sunday).
        number_of_schedule_days: Pre-computed count of active days.
        enable_booking_until_closing_time: When True, booking is allowed up to
            (and including) the closing time slot.
        resources: Resources connected to this schedule.
        services: Services connected to this schedule.
        exceptions: Individual exception overrides within this schedule.
    """

    id: int | None = None
    name: str | None = None
    description: str | None = None
    active: bool = True
    time_interval: int | None = None
    valid_from: date | None = None
    valid_to: date | None = None
    start_time: time | None = None
    end_time: time | None = None
    days_of_week: list[int] = field(default_factory=list)
    number_of_schedule_days: int | None = None
    enable_booking_until_closing_time: bool = False
    resources: list[dict] = field(default_factory=list)
    services: list[dict] = field(default_factory=list)
    exceptions: list[dict] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> RecurringScheduleResponse:
        """Construct a RecurringScheduleResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            name=d.get("Name"),
            description=d.get("Description"),
            active=d.get("Active", True),
            time_interval=d.get("TimeInterval"),
            valid_from=date.fromisoformat(d["ValidFrom"]) if d.get("ValidFrom") else None,
            valid_to=date.fromisoformat(d["ValidTo"]) if d.get("ValidTo") else None,
            start_time=time.fromisoformat(d["StartTime"]) if d.get("StartTime") else None,
            end_time=time.fromisoformat(d["EndTime"]) if d.get("EndTime") else None,
            days_of_week=d.get("DaysOfWeek", []),
            number_of_schedule_days=d.get("NumberOfScheduleDays"),
            enable_booking_until_closing_time=d.get("EnableBookingUntilClosingTime", False),
            resources=d.get("Resources", []),
            services=d.get("Services", []),
            exceptions=d.get("Exceptions", []),
        )
