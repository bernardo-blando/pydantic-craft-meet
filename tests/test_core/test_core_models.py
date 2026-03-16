"""Tests for Pydantic domain models."""

import pytest
from pydantic import ValidationError

from pydantic_craft_meet.models import Greeting


class TestGreeting:
    """Tests for the Greeting model."""

    def test_create_greeting(self) -> None:
        """Test creating a greeting with the factory method."""
        greeting = Greeting.create("Alice")
        assert greeting.name == "Alice"
        assert greeting.message == "Hello, Alice!"

    def test_create_greeting_default(self) -> None:
        """Test creating a greeting with default name."""
        greeting = Greeting.create()
        assert greeting.name == "World"
        assert greeting.message == "Hello, World!"

    def test_greeting_is_immutable(self) -> None:
        """Test that Greeting is frozen (immutable)."""
        greeting = Greeting.create("Test")
        with pytest.raises(ValidationError):
            greeting.name = "Changed"  # type: ignore[misc]
