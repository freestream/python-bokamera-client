"""
Data models for the articles resource.

Contains dataclasses for article definitions, article type classifications,
and payment log entries associated with article purchases.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from .common import _dt, _uuid


@dataclass(slots=True)
class ArticleTypeResponse:
    """An article type classification (e.g. Gift card, Membership).

    Attributes:
        id: Article type ID.
        name: Display name of the article type.
        description: Optional longer description.
    """

    id: int | None = None
    name: str | None = None
    description: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> ArticleTypeResponse:
        """Construct a ArticleTypeResponse from a raw API response dict."""
        return cls(id=d.get("Id"), name=d.get("Name"), description=d.get("Description"))


@dataclass(slots=True)
class ArticleResponse:
    """An article that can be sold to customers (e.g. a gift card or membership).

    Attributes:
        id: Article ID.
        name: Display name of the article.
        description: Longer description shown to customers.
        article_type_id: ID of the article's type classification.
        price: Selling price of the article.
        currency_id: ISO 4217 currency code.
        duration: Validity duration in days (for time-limited articles).
        active: Whether this article is currently available for purchase.
        service_ids: IDs of services this article can be applied to.
    """

    id: int | None = None
    name: str | None = None
    description: str | None = None
    article_type_id: int | None = None
    price: float | None = None
    currency_id: str | None = None
    duration: int | None = None
    active: bool = True
    service_ids: list[int] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> ArticleResponse:
        """Construct a ArticleResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            name=d.get("Name"),
            description=d.get("Description"),
            article_type_id=d.get("ArticleTypeId"),
            price=d.get("Price"),
            currency_id=d.get("CurrencyId"),
            duration=d.get("Duration"),
            active=d.get("Active", True),
            service_ids=d.get("ServiceIds", []),
        )


@dataclass(slots=True)
class PaymentLogResponse:
    """A payment transaction entry for an article purchase.

    Attributes:
        id: Payment log ID.
        company_id: UUID of the company that received the payment.
        article_type_id: Type ID of the purchased article.
        article_id: ID of the specific article purchased.
        amount: Payment amount.
        currency: ISO 4217 currency code.
        created: Timestamp when the payment was recorded.
        customer_id: UUID of the customer who made the purchase.
    """

    id: int | None = None
    company_id: UUID | None = None
    article_type_id: int | None = None
    article_id: int | None = None
    amount: float | None = None
    currency: str | None = None
    created: datetime | None = None
    customer_id: UUID | None = None

    @classmethod
    def from_dict(cls, d: dict) -> PaymentLogResponse:
        """Construct a PaymentLogResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            company_id=_uuid(d.get("CompanyId")),
            article_type_id=d.get("ArticleTypeId"),
            article_id=d.get("ArticleId"),
            amount=d.get("Amount"),
            currency=d.get("Currency"),
            created=_dt(d.get("Created")),
            customer_id=_uuid(d.get("CustomerId")),
        )
