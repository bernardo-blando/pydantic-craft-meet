# Unit 7: FastAPI + Pydantic Integration

## Learning Objectives

By the end of this unit, you will be able to:

- Create FastAPI endpoints with Pydantic request/response models
- Use path parameters, query parameters, and request bodies
- Implement automatic request validation
- Generate OpenAPI documentation automatically
- Handle validation errors gracefully

## Key Concepts

### FastAPI and Pydantic

FastAPI uses Pydantic models for:
- **Request body validation** - Automatic parsing and validation of JSON bodies
- **Response serialization** - Type-safe response models
- **Query/path parameter validation** - Using Pydantic types for parameters
- **Automatic documentation** - OpenAPI schema generation

### Request Body Models

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    name: str = Field(min_length=1)
    email: str
    age: int = Field(ge=0)

app = FastAPI()

@app.post("/users")
def create_user(user: UserCreate):
    # user is automatically validated
    return {"id": 1, **user.model_dump()}
```

### Response Models

```python
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int) -> UserResponse:
    return UserResponse(id=user_id, name="Alice", email="alice@example.com")
```

### Path Parameters

```python
from fastapi import Path

@app.get("/items/{item_id}")
def get_item(
    item_id: int = Path(ge=1, description="The item ID")
):
    return {"item_id": item_id}
```

### Query Parameters

```python
from fastapi import Query

@app.get("/search")
def search(
    q: str = Query(min_length=1, description="Search query"),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return {"query": q, "limit": limit, "offset": offset}
```

### Dependency Injection

```python
from fastapi import Depends

def get_db():
    return {"connection": "active"}

@app.get("/items")
def list_items(db = Depends(get_db)):
    return {"db_status": db["connection"]}
```

### Error Handling

FastAPI automatically returns 422 for validation errors:

```json
{
    "detail": [
        {
            "loc": ["body", "email"],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}
```

### Custom Error Responses

```python
from fastapi import HTTPException

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]
```

## Files in This Unit

- `example.py` - Task management CRUD API (runnable)
- `exercise.md` - Exercise description
- `exercise.py` - Starter code for Book Library API
- `solution.py` - Complete solution
- `test_solution.py` - Tests to verify your solution

## Running the Examples

```bash
# Run the example API
uvicorn units.unit_07_fastapi_integration.example:app --reload

# View docs at http://localhost:8000/docs
```

## Next Steps

After completing this unit, move on to Unit 8 to learn about Gemini structured outputs.
