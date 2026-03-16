"""Unit 5 Exercise: Create Configuration Models.

Your task is to create configuration models using ConfigDict
and pydantic-settings.

Instructions:
1. Complete all three model classes below
2. Configure each with the appropriate settings
3. Run tests with: pytest units/05_model_config/test_solution.py -v
"""

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """Application settings loaded from environment variables.

    TODO: Configure this class to:
    - Use env_prefix="APP_"
    - Load from .env file
    - Be frozen (immutable)

    TODO: Add these fields:
    - app_name: str (default "MyApp")
    - version: str (default "1.0.0")
    - debug: bool (default False)
    - log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] (default "INFO")
    - database_url: str (required, no default)
    - api_key: str | None (default None)
    - max_connections: int (default 10, range 1-100)
    """

    # TODO: Add model_config with SettingsConfigDict
    # model_config = SettingsConfigDict(
    #     env_prefix="APP_",
    #     env_file=".env",
    #     frozen=True,
    # )

    # TODO: Add fields
    # app_name: str = "MyApp"
    # version: str = "1.0.0"
    # debug: bool = False
    # log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    # database_url: str
    # api_key: str | None = None
    # max_connections: int = Field(default=10, ge=1, le=100)

    pass  # Remove this line once you add fields


class ApiConfig(BaseModel):
    """API configuration with camelCase aliases.

    TODO: Configure this class to:
    - Use alias_generator=to_camel
    - Allow populate_by_name=True
    - Forbid extra fields

    TODO: Add these fields:
    - base_url: str
    - timeout_seconds: int (1-300)
    - retry_count: int (0-10)
    - use_https: bool (default True)
    """

    # TODO: Add model_config with ConfigDict
    # model_config = ConfigDict(
    #     alias_generator=to_camel,
    #     populate_by_name=True,
    #     extra="forbid",
    # )

    # TODO: Add fields
    # base_url: str
    # timeout_seconds: int = Field(ge=1, le=300)
    # retry_count: int = Field(ge=0, le=10)
    # use_https: bool = True

    pass  # Remove this line once you add fields


class FeatureFlags(BaseModel):
    """Feature flags with strict validation.

    TODO: Configure this class to:
    - Be frozen (immutable)
    - Use strict mode (no type coercion)
    - Allow extra fields (for dynamic flags)

    TODO: Add these fields:
    - dark_mode: bool (default False)
    - beta_features: bool (default False)
    - max_items_per_page: int (default 25, range 10-100)
    """

    # TODO: Add model_config with ConfigDict
    # model_config = ConfigDict(
    #     frozen=True,
    #     strict=True,
    #     extra="allow",
    # )

    # TODO: Add fields
    # dark_mode: bool = False
    # beta_features: bool = False
    # max_items_per_page: int = Field(default=25, ge=10, le=100)

    pass  # Remove this line once you add fields


def main() -> None:
    """Test your implementation."""
    # TODO: Uncomment and test once you complete the models

    # import os
    # from pydantic import ValidationError
    #
    # # Part 1: AppSettings
    # print("=== Part 1: AppSettings ===")
    # os.environ["APP_DATABASE_URL"] = "postgresql://localhost/testdb"
    # os.environ["APP_DEBUG"] = "true"
    # os.environ["APP_LOG_LEVEL"] = "DEBUG"
    #
    # settings = AppSettings()
    # print(f"App: {settings.app_name} v{settings.version}")
    # print(f"Debug: {settings.debug}")
    # print(f"Log Level: {settings.log_level}")
    # print(f"Database: {settings.database_url}")
    # print()
    #
    # # Test frozen
    # try:
    #     settings.debug = False
    # except ValidationError as e:
    #     print(f"Cannot modify frozen: {e.errors()[0]['type']}")
    # print()
    #
    # # Part 2: ApiConfig
    # print("=== Part 2: ApiConfig ===")
    # # With aliases (camelCase)
    # config1 = ApiConfig(
    #     baseUrl="https://api.example.com",
    #     timeoutSeconds=30,
    #     retryCount=3,
    # )
    # print(f"Base URL: {config1.base_url}")
    #
    # # With field names
    # config2 = ApiConfig(
    #     base_url="https://api2.example.com",
    #     timeout_seconds=60,
    #     retry_count=5,
    # )
    # print(f"Base URL: {config2.base_url}")
    #
    # # Serialized with aliases
    # print(f"Serialized: {config1.model_dump(by_alias=True)}")
    #
    # # Test extra forbidden
    # try:
    #     ApiConfig(
    #         base_url="https://api.example.com",
    #         timeout_seconds=30,
    #         retry_count=3,
    #         unknown_field="oops",
    #     )
    # except ValidationError as e:
    #     print(f"Extra forbidden: {e.errors()[0]['type']}")
    # print()
    #
    # # Part 3: FeatureFlags
    # print("=== Part 3: FeatureFlags ===")
    # flags = FeatureFlags(
    #     dark_mode=True,
    #     beta_features=False,
    #     custom_flag=True,  # Extra field allowed
    # )
    # print(f"Dark mode: {flags.dark_mode}")
    # print(f"Full dump: {flags.model_dump()}")
    #
    # # Test strict mode
    # try:
    #     FeatureFlags(dark_mode="true")  # String not allowed!
    # except ValidationError as e:
    #     print(f"Strict mode error: {e.errors()[0]['type']}")

    print("Complete the models and uncomment the test code!")


if __name__ == "__main__":
    main()
