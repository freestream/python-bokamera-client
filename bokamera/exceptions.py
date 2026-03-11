from __future__ import annotations


class BokaMeraError(Exception):
    """Base exception for all BokaMera errors."""


class BokaMeraHTTPError(BokaMeraError):
    """Raised when the API returns a non-2xx status code."""

    def __init__(self, status_code: int, message: str, response_body: dict | None = None) -> None:
        self.status_code = status_code
        self.message = message
        self.response_body = response_body
        super().__init__(f"HTTP {status_code}: {message}")


class BokaMeraAuthError(BokaMeraHTTPError):
    """Raised on 401 Unauthorized."""


class BokaMeraForbiddenError(BokaMeraHTTPError):
    """Raised on 403 Forbidden."""


class BokaMeraNotFoundError(BokaMeraHTTPError):
    """Raised on 404 Not Found."""


class BokaMeraValidationError(BokaMeraHTTPError):
    """Raised on 400 Bad Request / validation failure."""


class BokaMeraRateLimitError(BokaMeraHTTPError):
    """Raised on 429 Too Many Requests."""
