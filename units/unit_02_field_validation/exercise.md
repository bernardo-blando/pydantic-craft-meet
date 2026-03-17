# Exercise 2: Create a BankAccount Model

## Objective

Create a Pydantic model for a bank account with strict validation rules.

## Requirements

Create a `BankAccount` model with the following fields and constraints:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `account_number` | `str` | Pattern: 10 digits exactly | Account number |
| `account_holder` | `str` | Min 2, Max 100 chars | Account holder name |
| `account_type` | `str` | Min 1 char | Type (checking/savings) |
| `balance` | `float` | >= 0 | Current balance |
| `currency` | `str` | Exactly 3 uppercase letters | Currency code (USD, EUR, etc.) |
| `is_active` | `bool` | Default: True | Account status |
| `overdraft_limit` | `float | None` | >= 0 if provided, default: None | Optional overdraft limit |
| `email` | `str | None` | Valid email pattern, default: None | Contact email |

## Steps

1. Open `exercise.py`
2. Complete the `BankAccount` class by adding all fields with proper constraints
3. Add helpful descriptions to each field using the `description` parameter
4. Run the tests to verify your solution

## Commands

```bash
# Run the example to see expected behavior
make example2

# Run the tests to verify your solution
make test2

# Run the solution (if you want to see the answer)
make solution2
```

## Hints

### Pattern for 10 digits:
```python
pattern=r"^\d{10}$"
```

### Pattern for 3 uppercase letters:
```python
pattern=r"^[A-Z]{3}$"
```

### Pattern for email:
```python
pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$"
```

### Optional field with constraint:
```python
optional_field: float | None = Field(default=None, ge=0)
```

## Expected Behavior

```python
# Valid account
account = BankAccount(
    account_number="1234567890",
    account_holder="Alice Johnson",
    account_type="checking",
    balance=1500.00,
    currency="USD",
)

# These should raise ValidationError:
# - account_number="123" (not 10 digits)
# - balance=-100 (negative)
# - currency="usd" (not uppercase)
# - currency="USDD" (not 3 letters)
# - email="not-an-email" (invalid format)
```

## Bonus Challenge

After completing the basic requirements, try:

1. Add an `interest_rate` field that must be between 0 and 1 (0% to 100%)
2. Write a method `can_withdraw(amount: float) -> bool` that checks if a withdrawal is possible (considering balance and overdraft_limit)
