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
class BookingTag:
    """A tag attached to a booking or customer.

    Attributes:
        id: Tag ID.
        name: Display name of the tag.
        color: Hex colour string for the tag.
        active: Whether the tag is active.
    """

    id: int | None = None
    name: str | None = None
    color: str | None = None
    active: bool | None = None

    @classmethod
    def from_dict(cls, d: dict) -> BookingTag:
        """Construct a BookingTag from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            name=d.get("Name"),
            color=d.get("Color"),
            active=d.get("Active"),
        )


@dataclass(slots=True)
class BookingCustomer:
    """Customer details embedded inside a booking.

    Attributes:
        id: UUID of the customer profile.
        firstname: Customer first name.
        lastname: Customer last name.
        email: Customer email address.
        phone: Customer phone number.
        facebook_user_name: Facebook username if linked.
        image_url: URL to the customer's profile image.
        personal_identity_number: National identity number (e.g. Swedish personnummer).
        corporate_identity_number: Corporate identity number if applicable.
        invoice_address1: Primary invoice street address.
        invoice_address2: Secondary invoice street address.
        invoice_city: Invoice city.
        invoice_postal_code: Invoice postal code.
        invoice_country_code: ISO country code for the invoice address.
        tags: Tags assigned to the customer.
    """

    id: UUID | None = None
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    phone: str | None = None
    facebook_user_name: str | None = None
    image_url: str | None = None
    personal_identity_number: str | None = None
    corporate_identity_number: str | None = None
    invoice_address1: str | None = None
    invoice_address2: str | None = None
    invoice_city: str | None = None
    invoice_postal_code: str | None = None
    invoice_country_code: str | None = None
    tags: list[BookingTag] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> BookingCustomer:
        """Construct a BookingCustomer from a raw API response dict."""
        return cls(
            id=_uuid(d.get("Id")),
            firstname=d.get("Firstname"),
            lastname=d.get("Lastname"),
            email=d.get("Email"),
            phone=d.get("Phone"),
            facebook_user_name=d.get("FacebookUserName"),
            image_url=d.get("ImageUrl"),
            personal_identity_number=d.get("PersonalIdentityNumber"),
            corporate_identity_number=d.get("CorporateIdentityNumber"),
            invoice_address1=d.get("InvoiceAddress1"),
            invoice_address2=d.get("InvoiceAddress2"),
            invoice_city=d.get("InvoiceCity"),
            invoice_postal_code=d.get("InvoicePostalCode"),
            invoice_country_code=d.get("InvoiceCountryCode"),
            tags=[BookingTag.from_dict(t) for t in d.get("Tags", [])],
        )

    def to_dict(self) -> dict:
        return {k: v for k, v in {
            "Id": str(self.id) if self.id else None,
            "Firstname": self.firstname,
            "Lastname": self.lastname,
            "Email": self.email,
            "Phone": self.phone,
        }.items() if v is not None}


@dataclass(slots=True)
class BookingQuantity:
    """A quantity line associated with a booking (e.g. number of participants).

    Attributes:
        id: ID of the quantity/price category.
        quantity: Number of units booked for this category.
        price: Unit price applied to this quantity line.
        price_before_rebate: Price before any rebate code was applied.
        currency_id: ISO 4217 currency code for the price.
        price_sign: Display symbol for the currency (e.g. ``"kr"``).
        category: Name of the price category.
        vat: VAT percentage applied to this quantity line.
        price_text: Formatted price string for display.
        occupies_spot: Whether this quantity counts against the service's capacity.
    """

    id: int | None = None
    quantity: int = 1
    price: float | None = None
    price_before_rebate: float | None = None
    currency_id: str | None = None
    price_sign: str | None = None
    category: str | None = None
    vat: float | None = None
    price_text: str | None = None
    occupies_spot: bool | None = None

    @classmethod
    def from_dict(cls, d: dict) -> BookingQuantity:
        """Construct a BookingQuantity from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            quantity=d.get("Quantity", 1),
            price=d.get("Price"),
            price_before_rebate=d.get("PriceBeforeRebate"),
            currency_id=d.get("CurrencyId"),
            price_sign=d.get("PriceSign"),
            category=d.get("Category"),
            vat=d.get("VAT"),
            price_text=d.get("PriceText"),
            occupies_spot=d.get("OccupiesSpot"),
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
        icon: Icon identifier for the status.
        color: Hex colour string for the status.
    """

    id: int | None = None
    name: str | None = None
    description: str | None = None
    icon: str | None = None
    color: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> BookingStatusResponse:
        """Construct a BookingStatusResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            name=d.get("Name"),
            description=d.get("Description"),
            icon=d.get("Icon"),
            color=d.get("Color"),
        )


