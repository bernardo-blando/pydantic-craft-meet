"""Domain models using Pydantic.

This module demonstrates how to define domain models with validation.
These models represent your business entities and should be independent
of the API layer.
"""

from pydantic import BaseModel, ConfigDict, Field


class Greeting(BaseModel):
    """Domain model for a greeting message."""

    model_config = ConfigDict(frozen=True)  # Immutable

    name: str = Field(
        default="World",
        min_length=0,
        max_length=100,
        description="Name to greet",
    )
    message: str = Field(
        ...,
        description="The greeting message",
    )

    @classmethod
    def create(cls, name: str = "World") -> "Greeting":
        """Factory method to create a greeting.

        Args:
            name: The name to greet.

        Returns:
            A Greeting instance with the formatted message.
        """
        return cls(name=name, message=f"Hello, {name}!")
