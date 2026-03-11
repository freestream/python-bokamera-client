"""
Resource namespace for license and trial operations.

Exposes methods for listing, creating, and deleting company licenses, as well
as managing trial periods, querying license types and plans, and checking
domain availability.
"""

from __future__ import annotations

from uuid import UUID

from .._client import BokaMeraHTTPClient
from ..models.common import QueryResponse
from ..models.licenses import CompanyLicenseResponse, CompanyTrialResponse, LicensePlanResponse, LicenseTypeResponse


class LicenseResource:
    """License operations: company licenses, types, plans, domain checks, and trials."""

    def __init__(self, http: BokaMeraHTTPClient) -> None:
        self._http = http

    def list_company_licenses(
        self,
        *,
        company_id: UUID | str | None = None,
        only_active_licenses: bool | None = None,
        country_id: str | None = None,
        type_id: int | None = None,
        include_license_items: bool | None = None,
        include_license_prices: bool | None = None,
        include_voss_subscription: bool | None = None,
    ) -> list[CompanyLicenseResponse]:
        """List licenses assigned to a company.

        Args:
            company_id: Target company (defaults to the client's company).
            only_active_licenses: When ``True``, return only non-expired licenses.
            country_id: ISO country code to filter applicable licenses.
            type_id: Filter to licenses of this type ID.
            include_license_items: Include feature items in each license.
            include_license_prices: Include pricing details in each license.
            include_voss_subscription: Include Voss subscription data.

        Returns:
            A list of :class:`~bokamera.models.licenses.CompanyLicenseResponse` objects.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "OnlyActiveLicenses": only_active_licenses,
            "CountryId": country_id,
            "TypeId": type_id,
            "IncludeLicenseItems": include_license_items,
            "IncludeLicensePrices": include_license_prices,
            "IncludeVossSubscription": include_voss_subscription,
        }
        data = self._http.get("/licenses/company", params)
        if isinstance(data, list):
            return [CompanyLicenseResponse.from_dict(d) for d in data]
        return [CompanyLicenseResponse.from_dict(d) for d in data.get("Results", [])]

    def create_company_license(
        self,
        *,
        type_id: int,
        meta_data: str | None = None,
        billing_information: dict | None = None,
        company_id: UUID | str | None = None,
    ) -> CompanyLicenseResponse:
        """Assign a new license to a company.

        Args:
            type_id: ID of the license type to assign.
            meta_data: Optional metadata string for the license.
            billing_information: Billing details to associate with the license.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.licenses.CompanyLicenseResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "TypeId": type_id,
            "MetaData": meta_data,
            "BillingInformation": billing_information,
        }
        return CompanyLicenseResponse.from_dict(self._http.post("/licenses/company", body))

    def delete_company_license(self, license_id: int, *, company_id: UUID | str | None = None) -> CompanyLicenseResponse:
        """Remove a license from a company.

        Args:
            license_id: ID of the company license to remove.
            company_id: Target company (defaults to the client's company).

        Returns:
            The deleted :class:`~bokamera.models.licenses.CompanyLicenseResponse`.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return CompanyLicenseResponse.from_dict(self._http.delete(f"/licenses/company/{license_id}", params))

    def deactivate_company(self, *, deactivate: bool = True, questionnaire: list[dict] | None = None, company_id: UUID | str | None = None) -> CompanyLicenseResponse:
        """Deactivate (or reactivate) a company account.

        Args:
            deactivate: When ``True``, deactivate the company. When ``False``, reactivate.
            questionnaire: Optional list of questionnaire answers collected on deactivation.
            company_id: Target company (defaults to the client's company).

        Returns:
            The resulting :class:`~bokamera.models.licenses.CompanyLicenseResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Deactivate": deactivate,
            "Questionnaire": questionnaire or [],
        }
        return CompanyLicenseResponse.from_dict(self._http.post("/licenses/company/delete", body))

    def list_types(
        self,
        *,
        extra_license_option: bool | None = None,
        country_id: str | None = None,
        include_license_items: bool | None = None,
        include_license_prices: bool | None = None,
    ) -> QueryResponse[LicenseTypeResponse]:
        """List available license types.

        Args:
            extra_license_option: When set, filter to extra/add-on license types.
            country_id: ISO country code to filter types available in that country.
            include_license_items: Include feature items in each type.
            include_license_prices: Include pricing details in each type.

        Returns:
            A paginated response of :class:`~bokamera.models.licenses.LicenseTypeResponse` objects.
        """
        params = {
            "ExtraLicenseOption": extra_license_option,
            "CountryId": country_id,
            "IncludeLicenseItems": include_license_items,
            "IncludeLicensePrices": include_license_prices,
        }
        return QueryResponse.from_dict(self._http.get("/licenses/types/", params), LicenseTypeResponse)

    def list_plans(self, *, active: bool | None = None) -> QueryResponse[LicensePlanResponse]:
        """List available license plans (billing plan tiers).

        Args:
            active: When set, filter to active or inactive plans.

        Returns:
            A paginated response of :class:`~bokamera.models.licenses.LicensePlanResponse` objects.
        """
        return QueryResponse.from_dict(self._http.get("/licenses/plans/", {"Active": active}), LicensePlanResponse)

    def check_domain(self, *, domain_name: str) -> dict:
        """Check whether a domain name is available for use as a company site path.

        Args:
            domain_name: The domain or site path string to check.

        Returns:
            Raw API response dict indicating availability.
        """
        return self._http.get("/licenses/checkdomain/", {"DomainName": domain_name})

    # ── Trials ───────────────────────────────────────────────────────────────

    def list_trials(self, *, company_id: UUID | str | None = None, id_: int | None = None) -> list[CompanyTrialResponse]:
        """List trial periods for a company.

        Args:
            company_id: Target company (defaults to the client's company).
            id_: Filter to a single trial by ID.

        Returns:
            A list of :class:`~bokamera.models.licenses.CompanyTrialResponse` objects.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Id": id_,
        }
        data = self._http.get("/trials/company/", params)
        if isinstance(data, list):
            return [CompanyTrialResponse.from_dict(d) for d in data]
        return [CompanyTrialResponse.from_dict(d) for d in data.get("Results", [])]

    def create_trial(self, *, trial_type_id: int, company_id: UUID | str | None = None) -> CompanyTrialResponse:
        """Start a trial period for a company.

        Args:
            trial_type_id: ID of the trial type to activate.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.licenses.CompanyTrialResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "TrialTypeId": trial_type_id,
        }
        return CompanyTrialResponse.from_dict(self._http.post("/trials/company/", body))

    def check_trial(self, *, trial_type_id: int, company_id: UUID | str | None = None) -> dict:
        """Check whether a company is eligible to start a specific trial.

        Args:
            trial_type_id: ID of the trial type to check eligibility for.
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw API response dict indicating eligibility.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "TrialTypeId": trial_type_id,
        }
        return self._http.get("/trials/company/check", params)