@dataclass(slots=True)
class BookingInvoiceAddress:
    """Invoice address attached directly to a booking.

    Attributes:
        invoice_address_id: ID of the invoice address record.
        user_id: UUID of the user who owns this address.
        corporate_identity_number: Corporate identity number for the invoice.
        invoice_address1: Primary street address.
        invoice_address2: Secondary street address.
        invoice_city: City.
        invoice_postal_code: Postal code.
        invoice_country_code: ISO country code.
    """

    invoice_address_id: str | None = None
    user_id: str | None = None
    corporate_identity_number: str | None = None
    invoice_address1: str | None = None
    invoice_address2: str | None = None
    invoice_city: str | None = None
    invoice_postal_code: str | None = None
    invoice_country_code: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> BookingInvoiceAddress:
        """Construct a BookingInvoiceAddress from a raw API response dict."""
        return cls(
            invoice_address_id=d.get("InvoiceAddressId"),
            user_id=d.get("UserId"),
            corporate_identity_number=d.get("CorporateIdentityNumber"),
            invoice_address1=d.get("InvoiceAddress1"),
            invoice_address2=d.get("InvoiceAddress2"),
            invoice_city=d.get("InvoiceCity"),
            invoice_postal_code=d.get("InvoicePostalCode"),
            invoice_country_code=d.get("InvoiceCountryCode"),
        )


