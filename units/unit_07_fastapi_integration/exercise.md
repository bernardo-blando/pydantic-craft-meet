# Exercise 7: Build a Book Library API

## Objective

Create a RESTful API for managing a book library with FastAPI and Pydantic.

## Requirements

### Models

#### BookCreate (Request Body for POST)
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `title` | `str` | Min 1, Max 200 | Book title |
| `author` | `str` | Min 1, Max 100 | Author name |
| `isbn` | `str` | Pattern: 13 digits | ISBN-13 |
| `published_year` | `int` | 1000-current year | Publication year |
| `genre` | `str` | Min 1 | Book genre |
| `pages` | `int` | >= 1 | Number of pages |
| `description` | `str \| None` | Max 2000, Default: None | Book description |

#### BookUpdate (Request Body for PATCH)
All fields optional (same as BookCreate but nullable)

#### BookResponse (Response Model)
Same fields as BookCreate plus:
| Field | Type | Description |
|-------|------|-------------|
| `id` | `int` | Unique book ID |
| `available` | `bool` | Is book available (default: True) |
| `created_at` | `datetime` | When book was added |

#### BookListResponse (Paginated Response)
| Field | Type | Description |
|-------|------|-------------|
| `books` | `list[BookResponse]` | List of books |
| `total` | `int` | Total count |
| `page` | `int` | Current page |
| `page_size` | `int` | Items per page |

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Welcome message |
| POST | `/books` | Create a new book |
| GET | `/books` | List books with filtering and pagination |
| GET | `/books/{book_id}` | Get a specific book |
| PATCH | `/books/{book_id}` | Update a book |
| DELETE | `/books/{book_id}` | Delete a book |
| POST | `/books/{book_id}/borrow` | Mark book as borrowed |
| POST | `/books/{book_id}/return` | Mark book as returned |
| GET | `/books/search` | Search books by title/author |

### Query Parameters for GET /books

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `genre` | `str \| None` | None | Filter by genre |
| `author` | `str \| None` | None | Filter by author |
| `available` | `bool \| None` | None | Filter by availability |
| `page` | `int` | 1 | Page number (>= 1) |
| `page_size` | `int` | 10 | Items per page (1-100) |

### Query Parameters for GET /books/search

| Parameter | Type | Description |
|-----------|------|-------------|
| `q` | `str` | Search query (min 1 char) |
| `limit` | `int` | Max results (1-50, default 10) |

## Steps

1. Open `exercise.py`
2. Complete all Pydantic models
3. Implement all API endpoints
4. Run the tests to verify your solution
5. Test manually by starting the API server

## Commands

```bash
# Start the FastAPI server (for manual testing)
make run-api

# Run the tests to verify your solution
make test7

# View OpenAPI docs (after starting the server)
open http://localhost:8000/docs
```

## Hints

### ISBN validation pattern:
```python
isbn: str = Field(pattern=r"^\d{13}$")
```

### Current year validation:
```python
from datetime import datetime

published_year: int = Field(ge=1000, le=datetime.now().year)
```

### Path parameter with validation:
```python
@app.get("/books/{book_id}")
def get_book(
    book_id: int = Path(ge=1, description="The book ID"),
):
    ...
```

### Query parameters:
```python
@app.get("/books")
def list_books(
    genre: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
):
    ...
```

### Simple search implementation:
```python
def search_books(query: str) -> list[dict]:
    query_lower = query.lower()
    return [
        book for book in books_db.values()
        if query_lower in book["title"].lower()
        or query_lower in book["author"].lower()
    ]
```

## Expected Behavior

```bash
# Create a book
curl -X POST http://localhost:8000/books \
  -H "Content-Type: application/json" \
  -d '{"title": "Python Crash Course", "author": "Eric Matthes", "isbn": "9781593279288", "published_year": 2019, "genre": "Programming", "pages": 544}'

# List books with filtering
curl "http://localhost:8000/books?genre=Programming&page=1"

# Search books
curl "http://localhost:8000/books/search?q=python&limit=5"

# Borrow a book
curl -X POST http://localhost:8000/books/1/borrow

# View OpenAPI docs
open http://localhost:8000/docs
```

## Bonus Challenge

Add these features:
1. `GET /stats` endpoint returning library statistics (total books, available/borrowed counts, books by genre)
2. Add `rating` field (optional, 1-5) and endpoint `POST /books/{book_id}/rate`
