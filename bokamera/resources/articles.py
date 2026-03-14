"""
Resource namespace for article operations.

Exposes methods for creating, listing, updating, and deleting articles
(add-on products), as well as listing article types, payment logs, and
downloading article reports.
"""

from __future__ import annotations

from uuid import UUID

from .._client import BokaMeraHTTPClient
from ..models.articles import ArticleResponse, ArticleTypeResponse, PaymentLogResponse
from ..models.common import QueryResponse


class ArticleResource:
    """Article operations: CRUD, types, payment logs, and reports."""

    def __init__(self, http: BokaMeraHTTPClient) -> None:
        self._http = http

    def list(
        self,
        *,
        article_type_id: int,
        active: bool = True,
        id_: int | None = None,
        company_id: UUID | str | None = None,
        include_service_information: bool | None = None,
        is_article_payable: bool | None = None,
    ) -> QueryResponse[ArticleResponse]:
        """List articles for a company.

        Args:
            article_type_id: Filter to articles of this type.
            active: When ``True``, return only active articles.
            id_: Filter to a single article by ID.
            company_id: Target company (defaults to the client's company).

        Returns:
            A paginated response of :class:`~bokamera.models.articles.ArticleResponse` objects.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Id": id_,
            "Active": active,
            "ArticleTypeId": article_type_id,
            "IncludeServiceInformation": include_service_information,
            "IsArticlePayable": is_article_payable,
        }
        return QueryResponse.from_dict(self._http.get("/articles", params), ArticleResponse)

    def create(
        self,
        *,
        name: str,
        article_type_id: int,
        price: float,
        description: str | None = None,
        currency_id: str | None = None,
        duration: int | None = None,
        service_ids: list[int] | None = None,
        active: bool = True,
        amount: int | None = None,
        sort_order: int | None = None,
        vat: float | None = None,
        valid_days: int | None = None,
        company_id: UUID | str | None = None,
    ) -> ArticleResponse:
        """Create a new article.

        Args:
            name: Display name of the article.
            article_type_id: ID of the article type (e.g. add-on, subscription).
            price: Price of the article.
            description: Optional description shown to customers.
            currency_id: ISO currency code (e.g. ``"SEK"``).
            duration: Duration in minutes, if the article adds time to a booking.
            service_ids: Service IDs this article can be added to.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.articles.ArticleResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Name": name,
            "ArticleTypeId": article_type_id,
            "Price": price,
            "Description": description,
            "CurrencyId": currency_id,
            "Duration": duration,
            "ServiceIds": service_ids or [],
            "Active": active,
            "Amount": amount,
            "SortOrder": sort_order,
            "VAT": vat,
            "ValidDays": valid_days,
        }
        return ArticleResponse.from_dict(self._http.post("/articles", body))

    def update(self, article_id: int, *, company_id: UUID | str | None = None, **kwargs: object) -> ArticleResponse:
        """Update an existing article.

        Args:
            article_id: ID of the article to update.
            company_id: Target company (defaults to the client's company).
            **kwargs: Article fields to update (e.g. ``Name``, ``Price``, ``Active``).

        Returns:
            The updated :class:`~bokamera.models.articles.ArticleResponse`.
        """
        body = {"CompanyId": str(company_id) if company_id else self._http.default_company_id, **kwargs}
        return ArticleResponse.from_dict(self._http.put(f"/articles/{article_id}", body))

    def delete(self, article_id: int, *, company_id: UUID | str | None = None) -> int:
        """Delete an article.

        Args:
            article_id: ID of the article to delete.
            company_id: Target company (defaults to the client's company).

        Returns:
            The ID of the deleted article.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return self._http.delete(f"/articles/{article_id}", params)

    def list_types(self, *, company_id: UUID | str | None = None) -> list[ArticleTypeResponse]:
        """List available article types.

        Args:
            company_id: Target company (defaults to the client's company).

        Returns:
            A list of :class:`~bokamera.models.articles.ArticleTypeResponse` objects.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        data = self._http.get("/articles/types", params)
        if isinstance(data, list):
            return [ArticleTypeResponse.from_dict(d) for d in data]
        return [ArticleTypeResponse.from_dict(d) for d in data.get("Results", [])]

    def list_payments(
        self,
        *,
        article_type_id: int,
        company_id: UUID | str | None = None,
        created_from: str | None = None,
        created_to: str | None = None,
        include_article_type: bool | None = None,
    ) -> QueryResponse[PaymentLogResponse]:
        """List payment log entries for articles of a given type.

        Args:
            article_type_id: Filter payments to articles of this type.
            company_id: Target company (defaults to the client's company).
            created_from: ISO date string — return payments on or after this date.
            created_to: ISO date string — return payments on or before this date.

        Returns:
            A paginated response of :class:`~bokamera.models.articles.PaymentLogResponse` objects.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "ArticleTypeId": article_type_id,
            "CreatedFrom": created_from,
            "CreatedTo": created_to,
            "IncludeArticleType": include_article_type,
        }
        return QueryResponse.from_dict(self._http.get("/articles/payments", params), PaymentLogResponse)

    def get_report(self, internal_reference_id: str, *, article_type_id: int, company_id: UUID | str | None = None) -> bytes:
        """Download a report for a specific article payment.

        Args:
            internal_reference_id: Internal reference identifier for the article payment.
            article_type_id: Article type ID used to scope the report.
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw report bytes (typically a PDF).
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "ArticleTypeId": article_type_id,
        }
        return self._http.get_bytes(f"/articles/{internal_reference_id}/reports", params)
