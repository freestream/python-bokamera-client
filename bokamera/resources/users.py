"""
Resource namespace for user account operations.

Exposes methods for retrieving and managing the authenticated user's profile,
creating new user accounts, handling password resets, email confirmation,
favorites, and user agreement acceptance.
"""

from __future__ import annotations

from uuid import UUID

from .._client import BokaMeraHTTPClient
from ..models.common import InvoiceAddress, QueryResponse
from ..models.users import AgreementResponse, CreateUserResponse, CurrentUserResponse, UserAgreementResponse


class UserResource:
    """User account operations: profile, creation, agreements, and favorites."""

    def __init__(self, http: BokaMeraHTTPClient) -> None:
        self._http = http

    def get_current(
        self,
        *,
        include_favorites: bool | None = None,
        include_company_customers: bool | None = None,
        include_invoice_address: bool | None = None,
    ) -> CurrentUserResponse:
        """Retrieve the authenticated user's profile.

        Args:
            include_favorites: Include the user's favourite company list.
            include_company_customers: Include customer records linked to the user.
            include_invoice_address: Include the user's invoice address.

        Returns:
            A :class:`~bokamera.models.users.CurrentUserResponse` for the authenticated user.
        """
        params = {
            "IncludeFavorites": include_favorites,
            "IncludeCompanyCustomers": include_company_customers,
            "IncludeInvoiceAddress": include_invoice_address,
        }
        return CurrentUserResponse.from_dict(self._http.get("/users", params))

    def create(
        self,
        *,
        firstname: str,
        lastname: str,
        email: str,
        phone: str | None = None,
        invoice_address: InvoiceAddress | None = None,
    ) -> CreateUserResponse:
        """Create a new user account.

        Args:
            firstname: User's first name.
            lastname: User's last name.
            email: User's email address (used as username).
            phone: User's phone number.
            invoice_address: Optional billing address for the new user.

        Returns:
            A :class:`~bokamera.models.users.CreateUserResponse` for the newly created account.
        """
        body = {
            "Firstname": firstname,
            "Lastname": lastname,
            "Email": email,
            "Phone": phone,
            "InvoiceAddress": invoice_address.to_dict() if invoice_address else None,
        }
        return CreateUserResponse.from_dict(self._http.post("/users", body))

    def delete(
        self,
        *,
        username: str,
        realm: str,
        delete_customer_profiles: bool = False,
        force_delete: bool = False,
        token: str | None = None,
    ) -> dict:
        """Delete a user account.

        Args:
            username: Username (email address) of the account to delete.
            realm: Authentication realm the account belongs to.
            delete_customer_profiles: Also delete any linked customer profiles.
            force_delete: Delete even if the user has active bookings.
            token: Optional deletion confirmation token.

        Returns:
            Raw API response dict for the deletion.
        """
        params = {
            "UserName": username,
            "Realm": realm,
            "DeleteCustomerProfiles": delete_customer_profiles,
            "ForceDelete": force_delete,
            "Token": token,
        }
        return self._http.delete("/users", params)

    def get_agreement(self, *, user_id: UUID | str | None = None) -> UserAgreementResponse:
        """Retrieve the current agreement status for a user.

        Args:
            user_id: UUID of the user to check. Defaults to the authenticated user.

        Returns:
            A :class:`~bokamera.models.users.UserAgreementResponse` describing the agreement state.
        """
        params = {"UserId": str(user_id) if user_id else None}
        return UserAgreementResponse.from_dict(self._http.get("/users/agreement", params))

    def accept_agreement(self, *, user_id: UUID | str, agreement_id: int) -> UserAgreementResponse:
        """Record a user's acceptance of a terms-of-service agreement.

        Args:
            user_id: UUID of the user accepting the agreement.
            agreement_id: ID of the agreement being accepted.

        Returns:
            The updated :class:`~bokamera.models.users.UserAgreementResponse`.
        """
        body = {"UserId": str(user_id), "AgreementId": agreement_id}
        return UserAgreementResponse.from_dict(self._http.post("/users/agreement", body))

    def forgot_password(self, *, email: str, realm: str) -> dict:
        """Trigger a password-reset email for a user account.

        Args:
            email: Email address of the account to reset.
            realm: Authentication realm the account belongs to.

        Returns:
            Raw API response dict confirming the reset email was sent.
        """
        return self._http.post("/users/forgotpassword", {"Email": email, "Realm": realm})

    def confirm_email(self, *, token: str, realm: str) -> dict:
        """Confirm a user's email address using a confirmation token.

        Args:
            token: Email confirmation token received by the user.
            realm: Authentication realm the account belongs to.

        Returns:
            Raw API response dict confirming the email address.
        """
        return self._http.post("/users/confirmemail", {"Token": token, "Realm": realm})

    def add_favorite(self, company_id: UUID | str) -> dict:
        """Add a company to the authenticated user's favourites.

        Args:
            company_id: UUID of the company to add as a favourite.

        Returns:
            Raw API response dict for the operation.
        """
        return self._http.post("/users/favorite", {"CompanyId": str(company_id)})

    def remove_favorite(self, company_id: UUID | str) -> dict:
        """Remove a company from the authenticated user's favourites.

        Args:
            company_id: UUID of the company to remove.

        Returns:
            Raw API response dict for the operation.
        """
        return self._http.delete("/users/favorite", {"CompanyId": str(company_id)})

    def list_agreements(self) -> list[AgreementResponse]:
        """List all available user agreements.

        Returns:
            A list of :class:`~bokamera.models.users.AgreementResponse` objects.
        """
        data = self._http.get("/agreements")
        if isinstance(data, list):
            return [AgreementResponse.from_dict(d) for d in data]
        return [AgreementResponse.from_dict(d) for d in data.get("Results", [])]
