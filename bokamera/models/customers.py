"""
Data models for the customers resource.

Contains dataclasses for customer profiles, customer comments, and customer
article associations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from .common import CustomFieldValue, InvoiceAddress, _dt, _uuid


@dataclass(slots=True)
class CustomerCommentResponse:
    """An internal comment attached to a customer profile.

    Attributes:
        id: Comment ID.
        comments: The free-text comment body.
        image_url: Optional URL of an image attached to the comment.
        created: Timestamp when the comment was created.
        updated: Timestamp of the most recent modification.
    """

    id: int | None = None
    comments: str | None = None
    image_url: str | None = None
    created: datetime | None = None
    updated: datetime | None = None

    @classmethod
    def from_dict(cls, d: dict) -> CustomerCommentResponse:
        """Construct a CustomerCommentResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            comments=d.get("Comments"),
            image_url=d.get("ImageUrl"),
            created=_dt(d.get("Created")),
            updated=_dt(d.get("Updated")),
        )


@dataclass(slots=True)
class CustomerResponse:
    """Full representation of a customer profile.

    Attributes:
        id: UUID of the customer record.
        user_id: UUID of the associated user account, if the customer has one.
        firstname: Customer's first name.
        lastname: Customer's last name.
        email: Customer's email address.
        phone: Customer's phone number.
        personal_identity_number: National identity / personal number.
        subscribed_to_newsletter: Whether the customer has opted in to newsletters.
        visible: Whether the customer is visible in admin lists.
        custom_fields: Custom field values stored for this customer.
        invoice_address: Billing / postal address.
        comments: Internal comments attached to this customer.
        access_keys: Code lock access keys assigned to this customer.
        created: Timestamp when the customer record was created.
        updated: Timestamp of the most recent modification.
    """

    id: UUID | None = None
    user_id: UUID | None = None
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    phone: str | None = None
    personal_identity_number: str | None = None
    subscribed_to_newsletter: bool = False
    visible: bool = True
    custom_fields: list[CustomFieldValue] = field(default_factory=list)
    invoice_address: InvoiceAddress | None = None
    comments: list[CustomerCommentResponse] = field(default_factory=list)
    access_keys: list[dict] = field(default_factory=list)
    created: datetime | None = None
    updated: datetime | None = None

    @classmethod
    def from_dict(cls, d: dict) -> CustomerResponse:
        """Construct a CustomerResponse from a raw API response dict."""
        return cls(
            id=_uuid(d.get("Id")),
            user_id=_uuid(d.get("UserId")),
            firstname=d.get("Firstname"),
            lastname=d.get("Lastname"),
            email=d.get("Email"),
            phone=d.get("Phone"),
            personal_identity_number=d.get("PersonalIdentityNumber"),
            subscribed_to_newsletter=d.get("SubscribedToNewsletter", False),
            visible=d.get("Visible", True),
            custom_fields=[CustomFieldValue.from_dict(c) for c in d.get("CustomFields", [])],
            invoice_address=InvoiceAddress.from_dict(d["InvoiceAddress"]) if d.get("InvoiceAddress") else None,
            comments=[CustomerCommentResponse.from_dict(c) for c in d.get("Comments", [])],
            access_keys=d.get("AccessKeys", []),
            created=_dt(d.get("Created")),
            updated=_dt(d.get("Updated")),
        )


@dataclass(slots=True)
class CustomerArticleResponse:
    """An article purchased by or assigned to a customer (e.g. a membership card).

    Attributes:
        id: Customer article ID.
        article_id: ID of the article definition.
        customer_id: UUID of the owning customer.
        status_id: Current status of the customer article.
        created: Timestamp when the article was assigned to the customer.
    """

    id: int | None = None
    article_id: int | None = None
    customer_id: UUID | None = None
    status_id: int | None = None
    created: datetime | None = None

    @classmethod
    def from_dict(cls, d: dict) -> CustomerArticleResponse:
        """Construct a CustomerArticleResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            article_id=d.get("ArticleId"),
            customer_id=_uuid(d.get("CustomerId")),
            status_id=d.get("StatusId"),
            created=_dt(d.get("Created")),
        )
