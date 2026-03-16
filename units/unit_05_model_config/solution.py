"""Unit 5 Solution: Configuration Models.

This is the complete solution for the configuration models exercise.
Compare your solution with this one after completing the exercise.
"""

from typing import Literal
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Application settings loaded from environment variables.

    This model demonstrates pydantic-settings for configuration
    management from environment variables and .env files.

    Environment variables use the APP_ prefix:
    - APP_DATABASE_URL
    - APP_DEBUG
    - etc.
    """

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        env_file_encoding="utf-8",
        frozen=True,
        extra="ignore",
    )

    app_name: str = Field(default="MyApp", description="Application name")
    version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=False, description="Enable debug mode")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="INFO", description="Logging level"
    )
    database_url: str = Field(description="Database connection URL")
    api_key: str | None = Field(default=None, description="Optional API key")
    max_connections: int = Field(
        default=10, ge=1, le=100, description="Maximum database connections"
    )

    def get_database_info(self) -> dict[str, str | int | None]:
        """Parse database URL into components.

        Returns:
            Dictionary with host, port, database, and driver.
        """
        parsed = urlparse(self.database_url)
        return {
            "driver": parsed.scheme,
            "host": parsed.hostname,
            "port": parsed.port,
            "database": parsed.path.lstrip("/") if parsed.path else None,
        }


class ApiConfig(BaseModel):
    """API configuration with camelCase aliases.

    This model demonstrates automatic alias generation for
    JSON API compatibility (snake_case Python to camelCase JSON).
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
    )

    base_url: str = Field(description="API base URL")
    timeout_seconds: int = Field(ge=1, le=300, description="Request timeout in seconds")
    retry_count: int = Field(ge=0, le=10, description="Number of retry attempts")
    use_https: bool = Field(default=True, description="Use HTTPS protocol")


class FeatureFlags(BaseModel):
    """Feature flags with strict validation.

    This model demonstrates:
    - Frozen (immutable) configuration
    - Strict mode (no type coercion)
    - Extra fields allowed for dynamic flags
    """

    model_config = ConfigDict(
        frozen=True,
        strict=True,
        extra="allow",
    )

    dark_mode: bool = Field(default=False, description="Enable dark mode UI")
    beta_features: bool = Field(default=False, description="Enable beta features")
    max_items_per_page: int = Field(
        default=25, ge=10, le=100, description="Items per page limit"
    )


def main() -> None:
    """Demonstrate configuration models."""
    import os

    from pydantic import ValidationError

    # Part 1: AppSettings from environment
    print("=== Part 1: AppSettings ===")
    os.environ["APP_DATABASE_URL"] = "postgresql://localhost:5432/myapp"
    os.environ["APP_DEBUG"] = "true"
    os.environ["APP_LOG_LEVEL"] = "DEBUG"
    os.environ["APP_MAX_CONNECTIONS"] = "50"

    settings = AppSettings()
    print(f"App: {settings.app_name} v{settings.version}")
    print(f"Debug: {settings.debug}")
    print(f"Log Level: {settings.log_level}")
    print(f"Database: {settings.database_url}")
    print(f"Max Connections: {settings.max_connections}")

    # Parse database URL
    db_info = settings.get_database_info()
    print(f"DB Info: {db_info}")

    # Test frozen
    try:
        settings.debug = False  # type: ignore
    except ValidationError as e:
        print(f"Cannot modify frozen model: {e.errors()[0]['type']}")
    print()

    # Part 2: ApiConfig with aliases
    print("=== Part 2: ApiConfig ===")

    # Create with camelCase aliases (like from JSON API)
    config_from_json = ApiConfig(
        baseUrl="https://api.example.com",
        timeoutSeconds=30,
        retryCount=3,
    )
    print(f"From JSON - Base URL: {config_from_json.base_url}")

    # Create with snake_case field names (Python code)
    config_from_code = ApiConfig(
        base_url="https://api2.example.com",
        timeout_seconds=60,
        retry_count=5,
        use_https=True,
    )
    print(f"From code - Base URL: {config_from_code.base_url}")

    # Serialize with aliases for JSON output
    json_output = config_from_code.model_dump(by_alias=True)
    print(f"JSON output: {json_output}")

    # Test extra forbidden
    try:
        ApiConfig(
            base_url="https://api.example.com",
            timeout_seconds=30,
            retry_count=3,
            unknown_field="should fail",  # type: ignore
        )
    except ValidationError as e:
        print(f"Extra forbidden: {e.errors()[0]['type']}")
    print()

    # Part 3: FeatureFlags
    print("=== Part 3: FeatureFlags ===")

    # Create with defined fields
    flags = FeatureFlags(
        dark_mode=True,
        beta_features=False,
        max_items_per_page=50,
    )
    print(f"Dark mode: {flags.dark_mode}")
    print(f"Beta features: {flags.beta_features}")
    print(f"Max items: {flags.max_items_per_page}")

    # Create with extra (dynamic) fields
    dynamic_flags = FeatureFlags(
        dark_mode=True,
        new_feature_x=True,  # Extra field - allowed
        experiment_abc=False,  # Another extra field
    )
    print(f"Dynamic flags dump: {dynamic_flags.model_dump()}")

    # Test frozen
    try:
        flags.dark_mode = False  # type: ignore
    except ValidationError as e:
        print(f"Cannot modify frozen: {e.errors()[0]['type']}")

    # Test strict mode - no type coercion
    try:
        FeatureFlags(dark_mode="true")  # String instead of bool
    except ValidationError as e:
        print(f"Strict mode error: {e.errors()[0]['type']}")

    # Clean up environment
    for key in [
        "APP_DATABASE_URL",
        "APP_DEBUG",
        "APP_LOG_LEVEL",
        "APP_MAX_CONNECTIONS",
    ]:
        os.environ.pop(key, None)


if __name__ == "__main__":
    main()
