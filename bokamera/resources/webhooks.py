"""
Resource namespace for webhook endpoint operations.

Exposes methods for retrieving, creating, and deleting webhook endpoints that
receive BokaMera event notifications.
"""

from __future__ import annotations

from uuid import UUID

from .._client import BokaMeraHTTPClient
from ..models.webhooks import WebhookEndpointResponse


class WebhookResource:
    """Webhook endpoint operations: get, create, and delete."""

    def __init__(self, http: BokaMeraHTTPClient) -> None:
        self._http = http

    def get(self, endpoint_id: UUID | str, *, include_secret: bool = False, company_id: UUID | str | None = None) -> WebhookEndpointResponse:
        """Retrieve a webhook endpoint by ID.

        Args:
            endpoint_id: UUID of the webhook endpoint to retrieve.
            include_secret: When ``True``, include the signing secret in the response.
            company_id: Target company (defaults to the client's company).

        Returns:
            The :class:`~bokamera.models.webhooks.WebhookEndpointResponse` for this endpoint.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "IncludeSecret": include_secret,
        }
        return WebhookEndpointResponse.from_dict(self._http.get(f"/webhook/endpoints/{endpoint_id}", params))

    def create(
        self,
        *,
        url: str,
        event_types: list[str],
        description: str | None = None,
        disabled: bool = False,
        company_id: UUID | str | None = None,
    ) -> WebhookEndpointResponse:
        """Create a new webhook endpoint.

        Args:
            url: HTTPS URL that event payloads should be delivered to.
            event_types: List of event type names to subscribe to.
            description: Optional human-readable description of the endpoint's purpose.
            disabled: When ``True``, create the endpoint in a paused state.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.webhooks.WebhookEndpointResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Url": url,
            "EventTypes": event_types,
            "Description": description,
            "Disabled": disabled,
        }
        return WebhookEndpointResponse.from_dict(self._http.post("/webhook/endpoints", body))

    def delete(self, endpoint_id: UUID | str, *, company_id: UUID | str | None = None) -> dict:
        """Delete a webhook endpoint.

        Args:
            endpoint_id: UUID of the webhook endpoint to delete.
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw API response dict for the deletion.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return self._http.delete(f"/webhook/endpoints/{endpoint_id}", params)
