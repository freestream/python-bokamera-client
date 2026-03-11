"""
Data models for the rebate codes resource.

Contains dataclasses for rebate code definitions, their type and status
lookups, and transaction records tracking code usage.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import UUID

from .common import _date, _dt, _uuid


@dataclass(slots=True)
class RebateCodeTypeResponse:
    """A rebate code type (e.g. percentage discount, fixed amount).

    Attributes:
        id: Type ID.
        name: Display name of the rebate type.
        description: Optional description explaining how the rebate is applied.
    """

    id: int | None = None
    name: str | None = None
    description: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> RebateCodeTypeResponse:
        """Construct a RebateCodeTypeResponse from a raw API response dict."""
        return cls(id=d.get("Id"), name=d.get("Name"), description=d.get("Description"))


@dataclass(slots=True)
class RebateCodeStatusResponse:
    """A rebate code status (e.g. Active, Expired, Depleted).

    Attributes:
        id: Status ID.
        name: Human-readable status name.
    """

    id: int | None = None
    name: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> RebateCodeStatusResponse:
        """Construct a RebateCodeStatusResponse from a raw API response dict."""
        return cls(id=d.get("Id"), name=d.get("Name"))


@dataclass(slots=True)
class RebateCodeResponse:
    """A rebate (discount) code that can be applied at booking time.

    Attributes:
        id: Rebate code ID.
        company_id: UUID of the owning company.
        rebate_code_sign: The code string customers enter (e.g. ``"SUMMER26"``).
        rebate_code_type_id: ID of the rebate type (percentage, fixed amount, etc.).
        rebate_code_value: Discount value (percentage or currency amount, depending on type).
        valid_from: First date from which the code can be used.
        valid_to: Last date until which the code can be used.
        max_number_of_uses: Maximum total times the code can be used (``None`` = unlimited).
        max_number_of_uses_per_customer: Maximum times a single customer can use the code.
        days_of_week: Days on which the code is valid (1 = Monday, 7 = Sunday).
        services: Services this code is restricted to (empty = all services).
        customers: Customers this code is restricted to (empty = all customers).
        currency_id: Currency code for fixed-amount rebates.
        remaining_uses: How many uses remain before the code is depleted.
        active: Whether the code is currently active.
    """

    id: int | None = None
    company_id: UUID | None = None
    rebate_code_sign: str | None = None
    rebate_code_type_id: int | None = None
    rebate_code_value: float | None = None
    valid_from: date | None = None
    valid_to: date | None = None
    max_number_of_uses: int | None = None
    max_number_of_uses_per_customer: int | None = None
    days_of_week: list[int] = field(default_factory=list)
    services: list[dict] = field(default_factory=list)
    customers: list[dict] = field(default_factory=list)
    currency_id: str | None = None
    remaining_uses: int | None = None
    active: bool = True

    @classmethod
    def from_dict(cls, d: dict) -> RebateCodeResponse:
        """Construct a RebateCodeResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            company_id=_uuid(d.get("CompanyId")),
            rebate_code_sign=d.get("RebateCodeSign"),
            rebate_code_type_id=d.get("RebateCodeTypeId"),
            rebate_code_value=d.get("RebateCodeValue"),
            valid_from=_date(d.get("ValidFrom")),
            valid_to=_date(d.get("ValidTo")),
            max_number_of_uses=d.get("MaxNumberOfUses"),
            max_number_of_uses_per_customer=d.get("MaxNumberOfUsesPerCustomer"),
            days_of_week=d.get("DaysOfWeek", []),
            services=d.get("Services", []),
            customers=d.get("Customers", []),
            currency_id=d.get("CurrencyId"),
            remaining_uses=d.get("RemainingUses"),
            active=d.get("Active", True),
        )


@dataclass(slots=True)
class RebateCodeTransactionResponse:
    """A usage transaction recorded when a rebate code is applied to a booking.

    Attributes:
        id: Transaction ID.
        rebate_code_id: ID of the rebate code that was used.
        amount: Discount amount credited in this transaction.
        usage: Usage units consumed (often 1 per booking).
        booking_id: ID of the booking the code was applied to.
        created: Timestamp when the transaction was recorded.
    """

    id: int | None = None
    rebate_code_id: int | None = None
    amount: float | None = None
    usage: float | None = None
    booking_id: int | None = None
    created: datetime | None = None

    @classmethod
    def from_dict(cls, d: dict) -> RebateCodeTransactionResponse:
        """Construct a RebateCodeTransactionResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            rebate_code_id=d.get("RebateCodeId"),
            amount=d.get("Amount"),
            usage=d.get("Usage"),
            booking_id=d.get("BookingId"),
            created=_dt(d.get("Created")),
        )
