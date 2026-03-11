"""
Data models for the companies resource.

Contains dataclasses for company profiles, types, geographic coordinates,
owners, and administrator (company user) accounts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from .common import InvoiceAddress, _dt, _uuid


@dataclass(slots=True)
class CompanyTypeResponse:
    """A company type classification (e.g. Hair salon, Gym).

    Attributes:
        id: Company type ID.
        name: Display name of the type.
        description: Optional longer description.
    """

    id: int | None = None
    name: str | None = None
    description: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> CompanyTypeResponse:
        """Construct a CompanyTypeResponse from a raw API response dict."""
        return cls(id=d.get("Id"), name=d.get("Name"), description=d.get("Description"))


@dataclass(slots=True)
class CompanyCoordinatesResponse:
    """Geographic coordinates resolved for a company's address.

    Attributes:
        longitude: WGS-84 longitude.
        latitude: WGS-84 latitude.
    """

    longitude: float | None = None
    latitude: float | None = None

    @classmethod
    def from_dict(cls, d: dict) -> CompanyCoordinatesResponse:
        """Construct a CompanyCoordinatesResponse from a raw API response dict."""
        return cls(longitude=d.get("Longitude"), latitude=d.get("Latitude"))


@dataclass(slots=True)
class RatingReview:
    """Aggregated customer rating summary for a company or service.

    Attributes:
        score: Average rating score (e.g. on a 1–5 scale).
        count: Total number of ratings contributing to the score.
    """

    score: float | None = None
    count: int | None = None

    @classmethod
    def from_dict(cls, d: dict) -> RatingReview:
        """Construct a RatingReview from a raw API response dict."""
        return cls(score=d.get("Score"), count=d.get("Count"))


@dataclass(slots=True)
class CompanyResponse:
    """Full representation of a BokaMera company.

    Attributes:
        id: UUID of the company.
        name: Legal or trading name of the company.
        organisation_number: Swedish organisation number or VAT ID.
        type_id: ID of the company type classification.
        street1: Primary street address.
        zip_code: Postal code.
        city: City name.
        country_id: ISO 3166-1 alpha-2 country code.
        phone: Contact phone number.
        email: Contact email address.
        site_path: URL-friendly identifier used in the company's booking page URL.
        longitude: WGS-84 longitude of the company's location.
        latitude: WGS-84 latitude of the company's location.
        logo_type: URL or identifier of the company's logo.
        active: Whether the company is currently active on the platform.
        rating_score: Aggregated customer rating for the company.
        booking_settings: Company-level booking configuration dict.
        homepage_settings: Homepage configuration dict.
        widget_settings: Booking widget configuration dict.
        custom_fields: Custom field definitions configured for this company.
    """

    id: UUID | None = None
    name: str | None = None
    organisation_number: str | None = None
    type_id: int | None = None
    street1: str | None = None
    zip_code: str | None = None
    city: str | None = None
    country_id: str | None = None
    phone: str | None = None
    email: str | None = None
    site_path: str | None = None
    longitude: float | None = None
    latitude: float | None = None
    logo_type: str | None = None
    active: bool | None = None
    rating_score: RatingReview | None = None
    booking_settings: dict | None = None
    homepage_settings: dict | None = None
    widget_settings: dict | None = None
    custom_fields: list[dict] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> CompanyResponse:
        """Construct a CompanyResponse from a raw API response dict."""
        return cls(
            id=_uuid(d.get("Id")),
            name=d.get("Name"),
            organisation_number=d.get("OrganisationNumber"),
            type_id=d.get("TypeId"),
            street1=d.get("Street1"),
            zip_code=d.get("ZipCode"),
            city=d.get("City"),
            country_id=d.get("CountryId"),
            phone=d.get("Phone"),
            email=d.get("Email"),
            site_path=d.get("SitePath"),
            longitude=d.get("Longitude"),
            latitude=d.get("Latitude"),
            logo_type=d.get("LogoType"),
            active=d.get("Active"),
            rating_score=RatingReview.from_dict(d["RatingScore"]) if d.get("RatingScore") else None,
            booking_settings=d.get("BookingSettings"),
            homepage_settings=d.get("HomepageSettings"),
            widget_settings=d.get("WidgetSettings"),
            custom_fields=d.get("CustomFields", []),
        )


@dataclass(slots=True)
class CompanyOwnerResponse:
    """A company owner entry.

    Attributes:
        id: Numeric ID of the owner account.
        name: Display name of the owner.
    """

    id: int | None = None
    name: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> CompanyOwnerResponse:
        """Construct a CompanyOwnerResponse from a raw API response dict."""
        return cls(id=d.get("Id"), name=d.get("Name"))


@dataclass(slots=True)
class CompanyUserResponse:
    """An administrator (company user) account within a company.

    Attributes:
        id: UUID of the administrator account.
        firstname: Administrator's first name.
        lastname: Administrator's last name.
        email: Administrator's email address.
        phone: Administrator's phone number.
        resource_id: ID of the resource record linked to this administrator.
        roles: List of role names assigned to this administrator.
        active: Whether this administrator account is currently active.
        worker_id: Optional external worker identifier.
        send_push_notification: Whether push notifications are enabled for this user.
    """

    id: UUID | None = None
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    phone: str | None = None
    resource_id: int | None = None
    roles: list[str] = field(default_factory=list)
    active: bool = True
    worker_id: str | None = None
    send_push_notification: bool = False

    @classmethod
    def from_dict(cls, d: dict) -> CompanyUserResponse:
        """Construct a CompanyUserResponse from a raw API response dict."""
        return cls(
            id=_uuid(d.get("Id")),
            firstname=d.get("Firstname"),
            lastname=d.get("Lastname"),
            email=d.get("Email"),
            phone=d.get("Phone"),
            resource_id=d.get("ResourceId"),
            roles=d.get("Roles", []),
            active=d.get("Active", True),
            worker_id=d.get("WorkerId"),
            send_push_notification=d.get("SendPushNotification", False),
        )
