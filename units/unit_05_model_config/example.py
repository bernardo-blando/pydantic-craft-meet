"""Unit 5 Example: Model Configuration.

This example demonstrates API response models with camelCase
conversion and various ConfigDict options.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, ValidationError
from pydantic.alias_generators import to_camel


class ApiResponse(BaseModel):
    """API response model with camelCase aliases.

    This model automatically converts snake_case field names
    to camelCase for JSON serialization (common in APIs).
    """

    model_config = ConfigDict(
        # Generate camelCase aliases automatically
        alias_generator=to_camel,
        # Allow creation using either field name or alias
        populate_by_name=True,
        # Strip whitespace from strings
        str_strip_whitespace=True,
    )

    status_code: int = Field(ge=100, le=599)
    response_message: str
    created_at: datetime
    request_id: str | None = None


class ImmutableConfig(BaseModel):
    """Configuration that cannot be modified after creation.

    Useful for ensuring configuration values don't change
    during runtime.
    """

    model_config = ConfigDict(frozen=True)

    app_name: str
    version: str
    debug_mode: bool = False


class StrictModel(BaseModel):
    """Model with strict validation (no type coercion)."""

    model_config = ConfigDict(strict=True)

    count: int
    name: str
    active: bool


class ForbidExtraModel(BaseModel):
    """Model that rejects unknown fields."""

    model_config = ConfigDict(extra="forbid")

    id: int
    name: str


class AllowExtraModel(BaseModel):
    """Model that stores unknown fields."""

    model_config = ConfigDict(extra="allow")

    id: int
    name: str


class UserProfile(BaseModel):
    """User profile with explicit aliases."""

    model_config = ConfigDict(populate_by_name=True)

    # Explicit alias for API compatibility
    user_id: int = Field(alias="userId")
    full_name: str = Field(alias="fullName")
    email_address: str = Field(alias="emailAddress")
    is_active: bool = Field(default=True, alias="isActive")


def main() -> None:
    """Demonstrate model configuration options."""
    # Example 1: CamelCase aliases
    print("=== Example 1: CamelCase Aliases ===")

    # Create with Python-style names
    response1 = ApiResponse(
        status_code=200,
        response_message="Success",
        created_at=datetime.now(),
        request_id="req-123",
    )
    print(f"Created with snake_case: {response1.response_message}")

    # Create with JSON-style names (camelCase)
    response2 = ApiResponse(
        statusCode=201,
        responseMessage="Created",
        createdAt=datetime.now(),
    )
    print(f"Created with camelCase: {response2.response_message}")

    # Serialize with aliases (for JSON APIs)
    json_data = response1.model_dump(by_alias=True)
    print(f"Serialized keys: {list(json_data.keys())}")
    print()

    # Example 2: Frozen models
    print("=== Example 2: Frozen (Immutable) Models ===")
    config = ImmutableConfig(
        app_name="MyApp",
        version="1.0.0",
        debug_mode=True,
    )
    print(f"Config: {config.app_name} v{config.version}")

    try:
        config.version = "2.0.0"  # This will fail!
    except ValidationError as e:
        print(f"Cannot modify frozen model: {e.errors()[0]['type']}")
    print()

    # Example 3: Strict mode
    print("=== Example 3: Strict Mode ===")
    # Normal model coerces types
    normal = ApiResponse(
        status_code="200",  # String coerced to int
        response_message="OK",
        created_at="2024-01-15T10:00:00",
    )
    print(
        f"Normal coercion works: {normal.status_code} (type: {type(normal.status_code).__name__})"
    )

    # Strict model rejects type mismatches
    try:
        StrictModel(
            count="5",  # String not allowed!
            name="Test",
            active=True,
        )
    except ValidationError as e:
        print(f"Strict mode error: {e.errors()[0]['msg']}")
    print()

    # Example 4: Extra fields handling
    print("=== Example 4: Extra Fields ===")

    # forbid - raises error
    try:
        ForbidExtraModel(id=1, name="Test", unknown_field="oops")
    except ValidationError as e:
        print(f"forbid extra: {e.errors()[0]['msg']}")

    # allow - stores extra fields
    allowed = AllowExtraModel(id=1, name="Test", unknown_field="stored!")
    print(f"allow extra: {allowed.model_dump()}")
    print()

    # Example 5: Explicit aliases
    print("=== Example 5: Explicit Aliases ===")
    # Create with aliases (like from JSON API)
    user_from_api = UserProfile(
        userId=123,
        fullName="Alice Johnson",
        emailAddress="alice@example.com",
    )
    print(f"User: {user_from_api.full_name}")

    # Create with field names (Python code)
    user_from_code = UserProfile(
        user_id=456,
        full_name="Bob Smith",
        email_address="bob@example.com",
    )
    print(f"User: {user_from_code.full_name}")

    # Serialize for API (with aliases)
    api_output = user_from_api.model_dump(by_alias=True)
    print(f"API output keys: {list(api_output.keys())}")

    # Example 6: String preprocessing
    print()
    print("=== Example 6: String Preprocessing ===")
    response = ApiResponse(
        status_code=200,
        response_message="  Success with spaces  ",  # Will be stripped
        created_at=datetime.now(),
    )
    print(f"Stripped message: '{response.response_message}'")


if __name__ == "__main__":
    main()
