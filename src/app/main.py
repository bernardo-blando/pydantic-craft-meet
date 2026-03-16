"""FastAPI application entry point.

Run with: make run
Or: fastapi dev src/app/main.py
"""

from fastapi import FastAPI

from app.models import GreetingResponse, HealthResponse, MessageResponse
from pydantic_craft_meet import greet
from pydantic_craft_meet.config import config

app = FastAPI(
    title=config.app_name,
    description="A Python project generated from the boilerplate template",
    version=config.app_version,
    debug=config.debug,
)


@app.get("/", response_model=MessageResponse)
def root() -> MessageResponse:
    """Root endpoint returning a welcome message."""
    return MessageResponse(message="Welcome to the API")


@app.get("/greet/{name}", response_model=GreetingResponse)
def greet_endpoint(name: str) -> GreetingResponse:
    """Greet a user by name."""
    greeting = greet(name)
    return GreetingResponse(message=greeting.message, name=greeting.name)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(status="healthy")
