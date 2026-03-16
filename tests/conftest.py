"""Shared test fixtures and configuration."""

from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_service() -> MagicMock:
    """Example mock fixture for external services.

    This demonstrates how to create mock fixtures for testing.
    Replace this with actual mocks for your external dependencies.

    Returns:
        A MagicMock instance configured for testing.
    """
    mock = MagicMock()
    mock.get_data.return_value = {"key": "value"}
    mock.is_available.return_value = True
    return mock
