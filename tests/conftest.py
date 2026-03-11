"""Shared pytest fixtures for BokaMera tests."""

from __future__ import annotations

import pytest

from bokamera._client import BokaMeraHTTPClient

BASE_URL = "https://api.bokamera.se"


@pytest.fixture
def http():
    """Synchronous HTTP client with a test API key."""
    client = BokaMeraHTTPClient(api_key="test-key", base_url=BASE_URL)
    yield client
    client.close()


@pytest.fixture
def company_id():
    """A fixed company UUID string used across tests."""
    return "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"


@pytest.fixture
def http_with_company(company_id):
    """Synchronous HTTP client with a default company ID set."""
    from uuid import UUID

    client = BokaMeraHTTPClient(
        api_key="test-key",
        base_url=BASE_URL,
        company_id=UUID(company_id),
    )
    yield client
    client.close()
