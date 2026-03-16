# Unit 6: Serialization and Parsing

## Learning Objectives

By the end of this unit, you will be able to:

- Use `model_validate()` for parsing data into models
- Use `model_dump()` and `model_dump_json()` for serialization
- Create custom serializers with `@field_serializer`
- Use `exclude` and `include` parameters for selective serialization
- Handle complex types like datetime in serialization

## Key Concepts

### Parsing with model_validate()

Parse data from various sources into a Pydantic model:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

# From dictionary
user = User.model_validate({"name": "Alice", "age": 30})

# From JSON string
user = User.model_validate_json('{"name": "Alice", "age": 30}')
```

### Serialization with model_dump()

Convert models to dictionaries:

```python
user = User(name="Alice", age=30)

# Basic dump
data = user.model_dump()  # {'name': 'Alice', 'age': 30}

# With aliases
data = user.model_dump(by_alias=True)

# Exclude fields
data = user.model_dump(exclude={"age"})

# Include only specific fields
data = user.model_dump(include={"name"})

# Exclude None values
data = user.model_dump(exclude_none=True)

# Exclude default values
data = user.model_dump(exclude_defaults=True)
```

### JSON Serialization

```python
# To JSON string
json_str = user.model_dump_json()

# Pretty print
json_str = user.model_dump_json(indent=2)

# With aliases
json_str = user.model_dump_json(by_alias=True)
```

### Custom Field Serializers

Control how fields are serialized:

```python
from datetime import datetime
from pydantic import BaseModel, field_serializer

class Event(BaseModel):
    name: str
    timestamp: datetime

    @field_serializer("timestamp")
    def serialize_timestamp(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")
```

### Serializer Modes

- `mode="plain"` (default): Returns the serialized value
- `mode="wrap"`: Wraps around default serialization

```python
@field_serializer("price", mode="plain")
def serialize_price(self, value: float) -> str:
    return f"${value:.2f}"
```

### Nested Model Serialization

Nested models are serialized recursively:

```python
class Address(BaseModel):
    city: str

class Person(BaseModel):
    name: str
    address: Address

person = Person(name="Alice", address=Address(city="Boston"))
data = person.model_dump()
# {'name': 'Alice', 'address': {'city': 'Boston'}}
```

### Handling Datetime

```python
from datetime import datetime
from pydantic import BaseModel

class Event(BaseModel):
    timestamp: datetime

event = Event(timestamp=datetime.now())
# Default: ISO format string in JSON
json_str = event.model_dump_json()
# {"timestamp": "2024-01-15T10:30:00"}
```

## Files in This Unit

- `example.py` - Event logging with custom datetime handling
- `exercise.md` - Exercise description
- `exercise.py` - Starter code for AuditLog system
- `solution.py` - Complete solution
- `test_solution.py` - Tests to verify your solution

## Next Steps

After completing this unit, move on to Unit 7 to learn about FastAPI integration.
