"""
Data models for the billing resource.

Contains dataclasses for billing methods, company billing information,
invoices, payment settings, and Stripe webhook/checkout integration.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from .common import InvoiceAddress, _dt, _uuid


@dataclass(slots=True)
class BillingMethodResponse:
    """A billing method option available for a company's subscription.

    Attributes:
        id: Billing method ID.
        name: Display name (e.g. "Invoice", "Credit card").
        description: Optional longer description of the billing method.
    """

    id: int | None = None
    name: str | None = None
    description: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> BillingMethodResponse:
        """Construct a BillingMethodResponse from a raw API response dict."""
        return cls(id=d.get("Id"), name=d.get("Name"), description=d.get("Description"))


@dataclass(slots=True)
class BillingInformationResponse:
    """Billing details for a company's BokaMera subscription.

    Attributes:
        id: Billing information record ID.
        company_id: UUID of the associated company.
        name: Name printed on invoices.
        email: Email address for invoice delivery.
        vat_registration_number: VAT / organisation number.
        street: Billing street address.
        city: Billing city.
        zip_code: Billing postal code.
        country_id: ISO 3166-1 alpha-2 country code.
        license_plan_id: ID of the active license plan.
        billing_method_id: ID of the selected billing method.
    """

    id: int | None = None
    company_id: UUID | None = None
    name: str | None = None
    email: str | None = None
    vat_registration_number: str | None = None
    street: str | None = None
    city: str | None = None
    zip_code: str | None = None
    country_id: str | None = None
    license_plan_id: int | None = None
    billing_method_id: int | None = None

    @classmethod
    def from_dict(cls, d: dict) -> BillingInformationResponse:
        """Construct a BillingInformationResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            company_id=_uuid(d.get("CompanyId")),
            name=d.get("Name"),
            email=d.get("Email"),
            vat_registration_number=d.get("VatRegistrationNumber"),
            street=d.get("Street"),
            city=d.get("City"),
            zip_code=d.get("ZipCode"),
            country_id=d.get("CountryId"),
            license_plan_id=d.get("LicensePlanId"),
            billing_method_id=d.get("BillingMethodId"),
        )


@dataclass(slots=True)
class InvoiceLineResponse:
    """A single line item on a company invoice.

    Attributes:
        id: Invoice line ID.
        description: Description of the invoiced item.
        quantity: Number of units.
        unit_price: Price per unit, excluding VAT.
        vat: VAT percentage applied to this line.
        amount: Total line amount (quantity × unit_price + VAT).
    """

    id: int | None = None
    description: str | None = None
    quantity: float | None = None
    unit_price: float | None = None
    vat: float | None = None
    amount: float | None = None

    @classmethod
    def from_dict(cls, d: dict) -> InvoiceLineResponse:
        """Construct a InvoiceLineResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            description=d.get("Description"),
            quantity=d.get("Quantity"),
            unit_price=d.get("UnitPrice"),
            vat=d.get("VAT"),
            amount=d.get("Amount"),
        )


@dataclass(slots=True)
class CompanyInvoiceResponse:
    """A BokaMera subscription invoice for a company.

    Attributes:
        id: Invoice ID.
        company_id: UUID of the invoiced company.
        status_id: Numeric payment status code.
        status: Human-readable payment status name.
        total: Total invoice amount including VAT.
        currency: ISO 4217 currency code of the invoice.
        created: Date the invoice was issued.
        due_date: Payment due date.
        invoice_lines: Individual line items on this invoice.
    """

    id: int | None = None
    company_id: UUID | None = None
    status_id: int | None = None
    status: str | None = None
    total: float | None = None
    currency: str | None = None
    created: datetime | None = None
    due_date: datetime | None = None
    invoice_lines: list[InvoiceLineResponse] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> CompanyInvoiceResponse:
        """Construct a CompanyInvoiceResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            company_id=_uuid(d.get("CompanyId")),
            status_id=d.get("StatusId"),
            status=d.get("Status"),
            total=d.get("Total"),
            currency=d.get("Currency"),
            created=_dt(d.get("Created")),
            due_date=_dt(d.get("DueDate")),
            invoice_lines=[InvoiceLineResponse.from_dict(l) for l in d.get("InvoiceLines", [])],
        )


@dataclass(slots=True)
class PaymentSettingsResponse:
    """Online payment configuration for a company.

    Attributes:
        id: Settings record ID.
        company_id: UUID of the company.
        enabled: Whether online payment is enabled.
        refund_on_cancel_booking: Whether payments are automatically refunded
            when a booking is cancelled.
        default_admin_payment_options_id: Default payment option ID used when
            administrators create bookings.
        payment_provider_id: ID of the configured payment provider.
    """

    id: int | None = None
    company_id: UUID | None = None
    enabled: bool = False
    refund_on_cancel_booking: bool = False
    default_admin_payment_options_id: int | None = None
    payment_provider_id: int | None = None

    @classmethod
    def from_dict(cls, d: dict) -> PaymentSettingsResponse:
        """Construct a PaymentSettingsResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            company_id=_uuid(d.get("CompanyId")),
            enabled=d.get("Enabled", False),
            refund_on_cancel_booking=d.get("RefundOnCancelBooking", False),
            default_admin_payment_options_id=d.get("DefaultAdminPaymentOptionsId"),
            payment_provider_id=d.get("PaymentProviderId"),
        )


@dataclass(slots=True)
class StripeWebhookResponse:
    """A Stripe webhook endpoint configuration.

    Attributes:
        id: Stripe webhook endpoint ID.
        url: Destination URL that receives webhook events.
        events: List of Stripe event type names the webhook subscribes to.
    """

    id: str | None = None
    url: str | None = None
    events: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> StripeWebhookResponse:
        """Construct a StripeWebhookResponse from a raw API response dict."""
        return cls(id=d.get("Id"), url=d.get("Url"), events=d.get("Events", []))


@dataclass(slots=True)
class StripeCheckoutStatusResponse:
    """Status of a Stripe Checkout session.

    Attributes:
        customer_email: Email address of the customer who initiated checkout.
        status: Current session status (e.g. ``"complete"``, ``"expired"``).
    """

    customer_email: str | None = None
    status: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> StripeCheckoutStatusResponse:
        """Construct a StripeCheckoutStatusResponse from a raw API response dict."""
        return cls(customer_email=d.get("CustomerEmail"), status=d.get("Status"))
