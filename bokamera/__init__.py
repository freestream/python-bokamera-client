"""
bokamera — Typed Python client for the BokaMera API.

Quick start::

    from bokamera import BokaMeraClient

    with BokaMeraClient(api_key="your-key", company_id="your-company-uuid") as client:
        services = client.services.list(active=True, include_prices=True)
        for svc in services:
            print(svc.name, svc.prices)
"""

from .auth import OAuthToken, fetch_token, refresh_access_token
from .client import BokaMeraClient
from .exceptions import (
    BokaMeraAuthError,
    BokaMeraError,
    BokaMeraForbiddenError,
    BokaMeraHTTPError,
    BokaMeraNotFoundError,
    BokaMeraRateLimitError,
    BokaMeraValidationError,
)

__all__ = [
    "BokaMeraClient",
    "OAuthToken",
    "fetch_token",
    "refresh_access_token",
    "BokaMeraError",
    "BokaMeraHTTPError",
    "BokaMeraAuthError",
    "BokaMeraForbiddenError",
    "BokaMeraNotFoundError",
    "BokaMeraValidationError",
    "BokaMeraRateLimitError",
]

__version__ = "0.1.0"
