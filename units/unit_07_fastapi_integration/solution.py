"""Unit 7 Solution: Book Library API.

This is the complete solution for the Book Library API exercise.
Run with: uvicorn units.unit_07_fastapi_integration.solution:app --reload
"""

from datetime import datetime

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field

# === Pydantic Models ===


class BookCreate(BaseModel):
    """Model for creating a new book."""

    title: str = Field(min_length=1, max_length=200, description="Book title")
    author: str = Field(min_length=1, max_length=100, description="Author name")
    isbn: str = Field(pattern=r"^\d{13}$", description="ISBN-13 (13 digits)")
    published_year: int = Field(
        ge=1000, le=datetime.now().year, description="Publication year"
    )
    genre: str = Field(min_length=1, description="Book genre")
    pages: int = Field(ge=1, description="Number of pages")
    description: str | None = Field(
        default=None, max_length=2000, description="Book description"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Python Crash Course",
                "author": "Eric Matthes",
                "isbn": "9781593279288",
                "published_year": 2019,
                "genre": "Programming",
                "pages": 544,
                "description": "A hands-on, project-based introduction to programming",
            }
        }
    }


class BookUpdate(BaseModel):
    """Model for updating a book (all fields optional)."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    author: str | None = Field(default=None, min_length=1, max_length=100)
    isbn: str | None = Field(default=None, pattern=r"^\d{13}$")
    published_year: int | None = Field(default=None, ge=1000, le=datetime.now().year)
    genre: str | None = Field(default=None, min_length=1)
    pages: int | None = Field(default=None, ge=1)
    description: str | None = Field(default=None, max_length=2000)


class BookResponse(BaseModel):
    """Model for book responses."""

    id: int
    title: str
    author: str
    isbn: str
    published_year: int
    genre: str
    pages: int
    description: str | None
    available: bool
    created_at: datetime


class BookListResponse(BaseModel):
    """Model for paginated book list."""

    books: list[BookResponse]
    total: int
    page: int
    page_size: int


class MessageResponse(BaseModel):
    """Simple message response."""

    message: str


class LibraryStats(BaseModel):
    """Library statistics."""

    total_books: int
    available_books: int
    borrowed_books: int
    books_by_genre: dict[str, int]


# === In-Memory Database ===

books_db: dict[int, dict] = {}
next_id = 1


def get_book_or_404(book_id: int) -> dict:
    """Get a book by ID or raise 404."""
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail=f"Book {book_id} not found")
    return books_db[book_id]


# === FastAPI Application ===

app = FastAPI(
    title="Book Library API",
    description="A book library API demonstrating FastAPI + Pydantic integration",
    version="1.0.0",
)


@app.get("/", response_model=MessageResponse)
def root() -> MessageResponse:
    """Welcome endpoint."""
    return MessageResponse(message="Welcome to the Book Library API")


@app.post("/books", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate) -> BookResponse:
    """Create a new book.

    The request body is automatically validated against BookCreate model.
    """
    global next_id

    book_data = {
        "id": next_id,
        "title": book.title,
        "author": book.author,
        "isbn": book.isbn,
        "published_year": book.published_year,
        "genre": book.genre,
        "pages": book.pages,
        "description": book.description,
        "available": True,
        "created_at": datetime.now(),
    }

    books_db[next_id] = book_data
    next_id += 1

    return BookResponse(**book_data)


@app.get("/books/search", response_model=list[BookResponse])
def search_books(
    q: str = Query(min_length=1, description="Search query"),
    limit: int = Query(default=10, ge=1, le=50, description="Maximum results"),
) -> list[BookResponse]:
    """Search books by title or author.

    Note: This endpoint must be defined BEFORE /books/{book_id}
    to avoid route conflicts.
    """
    query_lower = q.lower()
    results = [
        book
        for book in books_db.values()
        if query_lower in book["title"].lower() or query_lower in book["author"].lower()
    ]
    return [BookResponse(**book) for book in results[:limit]]


@app.get("/books", response_model=BookListResponse)
def list_books(
    genre: str | None = Query(default=None, description="Filter by genre"),
    author: str | None = Query(default=None, description="Filter by author"),
    available: bool | None = Query(default=None, description="Filter by availability"),
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=10, ge=1, le=100, description="Items per page"),
) -> BookListResponse:
    """List books with optional filtering and pagination."""
    # Start with all books
    filtered = list(books_db.values())

    # Apply filters
    if genre is not None:
        filtered = [b for b in filtered if b["genre"].lower() == genre.lower()]

    if author is not None:
        filtered = [b for b in filtered if author.lower() in b["author"].lower()]

    if available is not None:
        filtered = [b for b in filtered if b["available"] == available]

    # Calculate pagination
    total = len(filtered)
    start = (page - 1) * page_size
    end = start + page_size
    paginated = filtered[start:end]

    return BookListResponse(
        books=[BookResponse(**b) for b in paginated],
        total=total,
        page=page,
        page_size=page_size,
    )


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(
    book_id: int = Path(ge=1, description="The book ID"),
) -> BookResponse:
    """Get a specific book by ID."""
    book = get_book_or_404(book_id)
    return BookResponse(**book)


@app.patch("/books/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int = Path(ge=1, description="The book ID"),
    updates: BookUpdate = ...,
) -> BookResponse:
    """Update a book.

    Only provided fields are updated (partial update).
    """
    book = get_book_or_404(book_id)

    # Apply updates (only non-None values)
    update_data = updates.model_dump(exclude_none=True)
    for key, value in update_data.items():
        book[key] = value

    return BookResponse(**book)


@app.delete("/books/{book_id}", response_model=MessageResponse)
def delete_book(
    book_id: int = Path(ge=1, description="The book ID"),
) -> MessageResponse:
    """Delete a book from the library."""
    get_book_or_404(book_id)  # Check existence
    del books_db[book_id]
    return MessageResponse(message=f"Book {book_id} deleted successfully")


@app.post("/books/{book_id}/borrow", response_model=BookResponse)
def borrow_book(
    book_id: int = Path(ge=1, description="The book ID"),
) -> BookResponse:
    """Mark a book as borrowed."""
    book = get_book_or_404(book_id)

    if not book["available"]:
        raise HTTPException(
            status_code=400,
            detail=f"Book {book_id} is not available for borrowing",
        )

    book["available"] = False
    return BookResponse(**book)


@app.post("/books/{book_id}/return", response_model=BookResponse)
def return_book(
    book_id: int = Path(ge=1, description="The book ID"),
) -> BookResponse:
    """Mark a book as returned."""
    book = get_book_or_404(book_id)

    if book["available"]:
        raise HTTPException(
            status_code=400,
            detail=f"Book {book_id} is not currently borrowed",
        )

    book["available"] = True
    return BookResponse(**book)


@app.get("/stats", response_model=LibraryStats)
def get_stats() -> LibraryStats:
    """Get library statistics."""
    books = list(books_db.values())

    available = sum(1 for b in books if b["available"])
    borrowed = sum(1 for b in books if not b["available"])

    # Count by genre
    by_genre: dict[str, int] = {}
    for book in books:
        genre = book["genre"]
        by_genre[genre] = by_genre.get(genre, 0) + 1

    return LibraryStats(
        total_books=len(books),
        available_books=available,
        borrowed_books=borrowed,
        books_by_genre=by_genre,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
