"""Tests for Unit 5: Model Configuration."""

import os

import pytest
from pydantic import ValidationError

from units.unit_05_model_config.solution import ApiConfig, AppSettings, FeatureFlags


class TestAppSettings:
    """Tests for the AppSettings model."""

    @pytest.fixture(autouse=True)
    def setup_env(self):
        """Set up required environment variables."""
        os.environ["APP_DATABASE_URL"] = "postgresql://localhost/testdb"
        yield
        # Clean up
        for key in list(os.environ.keys()):
            if key.startswith("APP_"):
                del os.environ[key]

    def test_loads_from_environment(self):
        """Test that settings load from environment variables."""
        os.environ["APP_DEBUG"] = "true"
        os.environ["APP_LOG_LEVEL"] = "DEBUG"

        settings = AppSettings()

        assert settings.debug is True
        assert settings.log_level == "DEBUG"

    def test_default_values(self):
        """Test that default values are used when not in env."""
        settings = AppSettings()

        assert settings.app_name == "MyApp"
        assert settings.version == "1.0.0"
        assert settings.debug is False
        assert settings.log_level == "INFO"
        assert settings.api_key is None
        assert settings.max_connections == 10

    def test_database_url_required(self):
        """Test that database_url is required."""
        del os.environ["APP_DATABASE_URL"]

        with pytest.raises(ValidationError):
            AppSettings()

    def test_max_connections_range(self):
        """Test max_connections must be 1-100."""
        os.environ["APP_MAX_CONNECTIONS"] = "150"

        with pytest.raises(ValidationError):
            AppSettings()

    def test_frozen_cannot_modify(self):
        """Test that settings cannot be modified."""
        settings = AppSettings()

        with pytest.raises(ValidationError):
            settings.debug = True  # type: ignore

    def test_get_database_info(self):
        """Test database URL parsing."""
        os.environ["APP_DATABASE_URL"] = "postgresql://localhost:5432/mydb"

        settings = AppSettings()
        info = settings.get_database_info()

        assert info["driver"] == "postgresql"
        assert info["host"] == "localhost"
        assert info["port"] == 5432
        assert info["database"] == "mydb"

    def test_invalid_log_level(self):
        """Test that invalid log level is rejected."""
        os.environ["APP_LOG_LEVEL"] = "INVALID"

        with pytest.raises(ValidationError):
            AppSettings()


class TestApiConfig:
    """Tests for the ApiConfig model."""

    def test_create_with_aliases(self):
        """Test creating with camelCase aliases."""
        config = ApiConfig(
            baseUrl="https://api.example.com",
            timeoutSeconds=30,
            retryCount=3,
        )

        assert config.base_url == "https://api.example.com"
        assert config.timeout_seconds == 30
        assert config.retry_count == 3

    def test_create_with_field_names(self):
        """Test creating with snake_case field names."""
        config = ApiConfig(
            base_url="https://api.example.com",
            timeout_seconds=30,
            retry_count=3,
        )

        assert config.base_url == "https://api.example.com"

    def test_default_use_https(self):
        """Test default value for use_https."""
        config = ApiConfig(
            base_url="https://api.example.com",
            timeout_seconds=30,
            retry_count=3,
        )

        assert config.use_https is True

    def test_dump_with_aliases(self):
        """Test model_dump with by_alias=True."""
        config = ApiConfig(
            base_url="https://api.example.com",
            timeout_seconds=30,
            retry_count=3,
        )

        data = config.model_dump(by_alias=True)

        assert "baseUrl" in data
        assert "timeoutSeconds" in data
        assert "retryCount" in data
        assert "useHttps" in data

    def test_forbids_extra_fields(self):
        """Test that extra fields are forbidden."""
        with pytest.raises(ValidationError) as exc_info:
            ApiConfig(
                base_url="https://api.example.com",
                timeout_seconds=30,
                retry_count=3,
                unknown_field="should fail",
            )

        assert "extra" in str(exc_info.value).lower()

    def test_timeout_range(self):
        """Test timeout_seconds must be 1-300."""
        with pytest.raises(ValidationError):
            ApiConfig(
                base_url="https://api.example.com",
                timeout_seconds=0,
                retry_count=3,
            )

        with pytest.raises(ValidationError):
            ApiConfig(
                base_url="https://api.example.com",
                timeout_seconds=301,
                retry_count=3,
            )

    def test_retry_count_range(self):
        """Test retry_count must be 0-10."""
        # 0 is valid
        config = ApiConfig(
            base_url="https://api.example.com",
            timeout_seconds=30,
            retry_count=0,
        )
        assert config.retry_count == 0

        # 11 is invalid
        with pytest.raises(ValidationError):
            ApiConfig(
                base_url="https://api.example.com",
                timeout_seconds=30,
                retry_count=11,
            )


class TestFeatureFlags:
    """Tests for the FeatureFlags model."""

    def test_default_values(self):
        """Test default values."""
        flags = FeatureFlags()

        assert flags.dark_mode is False
        assert flags.beta_features is False
        assert flags.max_items_per_page == 25

    def test_frozen_cannot_modify(self):
        """Test that flags cannot be modified."""
        flags = FeatureFlags(dark_mode=True)

        with pytest.raises(ValidationError):
            flags.dark_mode = False  # type: ignore

    def test_strict_rejects_string_bool(self):
        """Test strict mode rejects string for bool."""
        with pytest.raises(ValidationError) as exc_info:
            FeatureFlags(dark_mode="true")  # type: ignore

        assert "bool_type" in str(exc_info.value)

    def test_strict_rejects_string_int(self):
        """Test strict mode rejects string for int."""
        with pytest.raises(ValidationError):
            FeatureFlags(max_items_per_page="50")  # type: ignore

    def test_allows_extra_fields(self):
        """Test that extra fields are allowed."""
        flags = FeatureFlags(
            dark_mode=True,
            custom_flag=True,
            another_flag="value",
        )

        data = flags.model_dump()
        assert "custom_flag" in data
        assert "another_flag" in data
        assert data["custom_flag"] is True

    def test_max_items_range(self):
        """Test max_items_per_page must be 10-100."""
        with pytest.raises(ValidationError):
            FeatureFlags(max_items_per_page=5)

        with pytest.raises(ValidationError):
            FeatureFlags(max_items_per_page=150)

        # Valid values
        flags = FeatureFlags(max_items_per_page=10)
        assert flags.max_items_per_page == 10

        flags = FeatureFlags(max_items_per_page=100)
        assert flags.max_items_per_page == 100
