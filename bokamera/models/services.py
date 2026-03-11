"""
Data models for the services resource.

Contains dataclasses for service definitions, pricing rules, available time
slots, duration types, and price calculation results.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time
from uuid import UUID

from .common import CustomFieldValue, _date, _dt, _uuid


@dataclass(slots=True)
class ServicePriceResponse:
    """A price rule associated with a service.

    Price rules can be restricted to specific date ranges, time windows,
    or days of the week.

    Attributes:
        id: Price rule ID.
        service_id: ID of the owning service.
        price: Price amount in the specified currency.
        currency_id: ISO 4217 currency code.
        vat: VAT percentage applied to this price.
        category: Optional price category label.
        from_date: Start date from which this price is valid.
        to_date: End date until which this price is valid.
        from_time: Start time within the day from which this price applies.
        to_time: End time within the day until which this price applies.
        days_of_week: Days on which this price is active (1 = Monday, 7 = Sunday).
        calculation_type_id: Determines how the price is applied (e.g. per person, flat).
    """

    id: int | None = None
    service_id: int | None = None
    price: float | None = None
    currency_id: str | None = None
    vat: float | None = None
    category: str | None = None
    from_date: date | None = None
    to_date: date | None = None
    from_time: time | None = None
    to_time: time | None = None
    days_of_week: list[int] = field(default_factory=list)
    calculation_type_id: int | None = None

    @classmethod
    def from_dict(cls, d: dict) -> ServicePriceResponse:
        return cls(
            id=d.get("Id"),
            service_id=d.get("ServiceId"),
            price=d.get("Price"),
            currency_id=d.get("CurrencyId"),
            vat=d.get("VAT"),
            category=d.get("Category"),
            from_date=_date(d.get("From")),
            to_date=_date(d.get("To")),
            from_time=time.fromisoformat(d["FromTime"]) if d.get("FromTime") else None,
            to_time=time.fromisoformat(d["ToTime"]) if d.get("ToTime") else None,
            days_of_week=d.get("DaysOfWeek", []),
            calculation_type_id=d.get("CalculationTypeId"),
        )


@dataclass(slots=True)
class DurationTypeResponse:
    """A duration type option for services (e.g. fixed, variable).

    Attributes:
        id: Duration type ID.
        name: Human-readable name of the duration type.
    """

    id: int | None = None
    name: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> DurationTypeResponse:
        return cls(id=d.get("Id"), name=d.get("Name"))


@dataclass(slots=True)
class ServiceResponse:
    """Full representation of a bookable service.

    Attributes:
        id: Service ID.
        name: Display name of the service.
        description: Longer description shown to customers.
        group: Optional grouping label for organising services.
        active: Whether the service is currently available for booking.
        booking_status_id: Default booking status applied to new bookings.
        duration: Default duration in minutes.
        duration_type_id: ID of the duration type (fixed / variable / etc.).
        total_spots: Maximum concurrent bookings for this service.
        image_url: URL of the service's cover image.
        is_payment_enabled: Whether online payment is enabled for this service.
        enable_booking_queue: Whether customers can join a waitlist.
        resource_types: Resource type configurations linked to this service.
        prices: Price rules configured for this service.
        schedules: Schedules that define when this service is available.
        custom_fields: Custom field definitions attached to this service.
        rating_score: Aggregated customer rating information.
    """

    id: int | None = None
    name: str | None = None
    description: str | None = None
    group: str | None = None
    active: bool = True
    booking_status_id: int | None = None
    duration: int | None = None
    duration_type_id: int | None = None
    total_spots: int | None = None
    image_url: str | None = None
    is_payment_enabled: bool = False
    enable_booking_queue: bool = False
    resource_types: list[dict] = field(default_factory=list)
    prices: list[ServicePriceResponse] = field(default_factory=list)
    schedules: list[dict] = field(default_factory=list)
    custom_fields: list[CustomFieldValue] = field(default_factory=list)
    rating_score: dict | None = None

    @classmethod
    def from_dict(cls, d: dict) -> ServiceResponse:
        return cls(
            id=d.get("Id"),
            name=d.get("Name"),
            description=d.get("Description"),
            group=d.get("Group"),
            active=d.get("Active", True),
            booking_status_id=d.get("BookingStatusId"),
            duration=d.get("Duration"),
            duration_type_id=d.get("DurationTypeId"),
            total_spots=d.get("TotalSpots"),
            image_url=d.get("ImageUrl"),
            is_payment_enabled=d.get("IsPaymentEnabled", False),
            enable_booking_queue=d.get("EnableBookingQueue", False),
            resource_types=d.get("ResourceTypes", []),
            prices=[ServicePriceResponse.from_dict(p) for p in d.get("Prices", [])],
            schedules=d.get("Schedules", []),
            custom_fields=[CustomFieldValue.from_dict(c) for c in d.get("CustomFields", [])],
            rating_score=d.get("RatingScore"),
        )


@dataclass(slots=True)
class AvailableTime:
    """A single available time slot for a service.

    Attributes:
        from_: Start datetime of this slot.
        to: End datetime of this slot.
        free: Raw free capacity value returned by the API.
        free_spots: Number of bookable spots remaining in this slot.
        resource_id: UUID of the resource assigned to this slot, if applicable.
        exception_texts: Human-readable reason texts for any exceptions that
            affect this slot (e.g. partial availability).
    """

    from_: datetime | None = None
    to: datetime | None = None
    free: int | None = None
    free_spots: int | None = None
    resource_id: UUID | None = None
    exception_texts: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> AvailableTime:
        return cls(
            from_=_dt(d.get("From")),
            to=_dt(d.get("To")),
            free=d.get("Free"),
            free_spots=d.get("FreeSpots"),
            resource_id=_uuid(d.get("ResourceId")),
            exception_texts=d.get("ExceptionTexts", []),
        )


@dataclass(slots=True)
class AvailableTimesResponse:
    """Collection of available time slots for a service within a date range.

    Attributes:
        times: Ordered list of available time slots.
    """

    times: list[AvailableTime] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> AvailableTimesResponse:
        return cls(times=[AvailableTime.from_dict(t) for t in d.get("Times", [])])


@dataclass(slots=True)
class TotalPriceInformationResponse:
    """Price calculation result including any applied rebate codes.

    Attributes:
        price: Final price after all discounts.
        vat: Total VAT amount included in *price*.
        price_before_rebate: Original price before any rebate was applied.
        applied_codes: Details of each rebate code that was applied.
    """

    price: float | None = None
    vat: float | None = None
    price_before_rebate: float | None = None
    applied_codes: list[dict] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> TotalPriceInformationResponse:
        return cls(
            price=d.get("Price"),
            vat=d.get("VAT"),
            price_before_rebate=d.get("PriceBeforeRebate"),
            applied_codes=d.get("AppliedCodes", []),
        )
