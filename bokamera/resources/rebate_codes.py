"""
Resource namespace for rebate code operations.

Exposes methods for creating, listing, updating, and deleting rebate codes
(discount codes), as well as looking up codes by their sign, managing
transactions, and generating reports.
"""

from __future__ import annotations

from datetime import date
from uuid import UUID

from .._client import BokaMeraHTTPClient
from ..models.common import InvoiceAddress
from ..models.rebate_codes import (
    RebateCodeResponse,
    RebateCodeStatusResponse,
    RebateCodeTransactionResponse,
    RebateCodeTypeResponse,
)


class RebateCodeResource:
    """Rebate code operations: CRUD, lookup by sign, transactions, and reports."""

    def __init__(self, http: BokaMeraHTTPClient) -> None:
        self._http = http

    def list(
        self,
        *,
        company_id: UUID | str | None = None,
        id_: int | None = None,
        active: bool | None = None,
        rebate_code_sign: str | None = None,
        rebate_code_type_ids: list[int] | None = None,
        include_connected_services: bool | None = None,
        include_connected_customers: bool | None = None,
        include_usages: bool | None = None,
        include_payment_log: bool | None = None,
        customer_id: UUID | str | None = None,
        include_code_type_options: bool | None = None,
        include_status_options: bool | None = None,
        include_connected_days_of_week: bool | None = None,
        include_article_information: bool | None = None,
        include_company_information: bool | None = None,
        company_rebate_codes: bool | None = None,
    ) -> list[RebateCodeResponse]:
        """List rebate codes for a company.

        Args:
            company_id: Target company (defaults to the client's company).
            id_: Filter to a single rebate code by ID.
            active: When set, filter by active/inactive status.
            rebate_code_sign: Filter by the code string (e.g. ``"SUMMER20"``).
            rebate_code_type_ids: Filter to codes of these type IDs.
            include_connected_services: Include services the code is valid for.
            include_connected_customers: Include customers the code is restricted to.
            include_usages: Include usage count details.
            include_payment_log: Include payment log entries for each code.
            customer_id: Filter to codes associated with this customer UUID.

        Returns:
            A list of :class:`~bokamera.models.rebate_codes.RebateCodeResponse` objects.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Id": id_,
            "Active": active,
            "RebateCodeSign": rebate_code_sign,
            "RebateCodeTypeIds": rebate_code_type_ids,
            "IncludeConnectedServices": include_connected_services,
            "IncludeConnectedCustomers": include_connected_customers,
            "IncludeUsages": include_usages,
            "IncludePaymentLog": include_payment_log,
            "CustomerId": str(customer_id) if customer_id else None,
            "IncludeCodeTypeOptions": include_code_type_options,
            "IncludeStatusOptions": include_status_options,
            "IncludeConnectedDaysOfWeek": include_connected_days_of_week,
            "IncludeArticleInformation": include_article_information,
            "IncludeCompanyInformation": include_company_information,
            "CompanyRebateCodes": company_rebate_codes,
        }
        data = self._http.get("/rebatecodes", params)
        if isinstance(data, list):
            return [RebateCodeResponse.from_dict(d) for d in data]
        return [RebateCodeResponse.from_dict(d) for d in data.get("Results", [])]

    def create(
        self,
        *,
        rebate_code_type_id: int,
        rebate_code_value: float,
        valid_from: date | None = None,
        valid_to: date | None = None,
        rebate_code_sign: str | None = None,
        max_number_of_uses: int | None = None,
        max_number_of_uses_per_customer: int | None = None,
        days_of_week: list[int] | None = None,
        services: list[dict] | None = None,
        customers: list[dict] | None = None,
        currency_id: str | None = None,
        promo_code_receiver: str | None = None,
        from_time: str | None = None,
        to_time: str | None = None,
        article_id: int | None = None,
        auto_generate_rebate_code_sign: bool | None = None,
        personal_note: str | None = None,
        price_vat: float | None = None,
        vat: float | None = None,
        invoice_address: dict | None = None,
        company_id: UUID | str | None = None,
    ) -> RebateCodeResponse:
        """Create a new rebate code.

        Args:
            rebate_code_type_id: ID of the rebate code type (e.g. percentage, fixed amount).
            rebate_code_value: Discount value (percentage or fixed amount depending on type).
            valid_from: Date from which the code is valid.
            valid_to: Date until which the code is valid.
            rebate_code_sign: Custom code string (e.g. ``"SUMMER20"``). Auto-generated if omitted.
            max_number_of_uses: Maximum total number of times the code can be used.
            max_number_of_uses_per_customer: Maximum uses per individual customer.
            days_of_week: Days of the week the code is valid (0 = Monday).
            services: List of service dicts this code applies to.
            customers: List of customer dicts this code is restricted to.
            currency_id: ISO currency code for fixed-amount codes.
            promo_code_receiver: Email address to notify when the code is used.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.rebate_codes.RebateCodeResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "RebateCodeTypeId": rebate_code_type_id,
            "RebateCodeValue": rebate_code_value,
            "ValidFrom": valid_from.isoformat() if valid_from else None,
            "ValidTo": valid_to.isoformat() if valid_to else None,
            "RebateCodeSign": rebate_code_sign,
            "MaxNumberOfUses": max_number_of_uses,
            "MaxNumberOfUsesPerCustomer": max_number_of_uses_per_customer,
            "DaysOfWeek": days_of_week or [],
            "Services": services or [],
            "Customers": customers or [],
            "CurrencyId": currency_id,
            "PromoCodeReceiver": promo_code_receiver,
            "FromTime": from_time,
            "ToTime": to_time,
            "ArticleId": article_id,
            "AutoGenerateRebateCodeSign": auto_generate_rebate_code_sign,
            "PersonalNote": personal_note,
            "PriceVat": price_vat,
            "VAT": vat,
            "InvoiceAddress": invoice_address,
        }
        return RebateCodeResponse.from_dict(self._http.post("/rebatecodes", body))

    def update(self, code_id: int, *, company_id: UUID | str | None = None, **kwargs: object) -> RebateCodeResponse:
        """Update an existing rebate code.

        Args:
            code_id: ID of the rebate code to update.
            company_id: Target company (defaults to the client's company).
            **kwargs: Rebate code fields to update (e.g. ``ValidTo``, ``MaxNumberOfUses``).

        Returns:
            The updated :class:`~bokamera.models.rebate_codes.RebateCodeResponse`.
        """
        body = {"CompanyId": str(company_id) if company_id else self._http.default_company_id, **kwargs}
        return RebateCodeResponse.from_dict(self._http.put(f"/rebatecodes/{code_id}", body))

    def delete(self, code_id: int, *, force_delete: bool = False, company_id: UUID | str | None = None) -> RebateCodeResponse:
        """Delete a rebate code.

        Args:
            code_id: ID of the rebate code to delete.
            force_delete: When ``True``, delete even if the code has been used.
            company_id: Target company (defaults to the client's company).

        Returns:
            The deleted :class:`~bokamera.models.rebate_codes.RebateCodeResponse`.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "ForceDelete": force_delete,
        }
        return RebateCodeResponse.from_dict(self._http.delete(f"/rebatecodes/{code_id}", params))

    def get_by_sign(
        self,
        *,
        company_id: UUID | str,
        rebate_code_sign: str,
        service_id: int | None = None,
        date: date | None = None,
        customer_email: str | None = None,
        include_connected_services: bool | None = None,
        include_connected_days_of_week: bool | None = None,
        include_connected_customers: bool | None = None,
    ) -> RebateCodeResponse:
        """Look up a rebate code by its code string.

        Args:
            company_id: UUID of the company that owns the code.
            rebate_code_sign: The code string to look up (e.g. ``"SUMMER20"``).
            service_id: Validate the code against this service ID.
            date: Validate the code's validity on this date.
            customer_email: Validate per-customer usage limits against this email.

        Returns:
            The matching :class:`~bokamera.models.rebate_codes.RebateCodeResponse`.
        """
        params = {
            "CompanyId": str(company_id),
            "RebateCodeSign": rebate_code_sign,
            "ServiceId": service_id,
            "Date": date.isoformat() if date else None,
            "CustomerEmail": customer_email,
            "IncludeConnectedServices": include_connected_services,
            "IncludeConnectedDaysOfWeek": include_connected_days_of_week,
            "IncludeConnectedCustomers": include_connected_customers,
        }
        return RebateCodeResponse.from_dict(self._http.get("/rebatecodes/getbysign", params))

    def list_statuses(self, *, id_: int | None = None) -> list[RebateCodeStatusResponse]:
        """List available rebate code status options.

        Args:
            id_: Filter to a single status by ID.

        Returns:
            A list of :class:`~bokamera.models.rebate_codes.RebateCodeStatusResponse` objects.
        """
        data = self._http.get("/rebatecodes/statuses", {"Id": id_})
        items = data.get("RebateCodeStatusItems", data if isinstance(data, list) else [])
        return [RebateCodeStatusResponse.from_dict(d) for d in items]

    def list_types(self, *, id_: int | None = None) -> list[RebateCodeTypeResponse]:
        """List available rebate code types.

        Args:
            id_: Filter to a single type by ID.

        Returns:
            A list of :class:`~bokamera.models.rebate_codes.RebateCodeTypeResponse` objects.
        """
        data = self._http.get("/rebatecodes/types", {"Id": id_})
        items = data.get("RebateCodeTypeItems", data if isinstance(data, list) else [])
        return [RebateCodeTypeResponse.from_dict(d) for d in items]

    def calculate_price(
        self,
        *,
        company_id: UUID | str | None = None,
        service_id: int | None = None,
        rebate_code_ids: list[int] | None = None,
        rebate_code_signs: list[str] | None = None,
        date_from: date | None = None,
    ) -> dict:
        """Calculate the discounted price for a service after applying rebate codes.

        Args:
            company_id: Target company (defaults to the client's company).
            service_id: ID of the service to price.
            rebate_code_ids: IDs of rebate codes to apply.
            rebate_code_signs: Code strings of rebate codes to apply.
            date_from: Date to use when evaluating date-restricted codes.

        Returns:
            Raw API response dict containing the calculated price breakdown.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "ServiceId": service_id,
            "RebateCodeIds": rebate_code_ids,
            "RebateCodeSigns": rebate_code_signs,
            "DateFrom": date_from.isoformat() if date_from else None,
        }
        return self._http.post("/rebatecodes/prices", body)

    def create_from_article(
        self,
        *,
        article_id: int,
        customer: dict,
        invoice_address: InvoiceAddress | None = None,
        receiver: dict | None = None,
        company_id: UUID | str | None = None,
    ) -> RebateCodeResponse:
        """Create a rebate code from an article purchase.

        Args:
            article_id: ID of the article being purchased.
            customer: Customer details dict (``Firstname``, ``Lastname``, ``Email``).
            invoice_address: Optional billing address for the purchase.
            receiver: Optional dict specifying who should receive the rebate code.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.rebate_codes.RebateCodeResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "ArticleId": article_id,
            "Customer": customer,
            "InvoiceAddress": invoice_address.to_dict() if invoice_address else None,
            "Receiver": receiver,
        }
        return RebateCodeResponse.from_dict(self._http.post("/rebatecodes/fromarticle", body))

    def create_transaction(
        self,
        *,
        rebate_code_id: int,
        amount: float,
        usage: float,
        booking_id: int | None = None,
        change_type: str = "Decrease",
        company_id: UUID | str | None = None,
    ) -> RebateCodeTransactionResponse:
        """Record a manual transaction against a rebate code (e.g. balance adjustment).

        Args:
            rebate_code_id: ID of the rebate code to transact against.
            amount: Monetary amount to adjust.
            usage: Usage count to adjust.
            booking_id: ID of the booking associated with this transaction.
            change_type: Direction of the change: ``"Decrease"`` or ``"Increase"``.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.rebate_codes.RebateCodeTransactionResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "RebateCodeId": rebate_code_id,
            "Amount": amount,
            "Usage": usage,
            "BookingId": booking_id,
            "ChangeType": change_type,
        }
        return RebateCodeTransactionResponse.from_dict(self._http.post("/rebatecodes/transactions", body))

    def get_report(
        self,
        rebate_code_id: int,
        *,
        send_receipt_method: str = "PdfExport",
        company_id: UUID | str | None = None,
    ) -> dict:
        """Retrieve a report for a rebate code.

        Args:
            rebate_code_id: ID of the rebate code to report on.
            send_receipt_method: Output format (e.g. ``"PdfExport"``).
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw API response dict for the report.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "SendReceiptMethod": send_receipt_method,
        }
        return self._http.get(f"/rebatecodes/{rebate_code_id}/reports", params)
