"""
Data models for the bookings, booking log, booking queue, and reports resources.

Includes enumerations for payment options and receipt methods, as well as
dataclasses for booking responses, queue entries, log entries, reports, and
printout configurations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import IntEnum
from uuid import UUID

from .common import CustomFieldValue, _dt, _uuid


class PaymentOption(IntEnum):
    """Payment behaviour to apply when creating or approving a booking."""

    DEFAULT_SETTING = 0
    BOOK_WITHOUT_PAYMENT = 1
    BOOK_WITH_PAYMENT_MESSAGE_TO_CUSTOMER = 2
    BOOK_WITH_MANUAL_PAYMENT = 3


class SendReceiptMethod(IntEnum):
    """Delivery method for booking receipts and reports."""

    EMAIL = 1
    PDF_EXPORT = 2


class BookingStatus(IntEnum):
    """Status of a booking."""

    BOOKED = 1
    UNBOOKED = 2
    RESERVED = 3
    CANCELED = 4
    AWAITING_PAYMENT = 5
    AWAITING_PAYMENT_NO_TIME_LIMIT = 6
    PAYED = 7
    AWAITING_PAYMENT_REQUEST_FROM_ADMIN = 8
    AWAITING_PAYMENT_FROM_PROVIDER = 9
    INVOICED = 10


@dataclass(slots=True)
class BookingCustomer:
    """Customer details embedded inside a booking.

    Attributes:
        firstname: Customer first name.
        lastname: Customer last name.
        email: Customer email address.
        phone: Customer phone number.
        customer_id: UUID of the linked customer profile, if any.
    """

    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    phone: str | None = None
    customer_id: UUID | None = None

    @classmethod
    def from_dict(cls, d: dict) -> BookingCustomer:
        """Construct a BookingCustomer from a raw API response dict."""
        return cls(
            firstname=d.get("Firstname"),
            lastname=d.get("Lastname"),
            email=d.get("Email"),
            phone=d.get("Phone"),
            customer_id=_uuid(d.get("CustomerId")),
        )

    def to_dict(self) -> dict:
        return {k: v for k, v in {
            "Firstname": self.firstname,
            "Lastname": self.lastname,
            "Email": self.email,
            "Phone": self.phone,
            "CustomerId": str(self.customer_id) if self.customer_id else None,
        }.items() if v is not None}


@dataclass(slots=True)
class BookingQuantity:
    """A quantity line associated with a booking (e.g. number of participants).

    Attributes:
        id: ID of the quantity/price category.
        quantity: Number of units booked for this category.
        price: Unit price applied to this quantity line.
        vat: VAT percentage applied to this quantity line.
    """

    id: int | None = None
    quantity: int = 1
    price: float | None = None
    vat: float | None = None

    @classmethod
    def from_dict(cls, d: dict) -> BookingQuantity:
        """Construct a BookingQuantity from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            quantity=d.get("Quantity", 1),
            price=d.get("Price"),
            vat=d.get("VAT"),
        )

    def to_dict(self) -> dict:
        return {k: v for k, v in {
            "Id": self.id,
            "Quantity": self.quantity,
            "Price": self.price,
            "VAT": self.vat,
        }.items() if v is not None}


@dataclass(slots=True)
class BookingStatusResponse:
    """A booking status option (e.g. Confirmed, Pending, Cancelled).

    Attributes:
        id: Numeric status ID.
        name: Short status name.
        description: Longer human-readable description.
    """

    id: int | None = None
    name: str | None = None
    description: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> BookingStatusResponse:
        """Construct a BookingStatusResponse from a raw API response dict."""
        return cls(id=d.get("Id"), name=d.get("Name"), description=d.get("Description"))


