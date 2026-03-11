"""
Resource namespace for GDPR data operations.

Exposes methods for exporting all personal data held about a customer, listing
customers who have been inactive since a given date, and bulk-deleting those
inactive customer records.
"""

from __future__ import annotations

from datetime import date
from uuid import UUID

from .._client import BokaMeraHTTPClient
from ..models.gdpr import GDPRCustomerResponse, InactiveCustomerResponse


class GDPRResource:
    """GDPR operations: customer data export, inactive customer listing, and bulk deletion."""

    def __init__(self, http: BokaMeraHTTPClient) -> None:
        self._http = http

    def get_customer_data(self, customer_id: UUID | str, *, company_id: UUID | str) -> GDPRCustomerResponse:
        """Export all personal data held about a customer.

        Args:
            customer_id: UUID of the customer whose data to export.
            company_id: UUID of the company that owns the customer record.

        Returns:
            A :class:`~bokamera.models.gdpr.GDPRCustomerResponse` containing all stored personal data.
        """
        params = {"CompanyId": str(company_id)}
        return GDPRCustomerResponse.from_dict(self._http.get(f"/gdpr/customers/{customer_id}", params))

    def list_inactive_customers(
        self,
        *,
        inactive_since: date,
        company_id: UUID | str | None = None,
        include_customer_information: bool | None = None,
    ) -> list[InactiveCustomerResponse]:
        """List customers who have had no bookings since a given date.

        Args:
            inactive_since: Return customers with no bookings on or after this date.
            company_id: Target company (defaults to the client's company).
            include_customer_information: Include full customer profile details.

        Returns:
            A list of :class:`~bokamera.models.gdpr.InactiveCustomerResponse` objects.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "InactiveSince": inactive_since.isoformat(),
            "IncludeCustomerInformation": include_customer_information,
        }
        data = self._http.get("/gdpr/customers/inactive", params)
        if isinstance(data, list):
            return [InactiveCustomerResponse.from_dict(d) for d in data]
        return [InactiveCustomerResponse.from_dict(d) for d in data.get("Results", [])]

    def delete_inactive_customers(self, *, inactive_since: date, company_id: UUID | str | None = None) -> dict:
        """Delete all customers who have had no bookings since a given date.

        Args:
            inactive_since: Delete customers with no bookings on or after this date.
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw API response dict summarising the deletion.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "InactiveSince": inactive_since.isoformat(),
        }
        return self._http.delete("/gdpr/customers/inactive", params)
