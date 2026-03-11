"""
Data models for the GDPR resource.

Contains dataclasses for complete customer data exports and for customers
who have been inactive (no bookings) for a configurable period.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from .common import _dt, _uuid


@dataclass(slots=True)
class GDPRCustomerResponse:
    """All personal data held about a customer, returned for GDPR data export requests.

    Attributes:
        customer_id: UUID of the customer whose data was exported.
        bookings: All bookings associated with this customer.
        message_log: All messages (email, SMS) sent to this customer.
        user_profile: User account profile data, if the customer has an account.
        customer: Customer profile data dict.
        customer_comment: Internal comments stored against this customer.
        newsletter_log: Newsletter subscription and activity log entries.
    """

    customer_id: UUID | None = None
    bookings: list[dict] = field(default_factory=list)
    message_log: list[dict] = field(default_factory=list)
    user_profile: dict | None = None
    customer: dict | None = None
    customer_comment: list[dict] = field(default_factory=list)
    newsletter_log: list[dict] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> GDPRCustomerResponse:
        """Construct a GDPRCustomerResponse from a raw API response dict."""
        return cls(
            customer_id=_uuid(d.get("CustomerId")),
            bookings=d.get("Bookings", []),
            message_log=d.get("MessageLog", []),
            user_profile=d.get("UserProfile"),
            customer=d.get("Customer"),
            customer_comment=d.get("CustomerComment", []),
            newsletter_log=d.get("NewsletterLog", []),
        )


@dataclass(slots=True)
class InactiveCustomerResponse:
    """A customer who has not made a booking since a given cut-off date.

    Used to identify customers eligible for GDPR data removal.

    Attributes:
        id: UUID of the inactive customer.
        firstname: Customer's first name.
        lastname: Customer's last name.
        email: Customer's email address.
        last_booking: Timestamp of the most recent booking made by this customer.
    """

    id: UUID | None = None
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    last_booking: datetime | None = None

    @classmethod
    def from_dict(cls, d: dict) -> InactiveCustomerResponse:
        """Construct a InactiveCustomerResponse from a raw API response dict."""
        return cls(
            id=_uuid(d.get("Id")),
            firstname=d.get("Firstname"),
            lastname=d.get("Lastname"),
            email=d.get("Email"),
            last_booking=_dt(d.get("LastBooking")),
        )
