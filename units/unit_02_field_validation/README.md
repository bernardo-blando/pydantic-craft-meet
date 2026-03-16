# Unit 2: Field Validation and Constraints

## Learning Objectives

By the end of this unit, you will be able to:

- Use `Field()` to add validation constraints
- Apply min/max constraints for numbers and strings
- Use regex patterns for string validation
- Handle `Optional` fields properly
- Catch and understand `ValidationError`

## Key Concepts

### The Field() Function

`Field()` provides additional validation and metadata for model fields:

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=150)  # ge = greater or equal, le = less or equal
```

### Numeric Constraints

| Constraint | Meaning | Example |
|------------|---------|---------|
| `gt` | Greater than | `Field(gt=0)` |
| `ge` | Greater or equal | `Field(ge=0)` |
| `lt` | Less than | `Field(lt=100)` |
| `le` | Less or equal | `Field(le=100)` |
| `multiple_of` | Must be multiple of | `Field(multiple_of=5)` |

### String Constraints

| Constraint | Meaning | Example |
|------------|---------|---------|
| `min_length` | Minimum length | `Field(min_length=1)` |
| `max_length` | Maximum length | `Field(max_length=100)` |
| `pattern` | Regex pattern | `Field(pattern=r"^[A-Z]{2}\d{4}$")` |

### Optional Fields

Use `| None` (or `Optional`) for fields that can be null:

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    email: str
    phone: str | None = None  # Optional, defaults to None
    nickname: str | None = Field(default=None, max_length=50)
```

### ValidationError

When validation fails, Pydantic raises `ValidationError`:

```python
from pydantic import BaseModel, Field, ValidationError

class User(BaseModel):
    age: int = Field(ge=0)

try:
    user = User(age=-5)
except ValidationError as e:
    print(e.errors())
    # Shows detailed error information
```

### Field Metadata

`Field()` also accepts metadata for documentation:

```python
class User(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
        description="The user's full name",
        examples=["Alice Smith", "Bob Jones"],
    )
```

## Files in This Unit

- `example.py` - Employee model with salary validation
- `exercise.md` - Exercise description
- `exercise.py` - Starter code for BankAccount model
- `solution.py` - Complete solution
- `test_solution.py` - Tests to verify your solution

## Next Steps

After completing this unit, move on to Unit 3 to learn about nested models and complex types.
