"""Tests for Unit 7: FastAPI + Pydantic Integration."""

import pytest
from fastapi.testclient import TestClient

from units.unit_07_fastapi_integration.solution import app, books_db


@pytest.fixture(autouse=True)
def reset_database():
    """Reset the database before each test."""
    global next_id
    books_db.clear()
    # Reset next_id by reimporting - need a different approach
    from units.unit_07_fastapi_integration import solution

    solution.next_id = 1
    yield
    books_db.clear()


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def sample_book():
    """Sample book data for testing."""
    return {
        "title": "Python Crash Course",
        "author": "Eric Matthes",
        "isbn": "9781593279288",
        "published_year": 2019,
        "genre": "Programming",
        "pages": 544,
        "description": "A hands-on introduction to programming",
    }


class TestRootEndpoint:
    """Tests for the root endpoint."""

    def test_root_returns_welcome_message(self, client):
        """Test that root returns welcome message."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == "Welcome to the Book Library API"


class TestCreateBook:
    """Tests for POST /books endpoint."""

    def test_create_book_success(self, client, sample_book):
        """Test creating a book successfully."""
        response = client.post("/books", json=sample_book)

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["title"] == sample_book["title"]
        assert data["author"] == sample_book["author"]
        assert data["available"] is True
        assert "created_at" in data

    def test_create_book_validation_error(self, client):
        """Test that invalid data returns 422."""
        invalid_book = {
            "title": "",  # Too short
            "author": "Test",
            "isbn": "123",  # Not 13 digits
            "published_year": 2019,
            "genre": "Test",
            "pages": 0,  # Must be >= 1
        }

        response = client.post("/books", json=invalid_book)
        assert response.status_code == 422

    def test_create_book_missing_field(self, client):
        """Test that missing required field returns 422."""
        incomplete_book = {
            "title": "Test Book",
            # Missing author, isbn, etc.
        }

        response = client.post("/books", json=incomplete_book)
        assert response.status_code == 422


class TestGetBook:
    """Tests for GET /books/{book_id} endpoint."""

    def test_get_book_success(self, client, sample_book):
        """Test getting a book by ID."""
        # Create a book first
        create_response = client.post("/books", json=sample_book)
        book_id = create_response.json()["id"]

        # Get the book
        response = client.get(f"/books/{book_id}")

        assert response.status_code == 200
        assert response.json()["id"] == book_id
        assert response.json()["title"] == sample_book["title"]

    def test_get_book_not_found(self, client):
        """Test getting non-existent book returns 404."""
        response = client.get("/books/999")
        assert response.status_code == 404

    def test_get_book_invalid_id(self, client):
        """Test that invalid book ID returns 422."""
        response = client.get("/books/0")  # Must be >= 1
        assert response.status_code == 422


class TestListBooks:
    """Tests for GET /books endpoint."""

    def test_list_books_empty(self, client):
        """Test listing books when database is empty."""
        response = client.get("/books")

        assert response.status_code == 200
        data = response.json()
        assert data["books"] == []
        assert data["total"] == 0

    def test_list_books_with_books(self, client, sample_book):
        """Test listing books with data."""
        # Create some books
        client.post("/books", json=sample_book)
        client.post("/books", json={**sample_book, "title": "Another Book"})

        response = client.get("/books")

        assert response.status_code == 200
        data = response.json()
        assert len(data["books"]) == 2
        assert data["total"] == 2

    def test_list_books_filter_by_genre(self, client, sample_book):
        """Test filtering books by genre."""
        client.post("/books", json=sample_book)
        client.post("/books", json={**sample_book, "genre": "Fiction"})

        response = client.get("/books?genre=Programming")

        assert response.status_code == 200
        data = response.json()
        assert len(data["books"]) == 1
        assert data["books"][0]["genre"] == "Programming"

    def test_list_books_filter_by_availability(self, client, sample_book):
        """Test filtering by availability."""
        client.post("/books", json=sample_book)
        create_resp = client.post("/books", json={**sample_book, "title": "Book 2"})
        book_id = create_resp.json()["id"]
        client.post(f"/books/{book_id}/borrow")

        # Only available
        response = client.get("/books?available=true")
        assert len(response.json()["books"]) == 1

        # Only borrowed
        response = client.get("/books?available=false")
        assert len(response.json()["books"]) == 1

    def test_list_books_pagination(self, client, sample_book):
        """Test pagination."""
        # Create 5 books
        for i in range(5):
            client.post("/books", json={**sample_book, "title": f"Book {i}"})

        # Get page 1 with size 2
        response = client.get("/books?page=1&page_size=2")
        data = response.json()

        assert len(data["books"]) == 2
        assert data["total"] == 5
        assert data["page"] == 1
        assert data["page_size"] == 2


class TestUpdateBook:
    """Tests for PATCH /books/{book_id} endpoint."""

    def test_update_book_success(self, client, sample_book):
        """Test updating a book."""
        create_response = client.post("/books", json=sample_book)
        book_id = create_response.json()["id"]

        response = client.patch(
            f"/books/{book_id}",
            json={"title": "Updated Title"},
        )

        assert response.status_code == 200
        assert response.json()["title"] == "Updated Title"
        assert response.json()["author"] == sample_book["author"]  # Unchanged

    def test_update_book_not_found(self, client):
        """Test updating non-existent book returns 404."""
        response = client.patch("/books/999", json={"title": "New Title"})
        assert response.status_code == 404


class TestDeleteBook:
    """Tests for DELETE /books/{book_id} endpoint."""

    def test_delete_book_success(self, client, sample_book):
        """Test deleting a book."""
        create_response = client.post("/books", json=sample_book)
        book_id = create_response.json()["id"]

        response = client.delete(f"/books/{book_id}")

        assert response.status_code == 200
        assert "deleted" in response.json()["message"].lower()

        # Verify book is gone
        get_response = client.get(f"/books/{book_id}")
        assert get_response.status_code == 404

    def test_delete_book_not_found(self, client):
        """Test deleting non-existent book returns 404."""
        response = client.delete("/books/999")
        assert response.status_code == 404


class TestBorrowReturn:
    """Tests for borrow/return endpoints."""

    def test_borrow_book_success(self, client, sample_book):
        """Test borrowing a book."""
        create_response = client.post("/books", json=sample_book)
        book_id = create_response.json()["id"]

        response = client.post(f"/books/{book_id}/borrow")

        assert response.status_code == 200
        assert response.json()["available"] is False

    def test_borrow_already_borrowed(self, client, sample_book):
        """Test borrowing already borrowed book returns 400."""
        create_response = client.post("/books", json=sample_book)
        book_id = create_response.json()["id"]

        client.post(f"/books/{book_id}/borrow")
        response = client.post(f"/books/{book_id}/borrow")

        assert response.status_code == 400

    def test_return_book_success(self, client, sample_book):
        """Test returning a book."""
        create_response = client.post("/books", json=sample_book)
        book_id = create_response.json()["id"]

        client.post(f"/books/{book_id}/borrow")
        response = client.post(f"/books/{book_id}/return")

        assert response.status_code == 200
        assert response.json()["available"] is True

    def test_return_not_borrowed(self, client, sample_book):
        """Test returning non-borrowed book returns 400."""
        create_response = client.post("/books", json=sample_book)
        book_id = create_response.json()["id"]

        response = client.post(f"/books/{book_id}/return")

        assert response.status_code == 400


class TestSearchBooks:
    """Tests for GET /books/search endpoint."""

    def test_search_by_title(self, client, sample_book):
        """Test searching books by title."""
        client.post("/books", json=sample_book)
        client.post("/books", json={**sample_book, "title": "JavaScript Guide"})

        response = client.get("/books/search?q=python")

        assert response.status_code == 200
        results = response.json()
        assert len(results) == 1
        assert "Python" in results[0]["title"]

    def test_search_by_author(self, client, sample_book):
        """Test searching books by author."""
        client.post("/books", json=sample_book)

        response = client.get("/books/search?q=matthes")

        assert response.status_code == 200
        results = response.json()
        assert len(results) == 1

    def test_search_limit(self, client, sample_book):
        """Test search respects limit."""
        for i in range(5):
            client.post("/books", json={**sample_book, "title": f"Python Book {i}"})

        response = client.get("/books/search?q=python&limit=2")

        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_search_empty_query(self, client):
        """Test that empty search query returns 422."""
        response = client.get("/books/search?q=")
        assert response.status_code == 422
