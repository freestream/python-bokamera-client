"""
Data models for the webhooks resource.

Contains the dataclass for webhook endpoint configurations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from .common import _uuid


@dataclass(slots=True)
class WebhookEndpointResponse:
    """A configured webhook endpoint that receives BokaMera event notifications.

    Attributes:
        id: UUID of the webhook endpoint.
        company_id: UUID of the company that owns this endpoint.
        url: HTTPS URL to which event payloads are delivered.
        description: Optional human-readable description of the endpoint's purpose.
        disabled: Whether the endpoint is currently paused (events are not delivered).
        event_types: List of event type names this endpoint subscribes to.
        secret: Signing secret used to verify the authenticity of incoming payloads.
    """

    id: UUID | None = None
    company_id: UUID | None = None
    url: str | None = None
    description: str | None = None
    disabled: bool = False
    event_types: list[str] = field(default_factory=list)
    secret: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> WebhookEndpointResponse:
        """Construct a WebhookEndpointResponse from a raw API response dict."""
        return cls(
            id=_uuid(d.get("Id")),
            company_id=_uuid(d.get("CompanyId")),
            url=d.get("Url"),
            description=d.get("Description"),
            disabled=d.get("Disabled", False),
            event_types=d.get("EventTypes", []),
            secret=d.get("Secret"),
        )
