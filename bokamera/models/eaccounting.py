"""
Data models for the Visma eEkonomi (eAccounting) integration resource.

Contains dataclasses for OAuth tokens, article mappings, invoices, settings,
and invoice notes used in the eEkonomi integration.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from .common import _dt, _uuid


@dataclass(slots=True)
class EAccountingTokenResponse:
    """OAuth token for the Visma eEkonomi API connection.

    Attributes:
        access_token: Short-lived access token used to authenticate API calls.
        refresh_token: Long-lived token used to obtain a new access token.
        token_type: Token scheme (typically ``"Bearer"``).
        expires_at: Timestamp when the access token expires.
    """

    access_token: str | None = None
    refresh_token: str | None = None
    token_type: str | None = None
    expires_at: datetime | None = None

    @classmethod
    def from_dict(cls, d: dict) -> EAccountingTokenResponse:
        """Construct a EAccountingTokenResponse from a raw API response dict."""
        return cls(
            access_token=d.get("AccessToken"),
            refresh_token=d.get("RefreshToken"),
            token_type=d.get("TokenType"),
            expires_at=_dt(d.get("ExpiresAt")),
        )


@dataclass(slots=True)
class EAccountingArticleResponse:
    """An article mapped from a BokaMera service to a Visma eEkonomi article.

    Attributes:
        unit_id: Visma unit identifier for this article.
        coding_id: Visma account coding identifier.
        vat_rate: Visma VAT rate code.
        vat_rate_percent: Numeric VAT percentage.
        article_price: Price of the article in the eEkonomi system.
        article_name: Display name in the eEkonomi system.
    """

    unit_id: str | None = None
    coding_id: str | None = None
    vat_rate: str | None = None
    vat_rate_percent: float | None = None
    article_price: float | None = None
    article_name: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> EAccountingArticleResponse:
        """Construct a EAccountingArticleResponse from a raw API response dict."""
        return cls(
            unit_id=d.get("UnitId"),
            coding_id=d.get("CodingId"),
            vat_rate=d.get("VatRate"),
            vat_rate_percent=d.get("VatRatePercent"),
            article_price=d.get("ArticlePrice"),
            article_name=d.get("ArticleName"),
        )


@dataclass(slots=True)
class EAccountingInvoiceResponse:
    """An invoice created in Visma eEkonomi from a BokaMera booking.

    Attributes:
        id: Visma eEkonomi invoice ID (string UUID).
        booking_id: ID of the BokaMera booking this invoice was created from.
        invoice_uri: URI to the invoice resource in the Visma eEkonomi API.
        customer_name: Customer name printed on the invoice.
        total_amount: Total invoice amount.
        paid: Whether the invoice has been marked as paid.
        lines: Line items on the invoice.
        notes: Notes attached to the invoice.
    """

    id: str | None = None
    booking_id: int | None = None
    invoice_uri: str | None = None
    customer_name: str | None = None
    total_amount: float | None = None
    paid: bool = False
    lines: list[dict] = field(default_factory=list)
    notes: list[dict] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> EAccountingInvoiceResponse:
        """Construct a EAccountingInvoiceResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            booking_id=d.get("BookingId"),
            invoice_uri=d.get("InvoiceUri"),
            customer_name=d.get("CustomerName"),
            total_amount=d.get("TotalAmount"),
            paid=d.get("Paid", False),
            lines=d.get("Lines", []),
            notes=d.get("Notes", []),
        )


@dataclass(slots=True)
class EAccountingSettingsResponse:
    """Integration settings for the Visma eEkonomi connection.

    Attributes:
        active: Whether the eEkonomi integration is currently enabled.
        default_create_type: Default creation mode (e.g. ``"Invoice"``, ``"Draft"``).
        default_terms_of_payment_id: Default payment terms applied to new invoices.
    """

    active: bool = False
    default_create_type: str | None = None
    default_terms_of_payment_id: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> EAccountingSettingsResponse:
        """Construct a EAccountingSettingsResponse from a raw API response dict."""
        return cls(
            active=d.get("Active", False),
            default_create_type=d.get("DefaultCreateType"),
            default_terms_of_payment_id=d.get("DefaultTermsOfPaymentId"),
        )


@dataclass(slots=True)
class EAccountingNoteResponse:
    """A note attached to an invoice in Visma eEkonomi.

    Attributes:
        id: Note ID in the eEkonomi system.
        text: Note body text.
        created_utc: UTC timestamp when the note was created.
        modified_utc: UTC timestamp of the most recent modification.
    """

    id: str | None = None
    text: str | None = None
    created_utc: datetime | None = None
    modified_utc: datetime | None = None

    @classmethod
    def from_dict(cls, d: dict) -> EAccountingNoteResponse:
        """Construct a EAccountingNoteResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            text=d.get("Text"),
            created_utc=_dt(d.get("CreatedUtc")),
            modified_utc=_dt(d.get("ModifiedUtc")),
        )
