# Exercise 5: Create an AppSettings Model

## Objective

Create an application settings model that loads configuration from environment variables and JSON configuration files.

## Requirements

### Part 1: Create AppSettings Model (using pydantic-settings)

Create an `AppSettings` class that:

1. Inherits from `BaseSettings`
2. Loads values from environment variables with prefix `APP_`
3. Loads values from `.env` file
4. Is frozen (immutable)

Fields:
| Field | Type | Default | Env Var | Description |
|-------|------|---------|---------|-------------|
| `app_name` | `str` | "MyApp" | `APP_APP_NAME` | Application name |
| `version` | `str` | "1.0.0" | `APP_VERSION` | App version |
| `debug` | `bool` | `False` | `APP_DEBUG` | Debug mode |
| `log_level` | `Literal["DEBUG", "INFO", "WARNING", "ERROR"]` | "INFO" | `APP_LOG_LEVEL` | Logging level |
| `database_url` | `str` | Required | `APP_DATABASE_URL` | Database connection string |
| `api_key` | `str | None` | `None` | `APP_API_KEY` | Optional API key |
| `max_connections` | `int` | 10 | `APP_MAX_CONNECTIONS` | Max DB connections (1-100) |

### Part 2: Create ApiConfig Model

Create an `ApiConfig` class for API response configuration:

1. Uses alias generator for camelCase
2. Allows both field names and aliases
3. Forbids extra fields

Fields:
| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| `base_url` | `str` | `baseUrl` | API base URL |
| `timeout_seconds` | `int` | `timeoutSeconds` | Request timeout (1-300) |
| `retry_count` | `int` | `retryCount` | Number of retries (0-10) |
| `use_https` | `bool` | `useHttps` | Use HTTPS (default True) |

### Part 3: Create FeatureFlags Model

Create a `FeatureFlags` class for feature toggles:

1. Frozen (immutable)
2. Strict mode (no type coercion)
3. Extra fields allowed (for dynamic flags)

Fields:
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `dark_mode` | `bool` | `False` | Enable dark mode |
| `beta_features` | `bool` | `False` | Enable beta features |
| `max_items_per_page` | `int` | 25 | Pagination limit (10-100) |

## Steps

1. Open `exercise.py`
2. Complete all three model classes
3. Run the tests to verify your solution

## Commands

```bash
# Run the example to see expected behavior
make example5

# Run the tests to verify your solution
make test5

# Run the solution (if you want to see the answer)
make solution5
```

## Hints

### BaseSettings configuration:
```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        frozen=True,
    )
```

### Alias generator:
```python
from pydantic import ConfigDict
from pydantic.alias_generators import to_camel

class ApiConfig(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
    )
```

### Strict mode with frozen:
```python
model_config = ConfigDict(
    frozen=True,
    strict=True,
    extra="allow",
)
```

## Expected Behavior

```python
import os

# Part 1: AppSettings from environment
os.environ["APP_DATABASE_URL"] = "postgresql://localhost/mydb"
os.environ["APP_DEBUG"] = "true"

settings = AppSettings()
print(settings.database_url)  # "postgresql://localhost/mydb"
print(settings.debug)  # True

# Frozen - cannot modify
settings.debug = False  # Raises ValidationError!

# Part 2: ApiConfig with aliases
config = ApiConfig(
    baseUrl="https://api.example.com",  # Using alias
    timeoutSeconds=30,
    retryCount=3,
)
# Or with field names
config = ApiConfig(
    base_url="https://api.example.com",
    timeout_seconds=30,
    retry_count=3,
)

# Extra fields forbidden
ApiConfig(base_url="...", timeout_seconds=30, retry_count=3, unknown="x")  # Error!

# Part 3: FeatureFlags
flags = FeatureFlags(
    dark_mode=True,
    new_dynamic_flag=True,  # Allowed due to extra="allow"
)
print(flags.model_dump())  # Includes new_dynamic_flag

# Strict mode - no coercion
FeatureFlags(dark_mode="true")  # Error! Must be actual bool
```

## Bonus Challenge

Add a method to `AppSettings`:
- `get_database_info() -> dict` that parses `database_url` and returns a dictionary with `host`, `port`, `database`, and `driver` keys.
