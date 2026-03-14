"""
Resource namespace for customer operations.

Exposes methods for creating, listing, updating, and deleting customers, as
well as managing customer comments and customer article subscriptions.
"""

from __future__ import annotations

from uuid import UUID

from .._client import BokaMeraHTTPClient
from ..models.common import InvoiceAddress, QueryResponse
from ..models.customers import CustomerArticleResponse, CustomerCommentResponse, CustomerResponse


class CustomerResource:
    """Customer operations: CRUD, comments, and article subscriptions."""

    def __init__(self, http: BokaMeraHTTPClient) -> None:
        self._http = http

    def list(
        self,
        *,
        company_id: UUID | str | None = None,
        customer_id: UUID | str | None = None,
        user_id: UUID | str | None = None,
        search: str | None = None,
        visible: bool | None = None,
        include_custom_field_values: bool | None = None,
        include_comments: bool | None = None,
        include_access_keys: bool | None = None,
        include_invoice_address: bool | None = None,
        skip: int | None = None,
        take: int | None = None,
    ) -> list[CustomerResponse]:
        """List customers for a company.

        Args:
            company_id: Target company (defaults to the client's company).
            customer_id: Filter to a single customer by UUID.
            user_id: Filter to the customer linked to this user UUID.
            search: Free-text search over customer name and email.
            visible: When set, filter by the customer's visibility flag.
            include_custom_field_values: Include custom field values for each customer.
            include_comments: Include internal comments for each customer.
            include_access_keys: Include access key records for each customer.
            include_invoice_address: Include invoice address for each customer.
            skip: Pagination offset.
            take: Maximum results to return.

        Returns:
            A list of :class:`~bokamera.models.customers.CustomerResponse` objects.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "CustomerId": str(customer_id) if customer_id else None,
            "UserId": str(user_id) if user_id else None,
            "Search": search,
            "Visible": visible,
            "IncludeCustomFieldValues": include_custom_field_values,
            "IncludeComments": include_comments,
            "IncludeAccessKeys": include_access_keys,
            "IncludeInvoiceAddress": include_invoice_address,
            "Skip": skip,
            "Take": take,
        }
        data = self._http.get("/customers", params)
        if isinstance(data, list):
            return [CustomerResponse.from_dict(d) for d in data]
        return [CustomerResponse.from_dict(d) for d in data.get("Results", [])]

    def create(
        self,
        *,
        firstname: str,
        lastname: str,
        email: str,
        phone: str | None = None,
        personal_identity_number: str | None = None,
        custom_fields: list[dict] | None = None,
        access_keys: list[dict] | None = None,
        invoice_address: InvoiceAddress | None = None,
        subscribed_to_newsletter: bool = False,
        company_id: UUID | str | None = None,
    ) -> CustomerResponse:
        """Create a new customer.

        Args:
            firstname: Customer's first name.
            lastname: Customer's last name.
            email: Customer's email address.
            phone: Customer's phone number.
            personal_identity_number: National identity number (e.g. Swedish personnummer).
            custom_fields: Custom field values to store on the customer.
            access_keys: Access key records to assign to the customer.
            invoice_address: Billing address for the customer.
            subscribed_to_newsletter: Whether the customer consents to newsletter emails.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.customers.CustomerResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Firstname": firstname,
            "Lastname": lastname,
            "Email": email,
            "Phone": phone,
            "PersonalIdentityNumber": personal_identity_number,
            "CustomFields": custom_fields or [],
            "AccessKeys": access_keys or [],
            "InvoiceAddress": invoice_address.to_dict() if invoice_address else None,
            "SubscribedToNewsletter": subscribed_to_newsletter,
        }
        return CustomerResponse.from_dict(self._http.post("/customers", body))

    def update(
        self,
        customer_id: UUID | str,
        *,
        company_id: UUID | str | None = None,
        firstname: str | None = None,
        lastname: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        personal_identity_number: str | None = None,
        custom_fields: list[dict] | None = None,
        access_keys: list[dict] | None = None,
        access_keys_to_delete: list[dict] | None = None,
        invoice_address: InvoiceAddress | None = None,
    ) -> CustomerResponse:
        """Update an existing customer.

        Args:
            customer_id: UUID of the customer to update.
            company_id: Target company (defaults to the client's company).
            firstname: New first name.
            lastname: New last name.
            email: New email address.
            phone: New phone number.
            personal_identity_number: New national identity number.
            custom_fields: Updated custom field values.
            access_keys: Access keys to add or update.
            access_keys_to_delete: Access keys to remove from the customer.
            invoice_address: Updated billing address.

        Returns:
            The updated :class:`~bokamera.models.customers.CustomerResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            **{k: v for k, v in {
                "Firstname": firstname,
                "Lastname": lastname,
                "Email": email,
                "Phone": phone,
                "PersonalIdentityNumber": personal_identity_number,
                "CustomFields": custom_fields,
                "AccessKeys": access_keys,
                "AccessKeysToDelete": access_keys_to_delete,
                "InvoiceAddress": invoice_address.to_dict() if invoice_address else None,
            }.items() if v is not None},
        }
        return CustomerResponse.from_dict(self._http.put(f"/customers/{customer_id}", body))

    def delete(self, customer_id: UUID | str, *, company_id: UUID | str | None = None) -> CustomerResponse:
        """Delete a customer.

        Args:
            customer_id: UUID of the customer to delete.
            company_id: Target company (defaults to the client's company).

        Returns:
            The deleted :class:`~bokamera.models.customers.CustomerResponse`.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return CustomerResponse.from_dict(self._http.delete(f"/customers/{customer_id}", params))

    # ── Comments ─────────────────────────────────────────────────────────────

    def list_comments(self, customer_id: UUID | str, *, company_id: UUID | str) -> QueryResponse[CustomerCommentResponse]:
        """List internal comments for a customer.

        Args:
            customer_id: UUID of the customer whose comments to list.
            company_id: UUID of the company that owns the customer record.

        Returns:
            A paginated response of :class:`~bokamera.models.customers.CustomerCommentResponse` objects.
        """
        params = {"CompanyId": str(company_id)}
        return QueryResponse.from_dict(
            self._http.get(f"/customers/{customer_id}/comments", params), CustomerCommentResponse
        )

    def add_comment(self, customer_id: UUID | str, *, comments: str, image_url: str | None = None, company_id: UUID | str | None = None) -> CustomerCommentResponse:
        """Add an internal comment to a customer.

        Args:
            customer_id: UUID of the customer to comment on.
            comments: Comment text.
            image_url: Optional URL of an image to attach to the comment.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.customers.CustomerCommentResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Comments": comments,
            "ImageUrl": image_url,
        }
        return CustomerCommentResponse.from_dict(self._http.post(f"/customers/{customer_id}/comments", body))

    def delete_comment(self, customer_id: UUID | str, comment_id: int, *, company_id: UUID | str | None = None) -> CustomerCommentResponse:
        """Delete an internal comment from a customer.

        Args:
            customer_id: UUID of the customer the comment belongs to.
            comment_id: ID of the comment to delete.
            company_id: Target company (defaults to the client's company).

        Returns:
            The deleted :class:`~bokamera.models.customers.CustomerCommentResponse`.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return CustomerCommentResponse.from_dict(self._http.delete(f"/customers/{customer_id}/comments/{comment_id}", params))

    # ── Customer articles ────────────────────────────────────────────────────

    def list_articles(
        self,
        *,
        company_id: UUID | str | None = None,
        id_: int | None = None,
        status_id: int | None = None,
        customer_id: UUID | str | None = None,
        include_customer_information: bool | None = None,
        include_article_information: bool | None = None,
        include_payment_log: bool | None = None,
    ) -> list[CustomerArticleResponse]:
        """List customer article subscriptions.

        Args:
            company_id: Target company (defaults to the client's company).
            id_: Filter to a single customer article by ID.
            status_id: Filter by subscription status ID.
            customer_id: Filter to articles for this customer UUID.
            include_customer_information: Include customer details in each result.
            include_article_information: Include article details in each result.
            include_payment_log: Include payment log entries in each result.

        Returns:
            A list of :class:`~bokamera.models.customers.CustomerArticleResponse` objects.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Id": id_,
            "StatusId": status_id,
            "CustomerId": str(customer_id) if customer_id else None,
            "IncludeCustomerInformation": include_customer_information,
            "IncludeArticleInformation": include_article_information,
            "IncludePaymentLog": include_payment_log,
        }
        data = self._http.get("/customerarticle", params)
        if isinstance(data, list):
            return [CustomerArticleResponse.from_dict(d) for d in data]
        return [CustomerArticleResponse.from_dict(d) for d in data.get("Results", [])]

    def create_article_from_article(
        self,
        *,
        article_id: int,
        customer: dict,
        invoice_address: InvoiceAddress | None = None,
        company_id: UUID | str | None = None,
    ) -> CustomerArticleResponse:
        """Create a customer article subscription from an article template.

        Args:
            article_id: ID of the article to subscribe the customer to.
            customer: Customer details dict (``Firstname``, ``Lastname``, ``Email``).
            invoice_address: Optional billing address for the subscription.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.customers.CustomerArticleResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "ArticleId": article_id,
            "Customer": customer,
            "InvoiceAddress": invoice_address.to_dict() if invoice_address else None,
        }
        return CustomerArticleResponse.from_dict(self._http.post("/customerarticle/fromarticle", body))
