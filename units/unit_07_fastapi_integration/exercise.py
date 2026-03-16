"""Unit 7 Exercise: Build a Book Library API.

Your task is to create a RESTful API for managing a book library
using FastAPI and Pydantic.

Instructions:
1. Complete all Pydantic models
2. Implement all API endpoints
3. Run tests with: pytest units/07_fastapi_integration/test_solution.py -v
4. Test manually: uvicorn units.unit_07_fastapi_integration.exercise:app --reload
"""

from fastapi import FastAPI
from pydantic import BaseModel

# === Pydantic Models ===


class BookCreate(BaseModel):
    """Model for creating a new book.

    TODO: Add the following fields:
    - title: str (min 1, max 200)
    - author: str (min 1, max 100)
    - isbn: str (pattern: 13 digits)
    - published_year: int (1000 to current year)
    - genre: str (min 1)
    - pages: int (>= 1)
    - description: str | None (max 2000, default None)
    """

    # TODO: Add fields
    # title: str = Field(min_length=1, max_length=200)
    # author: str = Field(min_length=1, max_length=100)
    # isbn: str = Field(pattern=r"^\d{13}$")
    # published_year: int = Field(ge=1000, le=datetime.now().year)
    # genre: str = Field(min_length=1)
    # pages: int = Field(ge=1)
    # description: str | None = Field(default=None, max_length=2000)

    pass  # Remove once you add fields


class BookUpdate(BaseModel):
    """Model for updating a book (all fields optional).

    TODO: Add the same fields as BookCreate but all optional (with None defaults)
    """

    # TODO: Add fields
    # title: str | None = Field(default=None, min_length=1, max_length=200)
    # ... etc

    pass  # Remove once you add fields


class BookResponse(BaseModel):
    """Model for book responses.

    TODO: Add these fields:
    - id: int
    - title: str
    - author: str
    - isbn: str
    - published_year: int
    - genre: str
    - pages: int
    - description: str | None
    - available: bool
    - created_at: datetime
    """

    # TODO: Add fields
    pass  # Remove once you add fields


class BookListResponse(BaseModel):
    """Model for paginated book list.

    TODO: Add these fields:
    - books: list[BookResponse]
    - total: int
    - page: int
    - page_size: int
    """

    # TODO: Add fields
    pass  # Remove once you add fields


class MessageResponse(BaseModel):
    """Simple message response."""

    message: str


# === In-Memory Database ===

books_db: dict[int, dict] = {}
next_id = 1


def get_book_or_404(book_id: int) -> dict:
    """Get a book by ID or raise 404.

    TODO: Implement this function
    - If book_id not in books_db, raise HTTPException(status_code=404, ...)
    - Otherwise return the book
    """
    pass


# === FastAPI Application ===

app = FastAPI(
    title="Book Library API",
    description="A book library API demonstrating FastAPI + Pydantic",
    version="1.0.0",
)


@app.get("/", response_model=MessageResponse)
def root() -> MessageResponse:
    """Welcome endpoint."""
    return MessageResponse(message="Welcome to the Book Library API")


# TODO: Implement POST /books endpoint
# @app.post("/books", response_model=BookResponse, status_code=201)
# def create_book(book: BookCreate) -> BookResponse:
#     """Create a new book."""
#     pass


# TODO: Implement GET /books endpoint with filtering and pagination
# @app.get("/books", response_model=BookListResponse)
# def list_books(
#     genre: str | None = Query(default=None),
#     author: str | None = Query(default=None),
#     available: bool | None = Query(default=None),
#     page: int = Query(default=1, ge=1),
#     page_size: int = Query(default=10, ge=1, le=100),
# ) -> BookListResponse:
#     """List books with optional filtering and pagination."""
#     pass


# TODO: Implement GET /books/{book_id} endpoint
# @app.get("/books/{book_id}", response_model=BookResponse)
# def get_book(
#     book_id: int = Path(ge=1, description="The book ID"),
# ) -> BookResponse:
#     """Get a specific book by ID."""
#     pass


# TODO: Implement PATCH /books/{book_id} endpoint
# @app.patch("/books/{book_id}", response_model=BookResponse)
# def update_book(
#     book_id: int = Path(ge=1),
#     updates: BookUpdate = ...,
# ) -> BookResponse:
#     """Update a book."""
#     pass


# TODO: Implement DELETE /books/{book_id} endpoint
# @app.delete("/books/{book_id}", response_model=MessageResponse)
# def delete_book(
#     book_id: int = Path(ge=1),
# ) -> MessageResponse:
#     """Delete a book."""
#     pass


# TODO: Implement POST /books/{book_id}/borrow endpoint
# @app.post("/books/{book_id}/borrow", response_model=BookResponse)
# def borrow_book(
#     book_id: int = Path(ge=1),
# ) -> BookResponse:
#     """Mark a book as borrowed."""
#     pass


# TODO: Implement POST /books/{book_id}/return endpoint
# @app.post("/books/{book_id}/return", response_model=BookResponse)
# def return_book(
#     book_id: int = Path(ge=1),
# ) -> BookResponse:
#     """Mark a book as returned."""
#     pass


# TODO: Implement GET /books/search endpoint
# @app.get("/books/search", response_model=list[BookResponse])
# def search_books(
#     q: str = Query(min_length=1, description="Search query"),
#     limit: int = Query(default=10, ge=1, le=50),
# ) -> list[BookResponse]:
#     """Search books by title or author."""
#     pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
