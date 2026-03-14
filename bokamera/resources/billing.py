"""
Resource namespace for billing and payment operations.

Exposes methods for managing company billing information, listing invoices,
downloading invoice PDFs, configuring payment provider settings, and
interacting with the Stripe payment integration.
"""

from __future__ import annotations

from uuid import UUID

from .._client import BokaMeraHTTPClient
from ..models.billing import (
    BillingInformationResponse,
    BillingMethodResponse,
    CompanyInvoiceResponse,
    PaymentSettingsResponse,
    StripeCheckoutStatusResponse,
    StripeWebhookResponse,
)
from ..models.common import QueryResponse


class BillingResource:
    """Billing operations: methods, invoices, payment settings, and Stripe integration."""

    def __init__(self, http: BokaMeraHTTPClient) -> None:
        self._http = http

    def list_methods(self, *, country_id: str | None = None) -> QueryResponse[BillingMethodResponse]:
        """List available billing/payment methods.

        Args:
            country_id: ISO country code to filter methods available in that country.

        Returns:
            A paginated response of :class:`~bokamera.models.billing.BillingMethodResponse` objects.
        """
        return QueryResponse.from_dict(
            self._http.get("/billing/methods", {"CountryId": country_id}), BillingMethodResponse
        )

    def get_company_billing(
        self,
        *,
        company_id: UUID | str | None = None,
        include_billing_method_options: bool | None = None,
    ) -> list[BillingMethodResponse]:
        """Retrieve the active billing methods configured for a company.

        Args:
            company_id: Target company (defaults to the client's company).
            include_billing_method_options: Include provider-specific option details.

        Returns:
            A list of :class:`~bokamera.models.billing.BillingMethodResponse` objects.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "IncludeBillingMethodOptions": include_billing_method_options,
        }
        data = self._http.get("/billing/company", params)
        if isinstance(data, list):
            return [BillingMethodResponse.from_dict(d) for d in data]
        return [BillingMethodResponse.from_dict(d) for d in data.get("Results", [])]

    def create_billing(
        self,
        *,
        license_plan_id: int,
        name: str | None = None,
        email: str | None = None,
        vat_registration_number: str | None = None,
        street: str | None = None,
        city: str | None = None,
        zip_code: str | None = None,
        country_id: str | None = None,
        attention: str | None = None,
        street2: str | None = None,
        payment_terms_days: int | None = None,
        gln: str | None = None,
        reference_line1: str | None = None,
        reference_line2: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        phone_number: str | None = None,
        billing_method_id: int | None = None,
        company_id: UUID | str | None = None,
    ) -> BillingInformationResponse:
        """Create billing information for a company.

        Args:
            license_plan_id: ID of the license plan to associate with the billing record.
            name: Billing contact or company name.
            email: Billing contact email address.
            vat_registration_number: VAT registration number for invoicing.
            street: Street address for the billing record.
            city: City for the billing record.
            zip_code: Postal code for the billing record.
            country_id: ISO country code for the billing record.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.billing.BillingInformationResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "LicensePlanId": license_plan_id,
            "Name": name,
            "Email": email,
            "VatRegistrationNumber": vat_registration_number,
            "Street": street,
            "City": city,
            "ZipCode": zip_code,
            "CountryId": country_id,
            "Attention": attention,
            "Street2": street2,
            "PaymentTermsDays": payment_terms_days,
            "GLN": gln,
            "ReferenceLine1": reference_line1,
            "ReferenceLine2": reference_line2,
            "FirstName": first_name,
            "LastName": last_name,
            "PhoneNumber": phone_number,
            "BillingMethodId": billing_method_id,
        }
        return BillingInformationResponse.from_dict(self._http.post("/billing/company/", body))

    def update_billing(
        self,
        *,
        license_plan_id: int,
        name: str | None = None,
        email: str | None = None,
        vat_registration_number: str | None = None,
        attention: str | None = None,
        street1: str | None = None,
        street2: str | None = None,
        zip_code: str | None = None,
        city: str | None = None,
        country_id: str | None = None,
        payment_terms_days: int | None = None,
        gln: str | None = None,
        reference_line1: str | None = None,
        reference_line2: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        phone_number: str | None = None,
        billing_method_id: int | None = None,
        company_id: UUID | str | None = None,
    ) -> BillingInformationResponse:
        """Update the billing information for a company.

        Args:
            license_plan_id: ID of the license plan associated with this billing record.
            name: Updated billing contact or company name.
            email: Updated billing contact email.
            vat_registration_number: Updated VAT registration number.
            attention: Attention line for the billing address.
            street1: Primary street address.
            street2: Secondary street address line.
            zip_code: Postal code.
            city: City name.
            country_id: ISO country code.
            payment_terms_days: Number of days for payment terms.
            gln: GLN (Global Location Number) for e-invoicing.
            reference_line1: Invoice reference line 1.
            reference_line2: Invoice reference line 2.
            first_name: First name of the billing contact.
            last_name: Last name of the billing contact.
            phone_number: Phone number of the billing contact.
            billing_method_id: ID of the billing method to use.
            company_id: Target company (defaults to the client's company).

        Returns:
            The updated :class:`~bokamera.models.billing.BillingInformationResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "LicensePlanId": license_plan_id,
            **{k: v for k, v in {
                "Name": name,
                "Email": email,
                "VatRegistrationNumber": vat_registration_number,
                "Attention": attention,
                "Street1": street1,
                "Street2": street2,
                "ZipCode": zip_code,
                "City": city,
                "CountryId": country_id,
                "PaymentTermsDays": payment_terms_days,
                "GLN": gln,
                "ReferenceLine1": reference_line1,
                "ReferenceLine2": reference_line2,
                "FirstName": first_name,
                "LastName": last_name,
                "PhoneNumber": phone_number,
                "BillingMethodId": billing_method_id,
            }.items() if v is not None},
        }
        return BillingInformationResponse.from_dict(self._http.put("/billing/company/", body))

    def list_invoices(
        self,
        *,
        company_id: UUID | str | None = None,
        id_: int | None = None,
        status_id: int | None = None,
        include_invoice_lines: bool | None = None,
        include_currency_information: bool | None = None,
        include_invoice_status_information: bool | None = None,
    ) -> QueryResponse[CompanyInvoiceResponse]:
        """List invoices for a company.

        Args:
            company_id: Target company (defaults to the client's company).
            id_: Filter to a single invoice by ID.
            status_id: Filter by invoice status ID.
            include_invoice_lines: Include line items in each invoice.
            include_currency_information: Include currency details in each invoice.
            include_invoice_status_information: Include status label details.

        Returns:
            A paginated response of :class:`~bokamera.models.billing.CompanyInvoiceResponse` objects.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Id": id_,
            "StatusId": status_id,
            "IncludeInvoiceLines": include_invoice_lines,
            "IncludeCurrencyInformation": include_currency_information,
            "IncludeInvoiceStatusInformation": include_invoice_status_information,
        }
        return QueryResponse.from_dict(self._http.get("/billing/company/invoices", params), CompanyInvoiceResponse)

    def get_invoice_pdf(self, invoice_id: int, *, company_id: UUID | str | None = None) -> bytes:
        """Download an invoice as a PDF.

        Args:
            invoice_id: ID of the invoice to download.
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw PDF bytes for the invoice.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return self._http.get_bytes(f"/billing/company/invoices/{invoice_id}", params)

    # ── Payment settings ─────────────────────────────────────────────────────

    def create_payment_settings(
        self,
        *,
        payment_provider_id: int,
        enabled: bool = False,
        refund_on_cancel_booking: bool = False,
        default_admin_payment_options_id: int | None = None,
        company_id: UUID | str | None = None,
    ) -> PaymentSettingsResponse:
        """Create payment provider settings for a company.

        Args:
            payment_provider_id: ID of the payment provider to configure.
            enabled: Whether the payment integration is immediately enabled.
            refund_on_cancel_booking: Automatically refund when a booking is cancelled.
            default_admin_payment_options_id: Default payment option for admin-created bookings.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.billing.PaymentSettingsResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "PaymentProviderId": payment_provider_id,
            "Enabled": enabled,
            "RefundOnCancelBooking": refund_on_cancel_booking,
            "DefaultAdminPaymentOptionsId": default_admin_payment_options_id,
        }
        return PaymentSettingsResponse.from_dict(self._http.post("/payment/settings", body))

    def create_qvickly_settings(
        self,
        *,
        id_: str,
        secret: str,
        receiver_email: str | None = None,
        receiver_firstname: str | None = None,
        receiver_lastname: str | None = None,
        company_id: UUID | str | None = None,
    ) -> dict:
        """Configure Qvickly (Billmate) payment provider credentials for a company.

        Args:
            id_: Qvickly merchant ID.
            secret: Qvickly API secret.
            receiver_email: Email address of the payment receiver.
            receiver_firstname: First name of the payment receiver.
            receiver_lastname: Last name of the payment receiver.
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw API response dict for the Qvickly settings.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Id": id_,
            "Secret": secret,
            "ReceiverEmail": receiver_email,
            "ReceiverFirstname": receiver_firstname,
            "ReceiverLastname": receiver_lastname,
        }
        return self._http.post("/payment/billmate/apisettings", body)

    # ── Stripe ───────────────────────────────────────────────────────────────

    def list_stripe_webhooks(self, *, webhook_id: str, company_id: UUID | str | None = None) -> list[StripeWebhookResponse]:
        """List Stripe webhook endpoints registered for a company.

        Args:
            webhook_id: Stripe webhook ID to filter by.
            company_id: Target company (defaults to the client's company).

        Returns:
            A list of :class:`~bokamera.models.billing.StripeWebhookResponse` objects.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "WebhookId": webhook_id,
        }
        data = self._http.get("/payment/stripe/v1/webhook", params)
        if isinstance(data, list):
            return [StripeWebhookResponse.from_dict(d) for d in data]
        return [StripeWebhookResponse.from_dict(d) for d in data.get("Results", [])]

    def create_stripe_webhook(
        self,
        *,
        url: str,
        events: list[str],
        connect: bool = False,
        company_id: UUID | str | None = None,
    ) -> StripeWebhookResponse:
        """Register a new Stripe webhook endpoint.

        Args:
            url: HTTPS URL that Stripe should deliver events to.
            events: List of Stripe event types to subscribe to (e.g. ``["charge.succeeded"]``).
            connect: When ``True``, register on the Stripe Connect account.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly registered :class:`~bokamera.models.billing.StripeWebhookResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Url": url,
            "Events": events,
            "Connect": connect,
        }
        return StripeWebhookResponse.from_dict(self._http.post("/payment/stripe/v1/webhook", body))

    def get_stripe_checkout_status(self, *, company_id: UUID | str, session_id: str) -> StripeCheckoutStatusResponse:
        """Retrieve the status of a Stripe Checkout session.

        Args:
            company_id: UUID of the company that initiated the checkout.
            session_id: Stripe Checkout session ID.

        Returns:
            A :class:`~bokamera.models.billing.StripeCheckoutStatusResponse` with payment status details.
        """
        body = {"CompanyId": str(company_id), "SessionId": session_id}
        return StripeCheckoutStatusResponse.from_dict(self._http.post("/payment/stripe/v1/checkout/status", body))
