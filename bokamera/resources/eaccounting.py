"""
Resource namespace for Visma eEkonomi (eAccounting) integration operations.

Exposes methods for checking the OAuth connection, managing integration
settings, synchronising articles and customers, creating invoices and invoice
drafts, managing invoice notes, and listing payment terms.
"""

from __future__ import annotations

from uuid import UUID

from .._client import BokaMeraHTTPClient
from ..models.eaccounting import (
    EAccountingArticleResponse,
    EAccountingInvoiceResponse,
    EAccountingNoteResponse,
    EAccountingSettingsResponse,
    EAccountingTokenResponse,
)


class EAccountingResource:
    """Visma eEkonomi integration operations: tokens, settings, articles, invoices, and notes."""

    def __init__(self, http: BokaMeraHTTPClient) -> None:
        self._http = http

    # ── OAuth / token ────────────────────────────────────────────────────────

    def check_connection(self, *, company_id: UUID | str | None = None) -> EAccountingTokenResponse:
        """Check whether the eEkonomi OAuth connection is valid.

        Args:
            company_id: Target company (defaults to the client's company).

        Returns:
            An :class:`~bokamera.models.eaccounting.EAccountingTokenResponse` with the current token state.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return EAccountingTokenResponse.from_dict(self._http.get("/eaccounting/check", params))

    def get_token(self, *, company_id: UUID | str | None = None) -> EAccountingTokenResponse:
        """Retrieve the current OAuth token for the eEkonomi integration.

        Args:
            company_id: Target company (defaults to the client's company).

        Returns:
            An :class:`~bokamera.models.eaccounting.EAccountingTokenResponse` with the stored token.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return EAccountingTokenResponse.from_dict(self._http.get("/eaccounting/token", params))

    # ── Settings ─────────────────────────────────────────────────────────────

    def get_settings(self, *, company_id: UUID | str | None = None) -> EAccountingSettingsResponse:
        """Retrieve the eEkonomi integration settings for a company.

        Args:
            company_id: Target company (defaults to the client's company).

        Returns:
            An :class:`~bokamera.models.eaccounting.EAccountingSettingsResponse`.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return EAccountingSettingsResponse.from_dict(self._http.get("/eaccounting/settings", params))

    # ── Articles ─────────────────────────────────────────────────────────────

    def list_articles(self, *, company_id: UUID | str | None = None) -> list[EAccountingArticleResponse]:
        """List articles mapped to Visma eEkonomi for a company.

        Args:
            company_id: Target company (defaults to the client's company).

        Returns:
            A list of :class:`~bokamera.models.eaccounting.EAccountingArticleResponse` objects.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        data = self._http.get("/eaccounting/articles", params)
        if isinstance(data, list):
            return [EAccountingArticleResponse.from_dict(d) for d in data]
        return [EAccountingArticleResponse.from_dict(d) for d in data.get("Results", [])]

    def create_article(
        self,
        *,
        service_id: int,
        article_name: str,
        article_price: float | None = None,
        unit_id: str | None = None,
        coding_id: str | None = None,
        vat_rate: str | None = None,
        currency_sign: str | None = None,
        company_id: UUID | str | None = None,
    ) -> EAccountingArticleResponse:
        """Create a new article mapping between a BokaMera service and Visma eEkonomi.

        Args:
            service_id: ID of the BokaMera service to map.
            article_name: Display name of the article in eEkonomi.
            article_price: Price of the article in eEkonomi.
            unit_id: Visma unit identifier.
            coding_id: Visma account coding identifier.
            vat_rate: Visma VAT rate code.
            currency_sign: ISO currency code for the article (e.g. ``"SEK"``).
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.eaccounting.EAccountingArticleResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "ServiceId": service_id,
            "ArticleName": article_name,
            "ArticlePrice": article_price,
            "UnitId": unit_id,
            "CodingId": coding_id,
            "VatRate": vat_rate,
            "CurrencySign": currency_sign,
        }
        return EAccountingArticleResponse.from_dict(self._http.post("/eaccounting/articles", body))

    def list_default_articles(self, *, company_id: UUID | str | None = None) -> list[dict]:
        """List the default article definitions available in eEkonomi.

        Args:
            company_id: Target company (defaults to the client's company).

        Returns:
            A list of default article dicts from eEkonomi.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        data = self._http.get("/eaccounting/defaultarticles", params)
        return data if isinstance(data, list) else data.get("Results", [])

    def update_article_mappings(self, *, service_price_mappings: list[dict], company_id: UUID | str | None = None) -> dict:
        """Update the service-price to eEkonomi article mappings in bulk.

        Args:
            service_price_mappings: List of mapping dicts linking service prices to eEkonomi articles.
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw API response dict for the update.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "ServicePriceMappings": service_price_mappings,
        }
        return self._http.put("/eaccounting/article/mappings", body)

    # ── Customers ────────────────────────────────────────────────────────────

    def list_customers(self, *, page_number: int = 1, page_size: int = 50, company_id: UUID | str | None = None) -> dict:
        """List customers synced to Visma eEkonomi.

        Args:
            page_number: Page number for pagination (1-based).
            page_size: Number of customers per page.
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw API response dict containing the paginated customer list.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "PageNumber": page_number,
            "PageSize": page_size,
        }
        return self._http.get("/eaccounting/customers", params)

    # ── Invoices ─────────────────────────────────────────────────────────────

    def list_invoices(
        self,
        *,
        company_id: UUID | str | None = None,
        booking_id: int | None = None,
        paid: bool | None = None,
        include_invoice_lines: bool | None = None,
        include_invoice_notes: bool | None = None,
        include_invoice_address: bool | None = None,
    ) -> list[EAccountingInvoiceResponse]:
        """List invoices created in eEkonomi.

        Args:
            company_id: Target company (defaults to the client's company).
            booking_id: Filter to invoices linked to this booking ID.
            paid: When set, filter by paid/unpaid status.
            include_invoice_lines: Include line items in each invoice.
            include_invoice_notes: Include notes in each invoice.
            include_invoice_address: Include invoice address in each invoice.

        Returns:
            A list of :class:`~bokamera.models.eaccounting.EAccountingInvoiceResponse` objects.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "BookingId": booking_id,
            "Paid": paid,
            "IncludeInvoiceLines": include_invoice_lines,
            "IncludeInvoiceNotes": include_invoice_notes,
            "IncludeInvoiceAddress": include_invoice_address,
        }
        data = self._http.get("/eaccounting/invoices", params)
        if isinstance(data, list):
            return [EAccountingInvoiceResponse.from_dict(d) for d in data]
        return [EAccountingInvoiceResponse.from_dict(d) for d in data.get("Results", [])]

    def create_invoice(
        self,
        *,
        booking_id: int,
        terms_of_payment_id: str | None = None,
        invoice_customer_name: str | None = None,
        send_type: str | None = None,
        notes: list[dict] | None = None,
        rot_property_type: str | None = None,
        rot_reduced_invoicing_type: str | None = None,
        corporate_identity_number: str | None = None,
        invoice_address: dict | None = None,
        company_id: UUID | str | None = None,
    ) -> dict:
        """Create an invoice in eEkonomi from a BokaMera booking.

        Args:
            booking_id: ID of the booking to invoice.
            terms_of_payment_id: eEkonomi payment terms identifier.
            invoice_customer_name: Customer name to print on the invoice.
            send_type: Delivery method (e.g. ``"Email"``, ``"Print"``).
            notes: List of note dicts to attach to the invoice.
            rot_property_type: Swedish ROT property type code.
            rot_reduced_invoicing_type: Swedish ROT reduced-invoicing type code.
            corporate_identity_number: Customer's corporate identity number.
            invoice_address: Billing address dict for the invoice.
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw API response dict for the created invoice.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "BookingId": booking_id,
            "TermsOfPaymentId": terms_of_payment_id,
            "InvoiceCustomerName": invoice_customer_name,
            "SendType": send_type,
            "Notes": notes or [],
            "RotPropertyType": rot_property_type,
            "RotReducedInvoicingType": rot_reduced_invoicing_type,
            "CorporateIdentityNumber": corporate_identity_number,
            "InvoiceAddress": invoice_address,
        }
        return self._http.post("/eaccounting/invoice", body)

    def print_invoice(self, *, invoice_id: str, company_id: UUID | str | None = None) -> EAccountingInvoiceResponse:
        """Mark an eEkonomi invoice as printed and retrieve it.

        Args:
            invoice_id: eEkonomi invoice ID.
            company_id: Target company (defaults to the client's company).

        Returns:
            The :class:`~bokamera.models.eaccounting.EAccountingInvoiceResponse` after the print action.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "InvoiceId": invoice_id,
        }
        return EAccountingInvoiceResponse.from_dict(self._http.get("/eaccounting/invoice/print", params))

    # ── Invoice drafts ───────────────────────────────────────────────────────

    def list_invoice_drafts(
        self,
        *,
        company_id: UUID | str | None = None,
        booking_id: int | None = None,
        include_invoice_lines: bool | None = None,
        include_invoice_notes: bool | None = None,
        page_number: int = 1,
        page_size: int = 50,
    ) -> dict:
        """List invoice drafts in eEkonomi.

        Args:
            company_id: Target company (defaults to the client's company).
            booking_id: Filter to drafts linked to this booking ID.
            include_invoice_lines: Include line items in each draft.
            include_invoice_notes: Include notes in each draft.
            page_number: Page number for pagination (1-based).
            page_size: Number of drafts per page.

        Returns:
            Raw API response dict containing the paginated draft list.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "BookingId": booking_id,
            "IncludeInvoiceLines": include_invoice_lines,
            "IncludeInvoiceNotes": include_invoice_notes,
            "PageNumber": page_number,
            "PageSize": page_size,
        }
        return self._http.get("/eaccounting/invoicedrafts", params)

    def create_invoice_draft(
        self,
        *,
        booking_id: int,
        terms_of_payment_id: str | None = None,
        invoice_customer_name: str | None = None,
        rot_property_type: str | None = None,
        rot_reduced_invoicing_type: str | None = None,
        corporate_identity_number: str | None = None,
        invoice_address: dict | None = None,
        company_id: UUID | str | None = None,
    ) -> dict:
        """Create an invoice draft in eEkonomi from a BokaMera booking.

        Args:
            booking_id: ID of the booking to create a draft for.
            terms_of_payment_id: eEkonomi payment terms identifier.
            invoice_customer_name: Customer name to print on the draft.
            rot_property_type: Swedish ROT property type code.
            rot_reduced_invoicing_type: Swedish ROT reduced-invoicing type code.
            corporate_identity_number: Customer's corporate identity number.
            invoice_address: Billing address dict for the draft.
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw API response dict for the created draft.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "BookingId": booking_id,
            "TermsOfPaymentId": terms_of_payment_id,
            "InvoiceCustomerName": invoice_customer_name,
            "RotPropertyType": rot_property_type,
            "RotReducedInvoicingType": rot_reduced_invoicing_type,
            "CorporateIdentityNumber": corporate_identity_number,
            "InvoiceAddress": invoice_address,
        }
        return self._http.post("/eaccounting/invoicedraft", body)

    def convert_invoice_draft(
        self,
        *,
        invoice_draft_id: str,
        send_type: str,
        booking_id: int | None = None,
        company_id: UUID | str | None = None,
    ) -> dict:
        """Convert an invoice draft to a finalised invoice in eEkonomi.

        Args:
            invoice_draft_id: eEkonomi invoice draft ID to convert.
            send_type: Delivery method for the finalised invoice (e.g. ``"Email"``).
            booking_id: ID of the associated BokaMera booking.
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw API response dict for the converted invoice.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "InvoiceDraftId": invoice_draft_id,
            "SendType": send_type,
            "BookingId": booking_id,
        }
        return self._http.post("/eaccounting/invoicedrafts/convert", body)

    # ── Notes ────────────────────────────────────────────────────────────────

    def list_notes(self, *, company_id: UUID | str | None = None) -> list[EAccountingNoteResponse]:
        """List invoice notes available in eEkonomi.

        Args:
            company_id: Target company (defaults to the client's company).

        Returns:
            A list of :class:`~bokamera.models.eaccounting.EAccountingNoteResponse` objects.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        data = self._http.get("/eaccounting/notes", params)
        if isinstance(data, list):
            return [EAccountingNoteResponse.from_dict(d) for d in data]
        return [EAccountingNoteResponse.from_dict(d) for d in data.get("Results", [])]

    def create_note(self, *, text: str, company_id: UUID | str | None = None) -> EAccountingNoteResponse:
        """Create a new note in eEkonomi.

        Args:
            text: Note body text.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.eaccounting.EAccountingNoteResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Text": text,
        }
        return EAccountingNoteResponse.from_dict(self._http.post("/eaccounting/notes", body))

    # ── Terms of payments ────────────────────────────────────────────────────

    def list_terms_of_payments(
        self,
        *,
        terms_of_payment_type_id: int | None = None,
        company_id: UUID | str | None = None,
    ) -> list[dict]:
        """List payment terms available in eEkonomi.

        Args:
            terms_of_payment_type_id: Filter to a specific payment terms type.
            company_id: Target company (defaults to the client's company).

        Returns:
            A list of payment terms dicts from eEkonomi.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "TermsOfPaymentTypeId": terms_of_payment_type_id,
        }
        data = self._http.get("/eaccounting/termsofpayments", params)
        return data if isinstance(data, list) else data.get("Results", [])
