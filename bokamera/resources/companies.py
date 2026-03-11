"""
Resource namespace for company operations.

Exposes methods for listing, creating, and searching companies, as well as
querying company types, geo-coordinates, company owners, and company
administrator (user) accounts.
"""

from __future__ import annotations

from uuid import UUID

from .._client import BokaMeraHTTPClient
from ..models.common import QueryResponse
from ..models.companies import (
    CompanyCoordinatesResponse,
    CompanyOwnerResponse,
    CompanyResponse,
    CompanyTypeResponse,
    CompanyUserResponse,
)


class CompanyResource:
    """Company operations: listing, creation, types, coordinates, owners, and admins."""

    def __init__(self, http: BokaMeraHTTPClient) -> None:
        self._http = http

    def list(
        self,
        *,
        id_: UUID | str | None = None,
        categories: list[int] | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
        site_path: str | None = None,
        search: str | None = None,
        distance: float | None = None,
        include_booking_settings: bool | None = None,
        include_rating_reviews: bool | None = None,
        include_widget_settings: bool | None = None,
        include_homepage_settings: bool | None = None,
        skip: int | None = None,
        take: int | None = None,
    ) -> list[CompanyResponse]:
        """Search and list companies.

        Args:
            id_: Filter to a single company by UUID.
            categories: Filter to companies belonging to these category IDs.
            latitude: Latitude for geo-proximity search.
            longitude: Longitude for geo-proximity search.
            site_path: Filter by the company's URL site path.
            search: Free-text search over company name.
            distance: Maximum distance in km for geo-proximity search.
            include_booking_settings: Include booking settings in each result.
            include_rating_reviews: Include rating review summary in each result.
            include_widget_settings: Include booking widget settings in each result.
            include_homepage_settings: Include homepage settings in each result.
            skip: Pagination offset.
            take: Maximum results to return.

        Returns:
            A list of :class:`~bokamera.models.companies.CompanyResponse` objects.
        """
        params = {
            "Id": str(id_) if id_ else None,
            "Categories": categories,
            "Latitude": latitude,
            "Longitude": longitude,
            "SitePath": site_path,
            "Search": search,
            "Distance": distance,
            "IncludeBookingSettings": include_booking_settings,
            "IncludeRatingReviews": include_rating_reviews,
            "IncludeWidgetSettings": include_widget_settings,
            "IncludeHomepageSettings": include_homepage_settings,
            "Skip": skip,
            "Take": take,
        }
        data = self._http.get("/companies", params)
        if isinstance(data, list):
            return [CompanyResponse.from_dict(d) for d in data]
        return [CompanyResponse.from_dict(d) for d in data.get("Results", [])]

    def create(
        self,
        *,
        name: str,
        organisation_number: str | None = None,
        type_id: int | None = None,
        company_owner_id: UUID | str | None = None,
        street1: str | None = None,
        zip_code: str | None = None,
        city: str | None = None,
        country_id: str | None = None,
        phone: str | None = None,
        email: str | None = None,
        site_path: str | None = None,
        company_user: dict | None = None,
        billing_information: dict | None = None,
        license_type_id: int | None = None,
    ) -> CompanyResponse:
        """Create a new company.

        Args:
            name: Display name of the company.
            organisation_number: Organisation registration number.
            type_id: ID of the company type.
            company_owner_id: UUID of the company owner account.
            street1: Street address line 1.
            zip_code: Postal code.
            city: City name.
            country_id: ISO country code (e.g. ``"SE"``).
            phone: Company phone number.
            email: Company email address.
            site_path: URL-friendly site path for the company.
            company_user: Initial administrator user dict.
            billing_information: Billing details dict.
            license_type_id: ID of the license type to assign.

        Returns:
            The newly created :class:`~bokamera.models.companies.CompanyResponse`.
        """
        body = {
            "Name": name,
            "OrganisationNumber": organisation_number,
            "TypeId": type_id,
            "CompanyOwnerId": str(company_owner_id) if company_owner_id else None,
            "Street1": street1,
            "ZipCode": zip_code,
            "City": city,
            "CountryId": country_id,
            "Phone": phone,
            "Email": email,
            "SitePath": site_path,
            "CompanyUser": company_user,
            "BillingInformation": billing_information,
            "LicenseTypeId": license_type_id,
        }
        return CompanyResponse.from_dict(self._http.post("/companies/", body))

    def list_types(self, *, skip: int | None = None, take: int | None = None) -> QueryResponse[CompanyTypeResponse]:
        """List all available company types.

        Args:
            skip: Pagination offset.
            take: Maximum results to return.

        Returns:
            A paginated response of :class:`~bokamera.models.companies.CompanyTypeResponse` objects.
        """
        return QueryResponse.from_dict(
            self._http.get("/companies/types", {"Skip": skip, "Take": take}), CompanyTypeResponse
        )

    def get_coordinates(
        self,
        *,
        street1: str | None = None,
        zip_code: str | None = None,
        city: str | None = None,
        country_id: str | None = None,
    ) -> CompanyCoordinatesResponse:
        """Geocode an address to latitude/longitude coordinates.

        Args:
            street1: Street address line 1.
            zip_code: Postal code.
            city: City name.
            country_id: ISO country code (e.g. ``"SE"``).

        Returns:
            A :class:`~bokamera.models.companies.CompanyCoordinatesResponse` with the resolved coordinates.
        """
        params = {"Street1": street1, "ZipCode": zip_code, "City": city, "CountryId": country_id}
        return CompanyCoordinatesResponse.from_dict(self._http.get("/companies/coordinates", params))

    def list_owners(self, *, skip: int | None = None, take: int | None = None) -> QueryResponse[CompanyOwnerResponse]:
        """List company owner accounts.

        Args:
            skip: Pagination offset.
            take: Maximum results to return.

        Returns:
            A paginated response of :class:`~bokamera.models.companies.CompanyOwnerResponse` objects.
        """
        return QueryResponse.from_dict(
            self._http.get("/companyOwners", {"Skip": skip, "Take": take}), CompanyOwnerResponse
        )

    # ── Administrators ───────────────────────────────────────────────────────

    def list_admins(
        self,
        *,
        company_id: UUID | str | None = None,
        active: bool | None = None,
        include_resource_information: bool | None = None,
        include_roles_information: bool | None = None,
    ) -> list[CompanyUserResponse]:
        """List administrator accounts for a company.

        Args:
            company_id: Target company (defaults to the client's company).
            active: When set, filter by active/inactive status.
            include_resource_information: Include linked resource details.
            include_roles_information: Include role assignments.

        Returns:
            A list of :class:`~bokamera.models.companies.CompanyUserResponse` objects.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Active": active,
            "IncludeResourceInformation": include_resource_information,
            "IncludeRolesInformation": include_roles_information,
        }
        data = self._http.get("/administrators/", params)
        if isinstance(data, list):
            return [CompanyUserResponse.from_dict(d) for d in data]
        return [CompanyUserResponse.from_dict(d) for d in data.get("Results", [])]

    def create_admin(
        self,
        *,
        firstname: str,
        lastname: str,
        email: str,
        phone: str | None = None,
        resource_id: UUID | str | None = None,
        roles: list[str] | None = None,
        worker_id: str | None = None,
        send_push_notification: bool = False,
        company_id: UUID | str | None = None,
    ) -> CompanyUserResponse:
        """Create a new administrator account for a company.

        Args:
            firstname: Administrator's first name.
            lastname: Administrator's last name.
            email: Administrator's email address.
            phone: Administrator's phone number.
            resource_id: UUID of a resource to link to this admin account.
            roles: List of role names to assign (e.g. ``["Administrator"]``).
            worker_id: External worker/employee identifier.
            send_push_notification: Send a push notification to welcome the new admin.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.companies.CompanyUserResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Firstname": firstname,
            "Lastname": lastname,
            "Email": email,
            "Phone": phone,
            "ResourceId": str(resource_id) if resource_id else None,
            "Roles": roles or [],
            "WorkerId": worker_id,
            "SendPushNotification": send_push_notification,
        }
        return CompanyUserResponse.from_dict(self._http.post("/administrators/", body))

    def update_admin(self, admin_id: UUID | str, *, company_id: UUID | str | None = None, **kwargs: object) -> CompanyUserResponse:
        """Update an existing administrator account.

        Args:
            admin_id: UUID of the administrator to update.
            company_id: Target company (defaults to the client's company).
            **kwargs: Administrator fields to update (e.g. ``Firstname``, ``Roles``).

        Returns:
            The updated :class:`~bokamera.models.companies.CompanyUserResponse`.
        """
        body = {"CompanyId": str(company_id) if company_id else self._http.default_company_id, **kwargs}
        return CompanyUserResponse.from_dict(self._http.put(f"/administrators/{admin_id}", body))

    def delete_admin(self, admin_id: UUID | str, *, company_id: UUID | str | None = None) -> CompanyUserResponse:
        """Delete an administrator account from a company.

        Args:
            admin_id: UUID of the administrator to delete.
            company_id: Target company (defaults to the client's company).

        Returns:
            The deleted :class:`~bokamera.models.companies.CompanyUserResponse`.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return CompanyUserResponse.from_dict(self._http.delete(f"/administrators/{admin_id}", params))

    def list_roles(self) -> list[dict]:
        """List all available administrator role definitions.

        Returns:
            A list of role dicts, each describing a role name and its permissions.
        """
        data = self._http.get("/administrators/roles")
        if isinstance(data, list):
            return data
        return data.get("Results", [])
