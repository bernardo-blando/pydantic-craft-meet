# Unit 1: Basic Models and Types

## Learning Objectives

By the end of this unit, you will be able to:

- Create Pydantic models using `BaseModel`
- Understand automatic type coercion
- Use basic Python types with Pydantic
- Convert models to dictionaries using `model_dump()`

## Key Concepts

### What is Pydantic?

Pydantic is a data validation library that uses Python type hints to validate and parse data. It's widely used in modern Python applications, especially with FastAPI.

### BaseModel

All Pydantic models inherit from `BaseModel`. When you create a model, Pydantic automatically:

1. **Validates** the data types
2. **Coerces** compatible types (e.g., `"123"` to `123` for an `int` field)
3. **Raises errors** for invalid data

### Basic Types

Pydantic supports all standard Python types:

- `str` - Strings
- `int` - Integers
- `float` - Floating-point numbers
- `bool` - Booleans
- `list` - Lists (use `list[str]` for typed lists)
- `dict` - Dictionaries
- `datetime` - Date and time objects

### Type Coercion

Pydantic automatically converts compatible types:

```python
class User(BaseModel):
    age: int

user = User(age="25")  # String "25" is coerced to int 25
print(user.age)  # Output: 25
print(type(user.age))  # Output: <class 'int'>
```

### model_dump()

Convert a model instance to a dictionary:

```python
user = User(name="Alice", age=30)
data = user.model_dump()
# {'name': 'Alice', 'age': 30}
```

## Files in This Unit

- `example.py` - Working example with User profile model
- `exercise.md` - Exercise description
- `exercise.py` - Starter code for the exercise
- `solution.py` - Complete solution
- `test_solution.py` - Tests to verify your solution

## Next Steps

After completing this unit, move on to Unit 2 to learn about field validation and constraints.
