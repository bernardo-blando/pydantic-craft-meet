# Unit 5: Model Configuration

## Learning Objectives

By the end of this unit, you will be able to:

- Configure models using `ConfigDict`
- Create frozen (immutable) models
- Use aliases for field names
- Handle extra fields
- Enable strict mode for validation
- Use `pydantic-settings` for configuration from environment variables

## Key Concepts

### ConfigDict

Use `model_config` with `ConfigDict` to configure model behavior:

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        str_strip_whitespace=True,
    )

    name: str
    email: str
```

### Common Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `frozen` | Make model instances immutable | `False` |
| `str_strip_whitespace` | Strip whitespace from strings | `False` |
| `str_to_lower` | Convert strings to lowercase | `False` |
| `strict` | Disable type coercion | `False` |
| `extra` | How to handle extra fields | `"ignore"` |
| `populate_by_name` | Allow using field name or alias | `False` |

### Frozen Models

Frozen models cannot be modified after creation:

```python
class ImmutableUser(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str

user = ImmutableUser(name="Alice")
user.name = "Bob"  # Raises ValidationError!
```

### Field Aliases

Map external field names to internal ones:

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    user_name: str = Field(alias="userName")  # JSON uses camelCase

# Can create with alias
user = User(userName="alice")
# Or with field name if populate_by_name=True
```

### Alias Generators

Automatically generate aliases for all fields:

```python
from pydantic import ConfigDict
from pydantic.alias_generators import to_camel

class User(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    user_name: str  # Alias becomes "userName"
    email_address: str  # Alias becomes "emailAddress"
```

### Extra Fields

Control what happens with unknown fields:

```python
class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")  # Error on extra fields
    name: str

StrictModel(name="Alice", unknown="value")  # Raises ValidationError!
```

Options: `"ignore"` (default), `"allow"`, `"forbid"`

### Pydantic Settings

Load configuration from environment variables:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
    )

    database_url: str
    debug: bool = False
```

## Files in This Unit

- `example.py` - API response with camelCase conversion
- `exercise.md` - Exercise description
- `exercise.py` - Starter code for config settings model
- `solution.py` - Complete solution
- `test_solution.py` - Tests to verify your solution

## Next Steps

After completing this unit, move on to Unit 6 to learn about serialization and parsing.
