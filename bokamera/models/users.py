"""
Data models for the users resource.

Contains dataclasses for user profiles, the current authenticated user,
user agreements, and the response returned when creating a new user account.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from .common import InvoiceAddress, _dt, _uuid


@dataclass(slots=True)
class UserProfile:
    """Basic profile information for a BokaMera user.

    Attributes:
        user_id: UUID of the user account.
        firstname: User's first name.
        lastname: User's last name.
        email: User's email address.
        phone: User's phone number.
    """

    user_id: UUID | None = None
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    phone: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> UserProfile:
        """Construct a UserProfile from a raw API response dict."""
        return cls(
            user_id=_uuid(d.get("UserId")),
            firstname=d.get("Firstname"),
            lastname=d.get("Lastname"),
            email=d.get("Email"),
            phone=d.get("Phone"),
        )


@dataclass(slots=True)
class CurrentUserResponse:
    """The authenticated user's full profile returned by ``GET /users``.

    Attributes:
        user_id: UUID of the authenticated user.
        user_profile: Consumer-facing profile information.
        admin_profile: Administrator profile, if the user has admin access.
        invoice_address: Saved billing address for this user.
        favorites: Companies marked as favourites by this user.
    """

    user_id: UUID | None = None
    user_profile: UserProfile | None = None
    admin_profile: UserProfile | None = None
    invoice_address: InvoiceAddress | None = None
    favorites: list[dict] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> CurrentUserResponse:
        """Construct a CurrentUserResponse from a raw API response dict."""
        return cls(
            user_id=_uuid(d.get("UserId")),
            user_profile=UserProfile.from_dict(d["UserProfile"]) if d.get("UserProfile") else None,
            admin_profile=UserProfile.from_dict(d["AdminProfile"]) if d.get("AdminProfile") else None,
            invoice_address=InvoiceAddress.from_dict(d["InvoiceAddress"]) if d.get("InvoiceAddress") else None,
            favorites=d.get("Favorites", []),
        )


@dataclass(slots=True)
class CreateUserResponse:
    """Response returned after successfully creating a new user account.

    Attributes:
        id: Numeric record ID of the newly created user.
        user_id: UUID assigned to the new user account.
        email: Email address registered for the new account.
        created_date: Timestamp when the account was created.
    """

    id: int | None = None
    user_id: UUID | None = None
    email: str | None = None
    created_date: datetime | None = None

    @classmethod
    def from_dict(cls, d: dict) -> CreateUserResponse:
        """Construct a CreateUserResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            user_id=_uuid(d.get("UserId")),
            email=d.get("Email"),
            created_date=_dt(d.get("CreatedDate")),
        )


@dataclass(slots=True)
class UserAgreementResponse:
    """A record of a user accepting (or declining) a specific agreement.

    Attributes:
        id: Record ID.
        user_id: UUID of the user who responded.
        agreement_id: ID of the agreement being accepted or declined.
        accepted: ``True`` if the user accepted, ``False`` if declined.
        accepted_date: Timestamp when the user responded.
    """

    id: int | None = None
    user_id: UUID | None = None
    agreement_id: int | None = None
    accepted: bool | None = None
    accepted_date: datetime | None = None

    @classmethod
    def from_dict(cls, d: dict) -> UserAgreementResponse:
        """Construct a UserAgreementResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            user_id=_uuid(d.get("UserId")),
            agreement_id=d.get("AgreementId"),
            accepted=d.get("Accepted"),
            accepted_date=_dt(d.get("AcceptedDate")),
        )


@dataclass(slots=True)
class AgreementResponse:
    """A legal agreement (e.g. terms of service) managed by the platform.

    Attributes:
        id: Agreement ID.
        name: Short title of the agreement.
        description: Longer description of what the agreement covers.
        url: URL to the full agreement text.
        version: Version identifier for this revision of the agreement.
        created: Timestamp when this version was published.
    """

    id: int | None = None
    name: str | None = None
    description: str | None = None
    url: str | None = None
    version: str | None = None
    created: datetime | None = None

    @classmethod
    def from_dict(cls, d: dict) -> AgreementResponse:
        """Construct a AgreementResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            name=d.get("Name"),
            description=d.get("Description"),
            url=d.get("Url"),
            version=d.get("Version"),
            created=_dt(d.get("Created")),
        )
