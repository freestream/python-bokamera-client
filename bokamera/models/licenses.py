"""
Data models for the licenses resource.

Contains dataclasses for license plans, license types, active company licenses,
and trial period records.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from .common import _dt, _uuid


@dataclass(slots=True)
class LicensePlanResponse:
    """A billing plan associated with a license type.

    Attributes:
        id: Plan ID.
        name: Display name of the plan.
        voss_plan: Internal VOSS subscription plan identifier.
        plan_length: Duration of the plan (number of units).
        plan_length_unit: Unit of duration (e.g. ``"Month"``, ``"Year"``).
    """

    id: int | None = None
    name: str | None = None
    voss_plan: str | None = None
    plan_length: int | None = None
    plan_length_unit: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> LicensePlanResponse:
        """Construct a LicensePlanResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            name=d.get("Name"),
            voss_plan=d.get("VossPlan"),
            plan_length=d.get("PlanLength"),
            plan_length_unit=d.get("PlanLengthUnit"),
        )


@dataclass(slots=True)
class LicenseTypeResponse:
    """A license product type available for purchase on BokaMera.

    Attributes:
        id: License type ID.
        name: Display name of the license type.
        description: Feature summary or description.
        items: Feature items / entitlements included in this license type.
        prices: Pricing options available for this license type.
    """

    id: int | None = None
    name: str | None = None
    description: str | None = None
    items: list[dict] = field(default_factory=list)
    prices: list[dict] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> LicenseTypeResponse:
        """Construct a LicenseTypeResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            name=d.get("Name"),
            description=d.get("Description"),
            items=d.get("LicenseItems", []),
            prices=d.get("LicensePrices", []),
        )


@dataclass(slots=True)
class CompanyLicenseResponse:
    """An active license held by a company.

    Attributes:
        id: License record ID.
        company_id: UUID of the licensed company.
        type_id: ID of the license type.
        type_name: Display name of the license type.
        valid_from: Timestamp from which the license is valid.
        valid_to: Timestamp until which the license is valid.
        active: Whether this license is currently active.
        meta_data: Optional serialised metadata string attached to the license.
    """

    id: int | None = None
    company_id: UUID | None = None
    type_id: int | None = None
    type_name: str | None = None
    valid_from: datetime | None = None
    valid_to: datetime | None = None
    active: bool = True
    meta_data: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> CompanyLicenseResponse:
        """Construct a CompanyLicenseResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            company_id=_uuid(d.get("CompanyId")),
            type_id=d.get("TypeId"),
            type_name=d.get("TypeName"),
            valid_from=_dt(d.get("ValidFrom")),
            valid_to=_dt(d.get("ValidTo")),
            active=d.get("Active", True),
            meta_data=d.get("MetaData"),
        )


@dataclass(slots=True)
class CompanyTrialResponse:
    """A trial period activated for a company feature.

    Attributes:
        id: Trial record ID.
        company_id: UUID of the company on trial.
        trial_type_id: ID of the trial type.
        trial_type: Display name of the trial type.
        started: Timestamp when the trial was activated.
        valid_to: Timestamp when the trial expires.
        active: Whether the trial is currently active.
    """

    id: int | None = None
    company_id: UUID | None = None
    trial_type_id: int | None = None
    trial_type: str | None = None
    started: datetime | None = None
    valid_to: datetime | None = None
    active: bool = True

    @classmethod
    def from_dict(cls, d: dict) -> CompanyTrialResponse:
        """Construct a CompanyTrialResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            company_id=_uuid(d.get("CompanyId")),
            trial_type_id=d.get("TrialTypeId"),
            trial_type=d.get("TrialType"),
            started=_dt(d.get("Started")),
            valid_to=_dt(d.get("ValidTo")),
            active=d.get("Active", True),
        )
