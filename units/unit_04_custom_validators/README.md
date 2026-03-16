# Unit 4: Custom Validators

## Learning Objectives

By the end of this unit, you will be able to:

- Create field validators with `@field_validator`
- Create model validators with `@model_validator`
- Use computed fields with `@computed_field`
- Understand validation modes (before, after, wrap)

## Key Concepts

### Field Validators

Use `@field_validator` to add custom validation logic to individual fields:

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v.lower()  # Normalize to lowercase
```

### Validation Modes

- **`mode="after"`** (default): Runs after Pydantic's built-in validation
- **`mode="before"`**: Runs before type coercion
- **`mode="wrap"`**: Wraps around the entire validation process

```python
@field_validator("age", mode="before")
@classmethod
def parse_age(cls, v):
    if isinstance(v, str):
        return int(v.replace(" years", ""))
    return v
```

### Model Validators

Use `@model_validator` to validate relationships between multiple fields:

```python
from pydantic import BaseModel, model_validator

class DateRange(BaseModel):
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def validate_dates(self) -> "DateRange":
        if self.end_date < self.start_date:
            raise ValueError("end_date must be after start_date")
        return self
```

### Computed Fields

Use `@computed_field` for fields that are calculated from other fields:

```python
from pydantic import BaseModel, computed_field

class Rectangle(BaseModel):
    width: float
    height: float

    @computed_field
    @property
    def area(self) -> float:
        return self.width * self.height
```

### Validating Multiple Fields

A single validator can apply to multiple fields:

```python
@field_validator("first_name", "last_name")
@classmethod
def capitalize_name(cls, v: str) -> str:
    return v.title()
```

### Important Notes

1. Field validators must be class methods (`@classmethod`)
2. Model validators can access `self` when `mode="after"`
3. Always return the validated/transformed value
4. Raise `ValueError` for validation failures

## Files in This Unit

- `example.py` - Order model with computed totals
- `exercise.md` - Exercise description
- `exercise.py` - Starter code for PasswordReset model
- `solution.py` - Complete solution
- `test_solution.py` - Tests to verify your solution

## Next Steps

After completing this unit, move on to Unit 5 to learn about model configuration.
