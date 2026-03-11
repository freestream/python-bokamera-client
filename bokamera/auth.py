"""OAuth2 token helpers for the BokaMera / Keycloak identity provider.

BokaMera uses Keycloak at ``https://identity.bookmore.com`` as its OAuth2 provider.
All API calls that require authentication must include a valid Bearer token obtained
from the token endpoint below.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass

import httpx

_TOKEN_URL = "https://identity.bookmore.com/realms/bookmore-admin/protocol/openid-connect/token"
_CLIENT_ID = "bm-external-api-users"


@dataclass
class OAuthToken:
    """An OAuth2 access/refresh token pair returned by Keycloak.

    Attributes:
        access_token: JWT bearer token to include in API requests.
        refresh_token: Token used to obtain a new access token without re-entering
            credentials.  May be ``None`` if the provider did not return one.
        expires_at: UTC datetime at which the access token expires.
    """

    access_token: str
    refresh_token: str | None
    expires_at: datetime.datetime

    @property
    def is_expired(self) -> bool:
        """Return ``True`` if the access token has expired."""
        return datetime.datetime.now(datetime.timezone.utc) >= self.expires_at


def fetch_token(
    username: str,
    password: str,
    *,
    token_url: str = _TOKEN_URL,
    client_id: str = _CLIENT_ID,
) -> OAuthToken:
    """Obtain a new OAuth2 token using the resource owner password grant.

    Args:
        username: BokaMera admin username (email address).
        password: BokaMera admin password.
        token_url: Override for the Keycloak token endpoint.
        client_id: Override for the OAuth2 client ID.

    Returns:
        An :class:`OAuthToken` containing the access token, refresh token,
        and expiry time.

    Raises:
        BokaMeraAuthError: If the credentials are rejected or the token endpoint
            returns a non-2xx response.
    """
    from .exceptions import BokaMeraAuthError

    response = httpx.post(
        token_url,
        data={
            "grant_type": "password",
            "client_id": client_id,
            "username": username,
            "password": password,
        },
        timeout=30.0,
    )
    if not response.is_success:
        try:
            body = response.json()
            message = body.get("error_description") or body.get("error") or response.text
        except Exception:
            message = response.text
        raise BokaMeraAuthError(response.status_code, message, None)

    data = response.json()
    expires_in = data.get("expires_in", 300)
    expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=int(expires_in))
    return OAuthToken(
        access_token=data["access_token"],
        refresh_token=data.get("refresh_token"),
        expires_at=expires_at,
    )


def refresh_access_token(
    token: OAuthToken,
    *,
    token_url: str = _TOKEN_URL,
    client_id: str = _CLIENT_ID,
) -> OAuthToken:
    """Obtain a new access token using an existing refresh token.

    Args:
        token: An :class:`OAuthToken` whose ``refresh_token`` will be used.
        token_url: Override for the Keycloak token endpoint.
        client_id: Override for the OAuth2 client ID.

    Returns:
        A new :class:`OAuthToken` with a refreshed access token.

    Raises:
        ValueError: If ``token.refresh_token`` is ``None``.
        BokaMeraAuthError: If the refresh token is rejected or has expired.
    """
    if not token.refresh_token:
        raise ValueError("Cannot refresh: no refresh_token available on this OAuthToken.")

    from .exceptions import BokaMeraAuthError

    response = httpx.post(
        token_url,
        data={
            "grant_type": "refresh_token",
            "client_id": client_id,
            "refresh_token": token.refresh_token,
        },
        timeout=30.0,
    )
    if not response.is_success:
        try:
            body = response.json()
            message = body.get("error_description") or body.get("error") or response.text
        except Exception:
            message = response.text
        raise BokaMeraAuthError(response.status_code, message, None)

    data = response.json()
    expires_in = data.get("expires_in", 300)
    expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=int(expires_in))
    return OAuthToken(
        access_token=data["access_token"],
        refresh_token=data.get("refresh_token", token.refresh_token),
        expires_at=expires_at,
    )
