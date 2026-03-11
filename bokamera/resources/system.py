"""
Resource namespace for system-level and miscellaneous operations.

Exposes methods for API version checking, access key types, error reporting,
booking settings, company categories, customer ratings, external references,
lookup data (countries, currencies, cities), Google Meet integration, and
Mailchimp integration.
"""

from __future__ import annotations

from uuid import UUID

from .._client import BokaMeraHTTPClient
from ..models.common import CountryResponse, CurrencyResponse, GeoCity, QueryResponse


class SystemResource:
    """System-level operations: versioning, lookup data, integrations, and references."""

    def __init__(self, http: BokaMeraHTTPClient) -> None:
        self._http = http

    # ── Version ──────────────────────────────────────────────────────────────

    def get_version(self) -> dict:
        """Retrieve the current API version information.

        Returns:
            Raw API response dict with version details.
        """
        return self._http.get("/version")

    def check_compatibility(self, *, identifier: str, version: str) -> dict:
        """Check whether a client version is compatible with the current API.

        Args:
            identifier: Client application identifier.
            version: Client version string to check (e.g. ``"1.2.3"``).

        Returns:
            Raw API response dict indicating compatibility status.
        """
        return self._http.get("/version/compability", {"Identifier": identifier, "Version": version})

    # ── Access key types ─────────────────────────────────────────────────────

    def list_access_key_types(self, *, skip: int | None = None, take: int | None = None) -> list[dict]:
        """List available access key types.

        Args:
            skip: Pagination offset.
            take: Maximum results to return.

        Returns:
            A list of access key type dicts.
        """
        params = {"Skip": skip, "Take": take}
        data = self._http.get("/accesskeytypes", params)
        if isinstance(data, list):
            return data
        return data.get("Results", [])

    # ── Error reporting ──────────────────────────────────────────────────────

    def report_error(
        self,
        *,
        exception_name: str | None = None,
        exception_message: str | None = None,
        exception_source: str | None = None,
        stack_trace: str | None = None,
        url: str | None = None,
    ) -> dict:
        """Report a client-side error to the BokaMera error log.

        Args:
            exception_name: Class name or type of the exception.
            exception_message: Human-readable exception message.
            exception_source: Source location where the exception occurred.
            stack_trace: Full stack trace string.
            url: URL that was being accessed when the error occurred.

        Returns:
            Raw API response dict confirming the error report.
        """
        body = {
            "ExceptionName": exception_name,
            "ExceptionMessage": exception_message,
            "ExceptionSource": exception_source,
            "StackTrace": stack_trace,
            "URL": url,
        }
        return self._http.post("/errors/", body)

    # ── Settings ─────────────────────────────────────────────────────────────

    def get_booking_settings(self, *, company_id: UUID | str | None = None, **includes: bool) -> dict:
        """Retrieve booking settings for a company.

        Args:
            company_id: Target company (defaults to the client's company).
            **includes: Boolean flags for optional related data (e.g. ``IncludePaymentSettings=True``).

        Returns:
            Raw API response dict containing the booking settings.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            **includes,
        }
        return self._http.get("/settings", params)

    # ── Categories ───────────────────────────────────────────────────────────

    def list_categories(self, *, id_: int | None = None) -> list[dict]:
        """List company categories.

        Args:
            id_: Filter to a single category by ID.

        Returns:
            A list of category dicts.
        """
        data = self._http.get("/categories", {"Id": id_})
        if isinstance(data, list):
            return data
        return data.get("Results", [])

    def create_category(self, *, name: str) -> dict:
        """Create a new company category.

        Args:
            name: Display name of the category.

        Returns:
            Raw API response dict for the created category.
        """
        return self._http.post("/categories", {"Name": name})

    # ── Ratings ──────────────────────────────────────────────────────────────

    def create_rating(
        self,
        *,
        company_id: UUID | str,
        booking_id: int,
        identifier: str,
        rating_score: int,
        review: dict | None = None,
    ) -> dict:
        """Submit a customer rating for a booking.

        Args:
            company_id: UUID of the company being rated.
            booking_id: ID of the booking the rating relates to.
            identifier: Unique token identifying the rating request (from the email link).
            rating_score: Numeric rating score.
            review: Optional dict containing a written review (``Heading``, ``Body``).

        Returns:
            Raw API response dict confirming the rating submission.
        """
        body = {
            "CompanyId": str(company_id),
            "BookingId": booking_id,
            "Identifier": identifier,
            "RatingScore": rating_score,
            "Review": review,
        }
        return self._http.post("/rating/", body)

    # ── References ───────────────────────────────────────────────────────────

    def list_references(
        self,
        *,
        company_id: UUID | str | None = None,
        id_: int | None = None,
        owner_id: UUID | str | None = None,
        reference_type: str | None = None,
        external_data: str | None = None,
    ) -> list[dict]:
        """List external reference records for a company.

        Args:
            company_id: Target company (defaults to the client's company).
            id_: Filter to a single reference by ID.
            owner_id: Filter to references owned by this entity UUID.
            reference_type: Filter by reference type string.
            external_data: Filter by the external data payload.

        Returns:
            A list of reference dicts.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Id": id_,
            "OwnerId": str(owner_id) if owner_id else None,
            "ReferenceType": reference_type,
            "ExternalData": external_data,
        }
        data = self._http.get("/references", params)
        if isinstance(data, list):
            return data
        return data.get("Results", [])

    def create_reference(
        self,
        *,
        owner_id: UUID | str,
        reference_type: str,
        external_data: str,
        reference_type_id: int | None = None,
        created_by: str | None = None,
        company_id: UUID | str | None = None,
    ) -> dict:
        """Create an external reference record.

        Args:
            owner_id: UUID of the entity this reference belongs to.
            reference_type: String identifying the type of reference.
            external_data: External data payload (e.g. an ID from a third-party system).
            reference_type_id: Numeric ID of the reference type.
            created_by: Identifier of the system or user creating the reference.
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw API response dict for the created reference.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "OwnerId": str(owner_id),
            "ReferenceType": reference_type,
            "ReferenceTypeId": reference_type_id,
            "ExternalData": external_data,
            "CreatedBy": created_by,
        }
        return self._http.post("/references", body)

    def delete_reference(self, company_id: UUID | str, reference_id: UUID | str) -> dict:
        """Delete a specific external reference record.

        Args:
            company_id: UUID of the company that owns the reference.
            reference_id: UUID of the reference to delete.

        Returns:
            Raw API response dict for the deletion.
        """
        return self._http.delete(f"/references/{company_id}/{reference_id}")

    def delete_references_by_owner(self, company_id: UUID | str, owner_id: UUID | str, reference_type: str) -> dict:
        """Delete all external references for an owner entity of a given type.

        Args:
            company_id: UUID of the company that owns the references.
            owner_id: UUID of the owner entity whose references should be deleted.
            reference_type: Reference type string to filter deletions.

        Returns:
            Raw API response dict for the deletion.
        """
        return self._http.delete(f"/references/{company_id}/{owner_id}/{reference_type}")

    def list_external_reference_types(self, *, company_id: UUID | str | None = None) -> list[dict]:
        """List available external reference type definitions.

        Args:
            company_id: Target company (defaults to the client's company).

        Returns:
            A list of external reference type dicts.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        data = self._http.get("/externalreferencestypes", params)
        if isinstance(data, list):
            return data
        return data.get("Results", [])

    # ── Lookup data ──────────────────────────────────────────────────────────

    def list_countries(self, *, id_: str | None = None) -> QueryResponse[CountryResponse]:
        """List available countries.

        Args:
            id_: Filter to a single country by ISO code.

        Returns:
            A paginated response of :class:`~bokamera.models.common.CountryResponse` objects.
        """
        return QueryResponse.from_dict(self._http.get("/countries", {"Id": id_}), CountryResponse)

    def list_currencies(self, *, id_: str | None = None, active: bool | None = None) -> QueryResponse[CurrencyResponse]:
        """List available currencies.

        Args:
            id_: Filter to a single currency by ISO code.
            active: When set, filter by active/inactive status.

        Returns:
            A paginated response of :class:`~bokamera.models.common.CurrencyResponse` objects.
        """
        return QueryResponse.from_dict(self._http.get("/currencies", {"Id": id_, "Active": active}), CurrencyResponse)

    def list_cities(self, country_id: str, *, skip: int | None = None, take: int | None = None) -> QueryResponse[GeoCity]:
        """List cities for a given country.

        Args:
            country_id: ISO country code to list cities for.
            skip: Pagination offset.
            take: Maximum results to return.

        Returns:
            A paginated response of :class:`~bokamera.models.common.GeoCity` objects.
        """
        params = {"Skip": skip, "Take": take}
        return QueryResponse.from_dict(self._http.get(f"/geodata/{country_id}/cities/", params), GeoCity)

    # ── Google Meet ──────────────────────────────────────────────────────────

    def get_google_meet_auth_url(self, resource_id: int, *, company_id: UUID | str | None = None) -> dict:
        """Retrieve the Google Meet OAuth authorisation URL for a resource.

        Args:
            resource_id: ID of the resource to authorise Google Meet for.
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw API response dict containing the authorisation URL.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return self._http.get(f"/google/meet/auth/{resource_id}", params)

    def disconnect_google_meet(self, resource_id: int, *, company_id: UUID | str | None = None) -> dict:
        """Disconnect Google Meet for a resource.

        Args:
            resource_id: ID of the resource to disconnect.
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw API response dict for the disconnection.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return self._http.delete(f"/google/meet/auth/{resource_id}", params)

    def get_google_meet_status(self, resource_id: int, *, company_id: UUID | str | None = None) -> dict:
        """Retrieve the Google Meet connection status for a resource.

        Args:
            resource_id: ID of the resource to check.
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw API response dict indicating the connection status.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return self._http.get(f"/google/meet/status/{resource_id}", params)

    # ── Mailchimp ────────────────────────────────────────────────────────────

    def get_mailchimp_profile(self, *, company_id: UUID | str | None = None) -> dict:
        """Retrieve the Mailchimp integration profile for a company.

        Args:
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw API response dict with the Mailchimp profile details.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return self._http.get("/mailchimp/profile", params)

    def update_mailchimp_profile(self, *, api_key: str, audience_id: str, company_id: UUID | str | None = None) -> dict:
        """Update the Mailchimp API credentials for a company.

        Args:
            api_key: Mailchimp API key.
            audience_id: Mailchimp audience (list) ID to sync with.
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw API response dict with the updated profile.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "MailChimpApiKey": api_key,
            "MailChimpAudienceId": audience_id,
        }
        return self._http.put("/mailchimp/profile", body)

    def list_mailchimp_audiences(self, *, company_id: UUID | str | None = None) -> list[dict]:
        """List Mailchimp audiences (lists) accessible to a company.

        Args:
            company_id: Target company (defaults to the client's company).

        Returns:
            A list of audience dicts from Mailchimp.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        data = self._http.get("/mailchimp/audience/company", params)
        return data if isinstance(data, list) else data.get("Results", [])

    def list_mailchimp_sync_executions(self, *, company_id: UUID | str | None = None, created_date: str | None = None) -> list[dict]:
        """List Mailchimp sync execution logs for a company.

        Args:
            company_id: Target company (defaults to the client's company).
            created_date: ISO date string to filter executions created on this date.

        Returns:
            A list of sync execution log dicts.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "CreatedDate": created_date,
        }
        data = self._http.get("/mailchimp/syncExecutions", params)
        if isinstance(data, list):
            return data
        return data.get("Results", [])
