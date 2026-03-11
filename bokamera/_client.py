"""
Low-level synchronous and asynchronous HTTP clients for the BokaMera API.

This module provides :class:`BokaMeraHTTPClient` (synchronous) and
:class:`AsyncBokaMeraHTTPClient` (asynchronous) which handle authentication,
request serialisation, response parsing, and error mapping for all API calls.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID

import httpx

from .exceptions import (
    BokaMeraAuthError,
    BokaMeraForbiddenError,
    BokaMeraHTTPError,
    BokaMeraNotFoundError,
    BokaMeraRateLimitError,
    BokaMeraValidationError,
)

_BASE_URL = "https://api.bokamera.se"


def _clean(params: dict) -> dict:
    """Remove None values from a dict.

    Args:
        params: Arbitrary key/value mapping that may contain ``None`` values.

    Returns:
        A new dict with all keys whose value is ``None`` removed.
    """
    return {k: v for k, v in params.items() if v is not None}


class BokaMeraHTTPClient:
    """Low-level synchronous HTTP client wrapping httpx.

    Handles authentication via the ``x-api-key`` header, serialises query
    parameters and request bodies, and maps non-2xx responses to the
    appropriate :class:`~bokamera.exceptions.BokaMeraHTTPError` subclass.

    Args:
        api_key: BokaMera API key sent as the ``x-api-key`` header.
        company_id: Default company UUID prepended to every request that
            accepts a ``CompanyId`` parameter.
        base_url: Override for the API base URL.
        timeout: Request timeout in seconds.
    """

    def __init__(
        self,
        api_key: str,
        company_id: UUID | None = None,
        base_url: str = _BASE_URL,
        timeout: float = 30.0,
    ) -> None:
        self._api_key = api_key
        self._company_id = company_id
        self._base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            base_url=self._base_url,
            headers={"x-api-key": api_key, "Accept": "application/json"},
            timeout=timeout,
        )

    def _raise_for_status(self, response: httpx.Response) -> None:
        """Raise the appropriate exception for a non-2xx response.

        Args:
            response: The httpx response to inspect.

        Raises:
            BokaMeraValidationError: On HTTP 400.
            BokaMeraAuthError: On HTTP 401.
            BokaMeraForbiddenError: On HTTP 403.
            BokaMeraNotFoundError: On HTTP 404.
            BokaMeraRateLimitError: On HTTP 429.
            BokaMeraHTTPError: On any other non-2xx status.
        """
        if response.is_success:
            return
        try:
            body = response.json()
            message = body.get("ResponseStatus", {}).get("Message", response.text)
        except Exception:
            body = None
            message = response.text

        status = response.status_code
        exc_cls: type[BokaMeraHTTPError]
        match status:
            case 400:
                exc_cls = BokaMeraValidationError
            case 401:
                exc_cls = BokaMeraAuthError
            case 403:
                exc_cls = BokaMeraForbiddenError
            case 404:
                exc_cls = BokaMeraNotFoundError
            case 429:
                exc_cls = BokaMeraRateLimitError
            case _:
                exc_cls = BokaMeraHTTPError
        raise exc_cls(status, message, body)

    def get(self, path: str, params: dict | None = None) -> Any:
        """Perform a GET request and return the parsed JSON response.

        Args:
            path: API path relative to the base URL.
            params: Optional query parameters; ``None`` values are stripped.

        Returns:
            Parsed JSON response (usually a ``dict`` or ``list``).

        Raises:
            BokaMeraHTTPError: If the response status is not 2xx.
        """
        response = self._client.get(path, params=_clean(params or {}))
        self._raise_for_status(response)
        return response.json()

    def post(self, path: str, json: dict | None = None, params: dict | None = None) -> Any:
        """Perform a POST request and return the parsed JSON response.

        Args:
            path: API path relative to the base URL.
            json: Request body as a dict; ``None`` values are stripped.
            params: Optional query parameters; ``None`` values are stripped.

        Returns:
            Parsed JSON response, or an empty dict if the body is not JSON.

        Raises:
            BokaMeraHTTPError: If the response status is not 2xx.
        """
        response = self._client.post(path, json=_clean(json or {}), params=_clean(params or {}))
        self._raise_for_status(response)
        try:
            return response.json()
        except Exception:
            return {}

    def put(self, path: str, json: dict | None = None, params: dict | None = None) -> Any:
        """Perform a PUT request and return the parsed JSON response.

        Args:
            path: API path relative to the base URL.
            json: Request body as a dict; ``None`` values are stripped.
            params: Optional query parameters; ``None`` values are stripped.

        Returns:
            Parsed JSON response, or an empty dict if the body is not JSON.

        Raises:
            BokaMeraHTTPError: If the response status is not 2xx.
        """
        response = self._client.put(path, json=_clean(json or {}), params=_clean(params or {}))
        self._raise_for_status(response)
        try:
            return response.json()
        except Exception:
            return {}

    def delete(self, path: str, params: dict | None = None) -> Any:
        """Perform a DELETE request and return the parsed JSON response.

        Args:
            path: API path relative to the base URL.
            params: Optional query parameters; ``None`` values are stripped.

        Returns:
            Parsed JSON response, or an empty dict if the body is not JSON.

        Raises:
            BokaMeraHTTPError: If the response status is not 2xx.
        """
        response = self._client.delete(path, params=_clean(params or {}))
        self._raise_for_status(response)
        try:
            return response.json()
        except Exception:
            return {}

    def get_bytes(self, path: str, params: dict | None = None) -> bytes:
        """Perform a GET request and return the raw response bytes.

        Useful for downloading binary content such as PDF files.

        Args:
            path: API path relative to the base URL.
            params: Optional query parameters; ``None`` values are stripped.

        Returns:
            Raw response body as bytes.

        Raises:
            BokaMeraHTTPError: If the response status is not 2xx.
        """
        response = self._client.get(path, params=_clean(params or {}))
        self._raise_for_status(response)
        return response.content

    @property
    def default_company_id(self) -> str | None:
        """Return the default company ID as a string, or ``None`` if not set."""
        return str(self._company_id) if self._company_id else None

    def close(self) -> None:
        """Close the underlying httpx client and release resources."""
        self._client.close()

    def __enter__(self) -> BokaMeraHTTPClient:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


class AsyncBokaMeraHTTPClient:
    """Low-level asynchronous HTTP client wrapping httpx.

    Provides the same interface as :class:`BokaMeraHTTPClient` but uses
    ``httpx.AsyncClient`` and ``async``/``await`` for all I/O operations.

    Args:
        api_key: BokaMera API key sent as the ``x-api-key`` header.
        company_id: Default company UUID prepended to every request that
            accepts a ``CompanyId`` parameter.
        base_url: Override for the API base URL.
        timeout: Request timeout in seconds.
    """

    def __init__(
        self,
        api_key: str,
        company_id: UUID | None = None,
        base_url: str = _BASE_URL,
        timeout: float = 30.0,
    ) -> None:
        self._api_key = api_key
        self._company_id = company_id
        self._base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            headers={"x-api-key": api_key, "Accept": "application/json"},
            timeout=timeout,
        )

    def _raise_for_status(self, response: httpx.Response) -> None:
        """Raise the appropriate exception for a non-2xx response.

        Args:
            response: The httpx response to inspect.

        Raises:
            BokaMeraValidationError: On HTTP 400.
            BokaMeraAuthError: On HTTP 401.
            BokaMeraForbiddenError: On HTTP 403.
            BokaMeraNotFoundError: On HTTP 404.
            BokaMeraRateLimitError: On HTTP 429.
            BokaMeraHTTPError: On any other non-2xx status.
        """
        if response.is_success:
            return
        try:
            body = response.json()
            message = body.get("ResponseStatus", {}).get("Message", response.text)
        except Exception:
            body = None
            message = response.text

        status = response.status_code
        exc_cls: type[BokaMeraHTTPError]
        match status:
            case 400:
                exc_cls = BokaMeraValidationError
            case 401:
                exc_cls = BokaMeraAuthError
            case 403:
                exc_cls = BokaMeraForbiddenError
            case 404:
                exc_cls = BokaMeraNotFoundError
            case 429:
                exc_cls = BokaMeraRateLimitError
            case _:
                exc_cls = BokaMeraHTTPError
        raise exc_cls(status, message, body)

    async def get(self, path: str, params: dict | None = None) -> Any:
        """Perform an async GET request and return the parsed JSON response.

        Args:
            path: API path relative to the base URL.
            params: Optional query parameters; ``None`` values are stripped.

        Returns:
            Parsed JSON response (usually a ``dict`` or ``list``).

        Raises:
            BokaMeraHTTPError: If the response status is not 2xx.
        """
        response = await self._client.get(path, params=_clean(params or {}))
        self._raise_for_status(response)
        return response.json()

    async def post(self, path: str, json: dict | None = None, params: dict | None = None) -> Any:
        """Perform an async POST request and return the parsed JSON response.

        Args:
            path: API path relative to the base URL.
            json: Request body as a dict; ``None`` values are stripped.
            params: Optional query parameters; ``None`` values are stripped.

        Returns:
            Parsed JSON response, or an empty dict if the body is not JSON.

        Raises:
            BokaMeraHTTPError: If the response status is not 2xx.
        """
        response = await self._client.post(path, json=_clean(json or {}), params=_clean(params or {}))
        self._raise_for_status(response)
        try:
            return response.json()
        except Exception:
            return {}

    async def put(self, path: str, json: dict | None = None, params: dict | None = None) -> Any:
        """Perform an async PUT request and return the parsed JSON response.

        Args:
            path: API path relative to the base URL.
            json: Request body as a dict; ``None`` values are stripped.
            params: Optional query parameters; ``None`` values are stripped.

        Returns:
            Parsed JSON response, or an empty dict if the body is not JSON.

        Raises:
            BokaMeraHTTPError: If the response status is not 2xx.
        """
        response = await self._client.put(path, json=_clean(json or {}), params=_clean(params or {}))
        self._raise_for_status(response)
        try:
            return response.json()
        except Exception:
            return {}

    async def delete(self, path: str, params: dict | None = None) -> Any:
        """Perform an async DELETE request and return the parsed JSON response.

        Args:
            path: API path relative to the base URL.
            params: Optional query parameters; ``None`` values are stripped.

        Returns:
            Parsed JSON response, or an empty dict if the body is not JSON.

        Raises:
            BokaMeraHTTPError: If the response status is not 2xx.
        """
        response = await self._client.delete(path, params=_clean(params or {}))
        self._raise_for_status(response)
        try:
            return response.json()
        except Exception:
            return {}

    async def get_bytes(self, path: str, params: dict | None = None) -> bytes:
        """Perform an async GET request and return the raw response bytes.

        Args:
            path: API path relative to the base URL.
            params: Optional query parameters; ``None`` values are stripped.

        Returns:
            Raw response body as bytes.

        Raises:
            BokaMeraHTTPError: If the response status is not 2xx.
        """
        response = await self._client.get(path, params=_clean(params or {}))
        self._raise_for_status(response)
        return response.content

    @property
    def default_company_id(self) -> str | None:
        """Return the default company ID as a string, or ``None`` if not set."""
        return str(self._company_id) if self._company_id else None

    async def aclose(self) -> None:
        """Close the underlying async httpx client and release resources."""
        await self._client.aclose()

    async def __aenter__(self) -> AsyncBokaMeraHTTPClient:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.aclose()