@dataclass(slots=True)
class BookingLogResponse:
    """A single audit log entry for a booking.

    Attributes:
        id: Log entry ID.
        booking_id: ID of the booking this entry belongs to.
        event_type_id: Numeric identifier of the event type.
        event_type_name: Human-readable name of the event type.
        event_type_description: Description of the event type.
        comments: Optional free-text comment attached to this log entry.
        user_name: Username or identifier of who triggered the event.
        created: Timestamp when the event occurred.
    """

    id: int | None = None
    booking_id: int | None = None
    event_type_id: int | None = None
    event_type_name: str | None = None
    event_type_description: str | None = None
    comments: str | None = None
    user_name: str | None = None
    created: datetime | None = None

    @classmethod
    def from_dict(cls, d: dict) -> BookingLogResponse:
        """Construct a BookingLogResponse from a raw API response dict."""
        event_type = d.get("EventType") or {}
        return cls(
            id=d.get("Id"),
            booking_id=d.get("BookingId"),
            event_type_id=d.get("EventTypeId"),
            event_type_name=event_type.get("Name") if isinstance(event_type, dict) else event_type,
            event_type_description=event_type.get("Description") if isinstance(event_type, dict) else None,
            comments=d.get("Comments"),
            user_name=d.get("UserName"),
            created=_dt(d.get("Created")),
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
        status: Status string from the API.
        status_name: Human-readable status name.
        status_info: Full status details including icon and colour.
        send_email_reminder: Whether an email reminder is configured.
        send_sms_reminder: Whether an SMS reminder is configured.
        send_sms_confirmation: Whether an SMS confirmation is sent.
        send_email_confirmation: Whether an email confirmation is sent.
        last_time_to_un_book: Deadline for the customer to cancel self-service.
        service_id: ID of the booked service.
        service_name: Name of the booked service.
        customer: Customer details embedded in the booking.
        quantities: Quantity lines (e.g. number of participants per category).
        booked_resource_types: Resource types and their assigned resources.
        company: Company details dict.
        custom_field_values: Custom field values collected at booking time.
        invoice_address: Invoice address attached to the booking.
        payment_expiration: When the pending payment expires.
        log: Audit log entries for this booking.
        payment_log: Payment transactions associated with this booking.
        checkout_log: Checkout session log entries.
        external_reference: External reference records linked to this booking.
        length_in_minutes: Duration of the booking in minutes.
        booked_by: Username of who created the booking.
        booked_comments: Internal comments added at booking time.
        unbooked_comments: Reason for cancellation, if applicable.
        comments_to_customer: Comments visible to the customer.
        created: Timestamp when the booking was created.
        updated: Timestamp of the most recent modification.
        unbooked_on: Timestamp when the booking was cancelled, if applicable.
        cancellation_code: Code that can be used for self-service cancellation.
        rating_code: Token used to submit a customer rating for this booking.
        google_meet_url: Google Meet URL if a video meeting is attached.
        tags: Tags assigned to this booking.
        total_price: Total price charged for the booking.
    """

    id: int | None = None
    company_id: UUID | None = None
    from_: datetime | None = None
    to: datetime | None = None
    status_id: int | None = None
    status: str | None = None
    status_name: str | None = None
    status_info: BookingStatusResponse | None = None
    send_email_reminder: bool | None = None
    send_sms_reminder: bool | None = None
    send_sms_confirmation: bool | None = None
    send_email_confirmation: bool | None = None
    last_time_to_un_book: datetime | None = None
    service_id: int | None = None
    service_name: str | None = None
    customer: BookingCustomer | None = None
    quantities: list[BookingQuantity] = field(default_factory=list)
    booked_resource_types: list[dict] = field(default_factory=list)
    company: dict = field(default_factory=dict)
    custom_field_values: list[CustomFieldValue] = field(default_factory=list)
    invoice_address: BookingInvoiceAddress | None = None
    payment_expiration: datetime | None = None
    log: list[BookingLogResponse] = field(default_factory=list)
    payment_log: list[dict] = field(default_factory=list)
    checkout_log: list[dict] = field(default_factory=list)
    external_reference: list[dict] = field(default_factory=list)
    length_in_minutes: int | None = None
    booked_by: str | None = None
    booked_comments: str | None = None
    unbooked_comments: str | None = None
    comments_to_customer: str | None = None
    created: datetime | None = None
    updated: datetime | None = None
    unbooked_on: datetime | None = None
    cancellation_code: str | None = None
    rating_code: str | None = None
    google_meet_url: str | None = None
    tags: list[BookingTag] = field(default_factory=list)
    total_price: float | None = None

    @classmethod
    def from_dict(cls, d: dict) -> BookingResponse:
        """Construct a BookingResponse from a raw API response dict."""
        service = d.get("Service") or {}
        return cls(
            id=d.get("Id"),
            company_id=_uuid(d.get("CompanyId")),
            from_=_dt(d.get("From")),
            to=_dt(d.get("To")),
            status_id=d.get("StatusId"),
            status=d.get("Status"),
            status_name=d.get("StatusName"),
            status_info=BookingStatusResponse.from_dict(d["StatusInfo"]) if d.get("StatusInfo") else None,
            send_email_reminder=d.get("SendEmailReminder"),
            send_sms_reminder=d.get("SendSmsReminder"),
            send_sms_confirmation=d.get("SendSmsConfirmation"),
            send_email_confirmation=d.get("SendEmailConfirmation"),
            last_time_to_un_book=_dt(d.get("LastTimeToUnBook")),
            service_id=service.get("Id") if isinstance(service, dict) else d.get("ServiceId"),
            service_name=service.get("Name") if isinstance(service, dict) else d.get("ServiceName"),
            customer=BookingCustomer.from_dict(d["Customer"]) if d.get("Customer") else None,
            quantities=[BookingQuantity.from_dict(q) for q in d.get("Quantities", [])],
            booked_resource_types=d.get("BookedResourceTypes", []),
            company=d.get("Company") or {},
            custom_field_values=[CustomFieldValue.from_dict(c) for c in d.get("CustomFieldValues", [])],
            invoice_address=BookingInvoiceAddress.from_dict(d["InvoiceAddress"]) if d.get("InvoiceAddress") else None,
            payment_expiration=_dt(d.get("PaymentExpiration")),
            log=[BookingLogResponse.from_dict(e) for e in d.get("Log", [])],
            payment_log=d.get("PaymentLog", []),
            checkout_log=d.get("CheckoutLog", []),
            external_reference=d.get("ExternalReference", []),
            length_in_minutes=d.get("LengthInMinutes"),
            booked_by=d.get("BookedBy"),
            booked_comments=d.get("BookedComments"),
            unbooked_comments=d.get("UnbookedComments"),
            comments_to_customer=d.get("CommentsToCustomer"),
            created=_dt(d.get("CreatedDate") or d.get("Created")),
            updated=_dt(d.get("UpdatedDate") or d.get("Updated")),
            unbooked_on=_dt(d.get("UnbookedOn")),
            cancellation_code=d.get("CancellationCode"),
            rating_code=d.get("RatingCode"),
            google_meet_url=d.get("GoogleMeetUrl"),
            tags=[BookingTag.from_dict(t) for t in d.get("Tags", [])],
            total_price=d.get("TotalPrice"),
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
