"""
Shared model types used across multiple BokaMera resources.

Contains generic helpers such as :class:`QueryResponse` for paginated results,
:class:`InvoiceAddress` for billing addresses, :class:`CustomFieldValue` for
dynamic custom fields, and basic lookup types for countries, currencies and
geographic data.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Generic, TypeVar
from uuid import UUID

T = TypeVar("T")


def _uuid(v: str | UUID | None) -> UUID | None:
    """Coerce a string or existing UUID to a ``UUID`` instance.

    Args:
        v: Value to coerce.  May be a UUID string, an existing ``UUID`` object,
            or ``None``.

    Returns:
        A :class:`~uuid.UUID` instance, or ``None`` if *v* is ``None``.
    """
    if v is None:
        return None
    return UUID(str(v)) if not isinstance(v, UUID) else v


def _date(v: str | date | None) -> date | None:
    """Coerce an ISO-8601 string to a ``date`` instance.

    Accepts both plain date strings (``'2026-03-11'``) and datetime strings
    (``'2026-03-11T00:00:00'``) — the time component is discarded.

    Args:
        v: Value to coerce.

    Returns:
        A :class:`~datetime.date` instance, or ``None`` if *v* is ``None``.
    """
    if v is None:
        return None
    if isinstance(v, date) and not isinstance(v, datetime):
        return v
    s = str(v)
    # Strip time component if present so date.fromisoformat() can parse it.
    return date.fromisoformat(s[:10])


def _dt(v: str | datetime | None) -> datetime | None:
    """Coerce an ISO-8601 string to a ``datetime`` instance.

    Args:
        v: Value to coerce.  May be an ISO-8601 formatted string (including the
            ``Z`` UTC suffix), an existing :class:`~datetime.datetime` object,
            or ``None``.

    Returns:
        A timezone-aware :class:`~datetime.datetime` instance, or ``None`` if
        *v* is ``None``.
    """
    if v is None:
        return None
    if isinstance(v, datetime):
        return v
    return datetime.fromisoformat(v.replace("Z", "+00:00"))


@dataclass(slots=True)
class QueryResponse(Generic[T]):
    """Generic paginated response wrapper returned by list endpoints.

    Attributes:
        offset: Number of items skipped before the first result.
        total: Total number of matching items in the API (may exceed
            ``len(results)`` when pagination is used).
        results: The items in this page.
        meta: Optional metadata dict returned alongside the results.
    """

    offset: int
    total: int
    results: list[T]
    meta: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, data: dict, item_factory: type[T]) -> QueryResponse[T]:  # type: ignore[valid-type]
        """Construct a QueryResponse from a raw API response dict, deserialising each result with *item_factory*."""
        items = [item_factory.from_dict(r) for r in data.get("Results", [])]  # type: ignore[attr-defined]
        return cls(
            offset=data.get("Offset", 0),
            total=data.get("Total", len(items)),
            results=items,
            meta=data.get("Meta"),
        )


@dataclass(slots=True)
class InvoiceAddress:
    """Postal/billing address used on invoices.

    Attributes:
        street: Street name and number.
        city: City name.
        zip_code: Postal code.
        country_id: ISO 3166-1 alpha-2 country code (e.g. ``"SE"``).
        name: Recipient name as it should appear on the invoice.
        vat_registration_number: VAT / organisation number of the recipient.
        email: Email address for e-invoice delivery.
    """

    street: str | None = None
    city: str | None = None
    zip_code: str | None = None
    country_id: str | None = None
    name: str | None = None
    vat_registration_number: str | None = None
    email: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> InvoiceAddress:
        """Construct a InvoiceAddress from a raw API response dict."""
        return cls(
            street=d.get("Street"),
            city=d.get("City"),
            zip_code=d.get("ZipCode"),
            country_id=d.get("CountryId"),
            name=d.get("Name"),
            vat_registration_number=d.get("VatRegistrationNumber"),
            email=d.get("Email"),
        )

    def to_dict(self) -> dict:
        return {k: v for k, v in {
            "Street": self.street,
            "City": self.city,
            "ZipCode": self.zip_code,
            "CountryId": self.country_id,
            "Name": self.name,
            "VatRegistrationNumber": self.vat_registration_number,
            "Email": self.email,
        }.items() if v is not None}


@dataclass(slots=True)
class CustomFieldValue:
    """A single custom field value attached to a booking, customer, or resource.

    Attributes:
        id: The ID of the custom field definition.
        column: Internal column name used by the API for storage.
        value: The value entered for this custom field.
    """

    id: int
    column: str | None = None
    value: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> CustomFieldValue:
        """Construct a CustomFieldValue from a raw API response dict."""
        return cls(id=d["Id"], column=d.get("Column"), value=d.get("Value"))

    def to_dict(self) -> dict:
        return {"Id": self.id, "Value": self.value}


@dataclass(slots=True)
class CountryResponse:
    """Country lookup entry returned by the ``/countries`` endpoint.

    Attributes:
        id: ISO 3166-1 alpha-2 country code (e.g. ``"SE"``).
        name: Human-readable country name.
        currency: ISO 4217 currency code used in the country.
    """

    id: str
    name: str | None = None
    currency: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> CountryResponse:
        """Construct a CountryResponse from a raw API response dict."""
        return cls(id=d["Id"], name=d.get("Name"), currency=d.get("Currency"))


@dataclass(slots=True)
class CurrencyResponse:
    """Currency lookup entry returned by the ``/currencies`` endpoint.

    Attributes:
        id: ISO 4217 currency code (e.g. ``"SEK"``).
        name: Human-readable currency name.
        currency_sign: Display symbol (e.g. ``"kr"``).
        active: Whether the currency is currently active in the platform.
    """

    id: str
    name: str | None = None
    currency_sign: str | None = None
    active: bool = True

    @classmethod
    def from_dict(cls, d: dict) -> CurrencyResponse:
        """Construct a CurrencyResponse from a raw API response dict."""
        return cls(
            id=d["Id"],
            name=d.get("Name"),
            currency_sign=d.get("CurrencySign"),
            active=d.get("Active", True),
        )


@dataclass(slots=True)
class GeoCity:
    """Geographic city entry returned by the geodata endpoint.

    Attributes:
        city: City name.
        longitude: WGS-84 longitude of the city centre.
        latitude: WGS-84 latitude of the city centre.
        population: Approximate population of the city.
    """

    city: str | None = None
    longitude: float | None = None
    latitude: float | None = None
    population: int | None = None

    @classmethod
    def from_dict(cls, d: dict) -> GeoCity:
        """Construct a GeoCity from a raw API response dict."""
        return cls(
            city=d.get("City"),
            longitude=d.get("Longitude"),
            latitude=d.get("Latitude"),
            population=d.get("Population"),
        )
