# Why Pydantic?

## The Problem: Python's Dynamic Typing

Python is dynamically typed. This means you can do this:

```python
def create_user(name, age, email):
    return {"name": name, "age": age, "email": email}

# All of these "work" - but are they correct?
create_user("Alice", 30, "alice@example.com")  # Valid
create_user("Bob", "thirty", "not-an-email")   # Invalid, but Python doesn't care
create_user(None, -5, 12345)                   # Completely wrong, but no error
```

**Python won't stop you.** The function accepts anything, and the bugs surface later—often in production.

---

## What Happens Without Pydantic?

### Manual Validation Hell

```python
def create_user(name, age, email):
    # You have to write ALL of this yourself
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    if not name.strip():
        raise ValueError("name cannot be empty")
    if len(name) > 100:
        raise ValueError("name too long")

    if not isinstance(age, int):
        raise TypeError("age must be an integer")
    if age < 0 or age > 150:
        raise ValueError("age must be between 0 and 150")

    if not isinstance(email, str):
        raise TypeError("email must be a string")
    if "@" not in email or "." not in email:
        raise ValueError("invalid email format")

    return {"name": name.strip(), "age": age, "email": email.lower()}
```

**Problems:**
- Verbose and repetitive
- Easy to forget edge cases
- Inconsistent across the codebase
- No IDE autocomplete or type hints
- Error messages vary by developer

### Silent Failures

```python
# API receives this JSON:
data = {"user_id": "abc", "amount": "50.5", "active": "yes"}

# Without validation, you might do:
user_id = data["user_id"]      # Expected int, got string
amount = data["amount"]        # Expected float, got string
active = data["active"]        # Expected bool, got string

# Later in your code...
total = amount * 2             # TypeError: can't multiply str by int
if active:                     # "yes" is truthy, but so is "no" and "false"
    process()
```

---

## What Pydantic Gives You

### 1. Declarative Validation

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=150)
    email: str
```

That's it. All the validation from before, in 5 lines.

### 2. Automatic Type Coercion

```python
# Pydantic intelligently converts types
user = User(name="Alice", age="30", email="alice@example.com")
print(user.age)        # 30 (int, not "30")
print(type(user.age))  # <class 'int'>
```

### 3. Clear Error Messages

```python
from pydantic import ValidationError

try:
    User(name="", age=-5, email="bad")
except ValidationError as e:
    print(e)
```

```
2 validation errors for User
name
  String should have at least 1 character [input_value='']
age
  Input should be greater than or equal to 0 [input_value=-5]
```

### 4. IDE Support & Autocomplete

```python
user = User(name="Alice", age=30, email="alice@example.com")
user.  # IDE shows: name, age, email with types
```

### 5. Easy Serialization

```python
user.model_dump()       # → {"name": "Alice", "age": 30, "email": "alice@example.com"}
user.model_dump_json()  # → '{"name":"Alice","age":30,"email":"alice@example.com"}'
```

### 6. FastAPI Integration

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/users")
def create_user(user: User) -> User:  # Automatic request validation
    return user                       # Automatic response serialization
```

FastAPI uses Pydantic models for:
- Request body validation
- Response serialization
- OpenAPI documentation generation

---

## Real-World Impact

| Without Pydantic | With Pydantic |
|------------------|---------------|
| Runtime crashes from bad data | Validation errors at the boundary |
| Manual type checking everywhere | Declarative type definitions |
| Inconsistent error messages | Standardized, detailed errors |
| No IDE support for data shapes | Full autocomplete and type hints |
| Manual JSON parsing/serialization | Built-in `model_dump()` / `model_validate()` |
| Documentation gets out of sync | Models ARE the documentation |

---

## When to Use Pydantic

**Use Pydantic when:**
- Receiving external data (APIs, user input, config files)
- Defining domain models with validation rules
- Building FastAPI applications
- Working with structured AI outputs (like Gemini)
- Sharing data shapes across your codebase

**You might skip it for:**
- Simple internal data structures with no validation needs
- Performance-critical hot paths (though Pydantic v2 is fast)

---

## Course Overview

This course teaches Pydantic through 8 hands-on units:

| Unit | Topic | Key Concepts |
|------|-------|--------------|
| 1 | Basic Models | `BaseModel`, types, `model_dump()` |
| 2 | Field Validation | `Field()`, constraints, patterns |
| 3 | Nested Models | Composition, lists, unions |
| 4 | Custom Validators | `@field_validator`, `@model_validator`, `@computed_field` |
| 5 | Model Configuration | `ConfigDict`, aliases, strict mode |
| 6 | Serialization | `model_dump()`, `@field_serializer`, exclude/include |
| 7 | FastAPI Integration | Request/response validation, automatic docs |
| 8 | Gemini Structured Outputs | AI + Pydantic for reliable extraction |

Each unit includes:
- **README.md** - Concept explanation
- **example.py** - Working code to study
- **exercise.md** - Your task description
- **exercise.py** - Starter code with TODOs
- **solution.py** - Reference solution
- **test_solution.py** - Tests to verify your work

---

## Getting Started

```bash
# Install dependencies
make setup

# Run an example
make example1

# Run tests for a unit
make test1

# Run all tests
make test
```