@dataclass(slots=True)
class BookingLogResponse:
    """A single audit log entry for a booking.

    Attributes:
        id: Log entry ID.
        booking_id: ID of the booking this entry belongs to.
        event_type_id: Numeric identifier of the event type.
        event_type: Human-readable event type name.
        comments: Optional free-text comment attached to this log entry.
        created: Timestamp when the event occurred.
        updated_by: Username or identifier of who triggered the event.
    """

    id: int | None = None
    booking_id: int | None = None
    event_type_id: int | None = None
    event_type: str | None = None
    comments: str | None = None
    created: datetime | None = None
    updated_by: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> BookingLogResponse:
        """Construct a BookingLogResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            booking_id=d.get("BookingId"),
            event_type_id=d.get("EventTypeId"),
            event_type=d.get("EventType"),
            comments=d.get("Comments"),
            created=_dt(d.get("Created")),
            updated_by=d.get("UpdatedBy"),
        )


@dataclass(slots=True)
class BookingResponse:
    """Full representation of a booking returned by the API.

    Attributes:
        id: Numeric booking ID.
        company_id: UUID of the company that owns the booking.
        from_: Start date and time of the booking.
        to: End date and time of the booking.
        status_id: Numeric status code.
        status: Human-readable status name.
        service_id: ID of the booked service.
        service_name: Name of the booked service.
        customer: Customer details embedded in the booking.
        quantities: Quantity lines (e.g. number of participants per category).
        resources: List of resource dicts assigned to this booking.
        custom_fields: Custom field values collected at booking time.
        payment_log: Payment transactions associated with this booking.
        unbooked_on: Timestamp when the booking was cancelled, if applicable.
        unbooked_comments: Reason for cancellation, if applicable.
        created: Timestamp when the booking was created.
        updated: Timestamp of the most recent modification.
        total_price: Total price charged for the booking.
        cancellation_code: Code that can be used for self-service cancellation.
    """

    id: int | None = None
    company_id: UUID | None = None
    from_: datetime | None = None
    to: datetime | None = None
    status_id: int | None = None
    status: str | None = None
    service_id: int | None = None
    service_name: str | None = None
    customer: BookingCustomer | None = None
    quantities: list[BookingQuantity] = field(default_factory=list)
    resources: list[dict] = field(default_factory=list)
    custom_fields: list[CustomFieldValue] = field(default_factory=list)
    payment_log: list[dict] = field(default_factory=list)
    unbooked_on: datetime | None = None
    unbooked_comments: str | None = None
    created: datetime | None = None
    updated: datetime | None = None
    total_price: float | None = None
    cancellation_code: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> BookingResponse:
        """Construct a BookingResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            company_id=_uuid(d.get("CompanyId")),
            from_=_dt(d.get("From")),
            to=_dt(d.get("To")),
            status_id=d.get("StatusId"),
            status=d.get("Status"),
            service_id=d.get("ServiceId"),
            service_name=d.get("ServiceName"),
            customer=BookingCustomer.from_dict(d["Customer"]) if d.get("Customer") else None,
            quantities=[BookingQuantity.from_dict(q) for q in d.get("Quantities", [])],
            resources=d.get("Resources", []),
            custom_fields=[CustomFieldValue.from_dict(c) for c in d.get("CustomFields", [])],
            payment_log=d.get("PaymentLog", []),
            unbooked_on=_dt(d.get("UnbookedOn")),
            unbooked_comments=d.get("UnbookedComments"),
            created=_dt(d.get("Created")),
            updated=_dt(d.get("Updated")),
            total_price=d.get("TotalPrice"),
            cancellation_code=d.get("CancellationCode"),
        )


@dataclass(slots=True)
class GroupedBookingResponse:
    """A group of bookings sharing the same calendar date.

    Attributes:
        date: The date this group represents.
        bookings: All bookings that start on this date.
    """

    date: datetime | None = None
    bookings: list[BookingResponse] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> GroupedBookingResponse:
        """Construct a GroupedBookingResponse from a raw API response dict."""
        return cls(
            date=_dt(d.get("Date")),
            bookings=[BookingResponse.from_dict(b) for b in d.get("Bookings", [])],
        )


@dataclass(slots=True)
class BookingUserQueueResponse:
    """An entry in the booking waitlist queue for a service.

    Attributes:
        id: Queue entry ID.
        company_id: UUID of the company.
        service_id: ID of the service the customer is waiting for.
        customer_id: UUID of the customer in the queue.
        created: Timestamp when the customer joined the queue.
        custom_fields: Custom field values submitted when joining the queue.
    """

    id: int | None = None
    company_id: UUID | None = None
    service_id: int | None = None
    customer_id: UUID | None = None
    created: datetime | None = None
    custom_fields: list[CustomFieldValue] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> BookingUserQueueResponse:
        """Construct a BookingUserQueueResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            company_id=_uuid(d.get("CompanyId")),
            service_id=d.get("ServiceId"),
            customer_id=_uuid(d.get("CustomerId")),
            created=_dt(d.get("Created")),
            custom_fields=[CustomFieldValue.from_dict(c) for c in d.get("CustomFields", [])],
        )


@dataclass(slots=True)
class ReportResponse:
    """A booking report template available for a company.

    Attributes:
        id: Report template ID.
        name: Display name of the report.
        description: Short description of the report's content.
    """

    id: int | None = None
    name: str | None = None
    description: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> ReportResponse:
        """Construct a ReportResponse from a raw API response dict."""
        return cls(id=d.get("Id"), name=d.get("Name"), description=d.get("Description"))


@dataclass(slots=True)
class PrintoutResponse:
    """A booking printout (receipt/ticket) template configuration.

    Attributes:
        id: Printout template ID.
        name: Display name of the template.
        header_left_cell: Content rendered in the top-left header cell.
        header_middle_cell: Content rendered in the top-centre header cell.
        header_right_cell: Content rendered in the top-right header cell.
        body_cell: Main body content template.
        footer_left_cell: Content rendered in the bottom-left footer cell.
        footer_middle_cell: Content rendered in the bottom-centre footer cell.
        footer_right_cell: Content rendered in the bottom-right footer cell.
        language: BCP 47 language tag for this printout (e.g. ``"sv"``).
    """

    id: int | None = None
    name: str | None = None
    header_left_cell: str | None = None
    header_middle_cell: str | None = None
    header_right_cell: str | None = None
    body_cell: str | None = None
    footer_left_cell: str | None = None
    footer_middle_cell: str | None = None
    footer_right_cell: str | None = None
    language: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> PrintoutResponse:
        """Construct a PrintoutResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            name=d.get("Name"),
            header_left_cell=d.get("HeaderLeftCell"),
            header_middle_cell=d.get("HeaderMiddleCell"),
            header_right_cell=d.get("HeaderRightCell"),
            body_cell=d.get("BodyCell"),
            footer_left_cell=d.get("FooterLeftCell"),
            footer_middle_cell=d.get("FooterMiddleCell"),
            footer_right_cell=d.get("FooterRightCell"),
            language=d.get("Language"),
        )
