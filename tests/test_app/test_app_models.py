"""Tests for FastAPI schemas."""

from app.models import GreetingResponse, HealthResponse, MessageResponse


class TestResponseSchemas:
    """Tests for response schemas."""

    def test_message_response(self) -> None:
        """Test MessageResponse creation."""
        response = MessageResponse(message="Hello")
        assert response.message == "Hello"

    def test_health_response(self) -> None:
        """Test HealthResponse creation."""
        response = HealthResponse(status="healthy")
        assert response.status == "healthy"

    def test_greeting_response(self) -> None:
        """Test GreetingResponse creation."""
        response = GreetingResponse(message="Hello, Alice!", name="Alice")
        assert response.message == "Hello, Alice!"
        assert response.name == "Alice"
