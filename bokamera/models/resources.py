"""
Data models for the resources, resource types, and time exceptions.

Contains dataclasses for resources (staff members, rooms, equipment), their
grouping types, time exception rules, and colliding booking responses.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time
from uuid import UUID

from .common import CustomFieldValue, _dt, _uuid


@dataclass(slots=True)
class ResourceResponse:
    """A bookable resource such as a staff member, room, or piece of equipment.

    Attributes:
        id: Numeric ID of the resource.
        name: Display name of the resource.
        description: Longer description of the resource.
        active: Whether the resource is currently available for booking.
        color: Hex colour code used to distinguish the resource in the calendar.
        email: Email address of the resource (e.g. staff member's email).
        mobile_phone: Mobile phone number of the resource.
        access_group: Optional access group label for code lock integrations.
        email_notification: Whether the resource receives email notifications for bookings.
        sms_notification: Whether the resource receives SMS notifications for bookings.
        send_email_reminder: Whether email reminders are sent to the resource.
        send_sms_reminder: Whether SMS reminders are sent to the resource.
        image_url: URL of the resource's profile image.
        custom_fields: Custom field values attached to this resource.
        schedules: Schedules defining when this resource is available.
        exceptions: Time exceptions (e.g. holidays) for this resource.
    """

    id: int | None = None
    name: str | None = None
    description: str | None = None
    active: bool = True
    color: str | None = None
    email: str | None = None
    mobile_phone: str | None = None
    access_group: str | None = None
    email_notification: bool = False
    sms_notification: bool = False
    send_email_reminder: bool = False
    send_sms_reminder: bool = False
    image_url: str | None = None
    custom_fields: list[CustomFieldValue] = field(default_factory=list)
    schedules: list[dict] = field(default_factory=list)
    exceptions: list[dict] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> ResourceResponse:
        """Construct a ResourceResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            name=d.get("Name"),
            description=d.get("Description"),
            active=d.get("Active", True),
            color=d.get("Color"),
            email=d.get("Email"),
            mobile_phone=d.get("MobilePhone"),
            access_group=d.get("AccessGroup"),
            email_notification=d.get("EmailNotification", False),
            sms_notification=d.get("SMSNotification", False),
            send_email_reminder=d.get("SendEmailReminder", False),
            send_sms_reminder=d.get("SendSMSReminder", False),
            image_url=d.get("ImageUrl"),
            custom_fields=[CustomFieldValue.from_dict(c) for c in d.get("CustomFields", [])],
            schedules=d.get("Schedules", []),
            exceptions=d.get("Exceptions", []),
        )


@dataclass(slots=True)
class ResourceTypeResponse:
    """A resource type that groups related resources together.

    Attributes:
        id: Resource type ID.
        name: Display name of the resource type.
        description: Longer description of this resource type.
        active: Whether this resource type is currently active.
        resources: The individual resources belonging to this type.
    """

    id: int | None = None
    name: str | None = None
    description: str | None = None
    active: bool = True
    resources: list[ResourceResponse] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> ResourceTypeResponse:
        """Construct a ResourceTypeResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            name=d.get("Name"),
            description=d.get("Description"),
            active=d.get("Active", True),
            resources=[ResourceResponse.from_dict(r) for r in d.get("Resources", [])],
        )


@dataclass(slots=True)
class ResourceTimeExceptionResponse:
    """A time exception that marks a resource as unavailable during a period.

    Time exceptions can be one-off (e.g. a specific holiday) or recurring
    (e.g. every Monday from 12:00–13:00).

    Attributes:
        id: Exception ID.
        from_: Start datetime of the exception window.
        to: End datetime of the exception window.
        from_time: Start time within each day (for recurring exceptions).
        to_time: End time within each day (for recurring exceptions).
        days_of_week: Days the recurring exception applies to (1 = Monday, 7 = Sunday).
        reason_text: Internal reason text (visible to administrators).
        reason_text_public: Customer-facing reason text.
        color: Hex colour used to highlight the exception in the calendar.
        block_time: Whether this exception actively blocks new bookings.
        is_recurring: Whether this is a recurring exception.
        resource_ids: IDs of all resources affected by this exception.
    """

    id: int | None = None
    from_: datetime | None = None
    to: datetime | None = None
    from_time: time | None = None
    to_time: time | None = None
    days_of_week: list[int] = field(default_factory=list)
    reason_text: str | None = None
    reason_text_public: str | None = None
    color: str | None = None
    block_time: bool = True
    is_recurring: bool = False
    resource_ids: list[int] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> ResourceTimeExceptionResponse:
        """Construct a ResourceTimeExceptionResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            from_=_dt(d.get("From")),
            to=_dt(d.get("To")),
            from_time=time.fromisoformat(d["FromTime"]) if d.get("FromTime") else None,
            to_time=time.fromisoformat(d["ToTime"]) if d.get("ToTime") else None,
            days_of_week=d.get("DaysOfWeek", []),
            reason_text=d.get("ReasonText"),
            reason_text_public=d.get("ReasonTextPublic"),
            color=d.get("Color"),
            block_time=d.get("BlockTime", True),
            is_recurring=d.get("IsRecurring", False),
            resource_ids=[r for r in d.get("ResourceIds", []) if r is not None],
        )


@dataclass(slots=True)
class CollidingBookingResponse:
    """Bookings and resources that would collide with a proposed time exception.

    Attributes:
        resource_ids: IDs of resources that have conflicting bookings.
        bookings: Booking dicts that overlap with the proposed exception window.
    """

    resource_ids: list[int] = field(default_factory=list)
    bookings: list[dict] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> CollidingBookingResponse:
        """Construct a CollidingBookingResponse from a raw API response dict."""
        return cls(
            resource_ids=[r for r in d.get("ResourceIds", []) if r is not None],
            bookings=d.get("Bookings", []),
        )
