# Unit 3: Nested Models and Complex Types

## Learning Objectives

By the end of this unit, you will be able to:

- Create nested Pydantic models (models within models)
- Use lists of models
- Work with Union types for flexible fields
- Implement discriminated unions for type-safe variants

## Key Concepts

### Nested Models

Models can contain other models as fields:

```python
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    country: str

class Person(BaseModel):
    name: str
    address: Address  # Nested model
```

### Lists of Models

Use `list[Model]` for collections:

```python
class Team(BaseModel):
    name: str
    members: list[Person]  # List of Person models
```

### Union Types

Use `|` (or `Union`) for fields that can be multiple types:

```python
class Response(BaseModel):
    result: str | int | None  # Can be string, int, or None
```

### Discriminated Unions

When you have multiple model types, use a discriminator field to distinguish them:

```python
from typing import Literal
from pydantic import BaseModel

class Cat(BaseModel):
    pet_type: Literal["cat"]
    meows: int

class Dog(BaseModel):
    pet_type: Literal["dog"]
    barks: int

class Pet(BaseModel):
    pet: Cat | Dog  # Pydantic uses pet_type to determine which
```

### Complex Nested Structures

You can combine all these concepts:

```python
class Company(BaseModel):
    name: str
    departments: list[Department]  # List of nested models

class Department(BaseModel):
    name: str
    employees: list[Employee]  # Another level of nesting
    budget: float | None = None  # Optional union type
```

### Creating Nested Models from Dictionaries

Pydantic automatically converts nested dictionaries:

```python
data = {
    "name": "Alice",
    "address": {
        "street": "123 Main St",
        "city": "Boston",
        "country": "USA"
    }
}

person = Person(**data)  # address dict becomes Address model
```

## Files in This Unit

- `example.py` - Company/Department/Employee hierarchy
- `exercise.md` - Exercise description
- `exercise.py` - Starter code for blog system
- `solution.py` - Complete solution
- `test_solution.py` - Tests to verify your solution

## Next Steps

After completing this unit, move on to Unit 4 to learn about custom validators.
