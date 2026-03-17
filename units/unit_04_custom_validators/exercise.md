# Exercise 4: Create a PasswordReset Model

## Objective

Create a password reset model with cross-field validation to ensure password requirements and matching confirmation.

## Requirements

Create a `PasswordReset` model with the following:

### Fields
| Field | Type | Description |
|-------|------|-------------|
| `user_id` | `str` | User identifier (min 1 char) |
| `email` | `str` | User's email address |
| `new_password` | `str` | The new password |
| `confirm_password` | `str` | Password confirmation |
| `reset_token` | `str` | Reset token (min 32 chars) |
| `requested_at` | `datetime` | When reset was requested |
| `expires_at` | `datetime` | When reset expires |

### Validators

1. **Email Validator** (`@field_validator`):
   - Normalize to lowercase
   - Strip whitespace
   - Must contain `@` and a `.` after the `@`

2. **Password Validator** (`@field_validator`):
   - Minimum 8 characters
   - Must contain at least one uppercase letter
   - Must contain at least one lowercase letter
   - Must contain at least one digit
   - Must contain at least one special character (`!@#$%^&*`)

3. **Token Validator** (`@field_validator`):
   - Convert to lowercase
   - Must be alphanumeric only

4. **Passwords Match** (`@model_validator`):
   - `new_password` must equal `confirm_password`

5. **Expiry Validation** (`@model_validator`):
   - `expires_at` must be after `requested_at`

### Computed Fields

1. **`is_expired`**: Returns `True` if current time is past `expires_at`
2. **`password_strength`**: Returns "weak", "medium", or "strong" based on length
   - weak: 8-11 characters
   - medium: 12-15 characters
   - strong: 16+ characters

## Steps

1. Open `exercise.py`
2. Complete the `PasswordReset` class
3. Implement all validators and computed fields
4. Run the tests to verify your solution

## Commands

```bash
# Run the example to see expected behavior
make example4

# Run the tests to verify your solution
make test4

# Run the solution (if you want to see the answer)
make solution4
```

## Hints

### Field validator for email:
```python
@field_validator("email")
@classmethod
def validate_email(cls, v: str) -> str:
    v = v.strip().lower()
    if "@" not in v or "." not in v.split("@")[-1]:
        raise ValueError("Invalid email format")
    return v
```

### Checking password requirements:
```python
import re

has_upper = bool(re.search(r"[A-Z]", password))
has_lower = bool(re.search(r"[a-z]", password))
has_digit = bool(re.search(r"\d", password))
has_special = bool(re.search(r"[!@#$%^&*]", password))
```

### Model validator for password match:
```python
@model_validator(mode="after")
def validate_passwords_match(self) -> "PasswordReset":
    if self.new_password != self.confirm_password:
        raise ValueError("Passwords do not match")
    return self
```

### Computed field:
```python
@computed_field
@property
def is_expired(self) -> bool:
    return datetime.now() > self.expires_at
```

## Expected Behavior

```python
from datetime import datetime, timedelta

# Valid password reset
reset = PasswordReset(
    user_id="user123",
    email="  USER@EXAMPLE.COM  ",
    new_password="SecurePass1!",
    confirm_password="SecurePass1!",
    reset_token="abc123def456ghi789jkl012mno345pq",
    requested_at=datetime.now(),
    expires_at=datetime.now() + timedelta(hours=1),
)

# Email is normalized
print(reset.email)  # "user@example.com"

# Computed fields
print(reset.is_expired)  # False
print(reset.password_strength)  # "medium"

# This should fail - passwords don't match
PasswordReset(
    user_id="user123",
    email="test@example.com",
    new_password="SecurePass1!",
    confirm_password="DifferentPass1!",  # Doesn't match!
    ...
)

# This should fail - password too weak
PasswordReset(
    user_id="user123",
    email="test@example.com",
    new_password="short",  # Too short, missing requirements
    confirm_password="short",
    ...
)
```

## Bonus Challenge

Add a method `time_until_expiry() -> timedelta | None` that returns:
- The time remaining until expiration
- `None` if already expired
