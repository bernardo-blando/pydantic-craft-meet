"""FastAPI request/response schemas."""

from pydantic import BaseModel, ConfigDict, Field


class MessageResponse(BaseModel):
    """Standard message response."""

    model_config = ConfigDict(frozen=True)

    message: str = Field(..., description="Response message")


class HealthResponse(BaseModel):
    """Health check response."""

    model_config = ConfigDict(frozen=True)

    status: str = Field(..., description="Health status", examples=["healthy"])


class GreetingResponse(BaseModel):
    """Greeting endpoint response."""

    model_config = ConfigDict(frozen=True)

    message: str = Field(..., description="Greeting message")
    name: str = Field(..., description="Name that was greeted")
