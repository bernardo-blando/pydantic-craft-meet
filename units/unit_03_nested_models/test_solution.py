"""Tests for Unit 3: Nested Models and Complex Types."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from units.unit_03_nested_models.solution import Author, Blog, Comment, Post


class TestAuthor:
    """Tests for the Author model."""

    def test_create_author(self):
        """Test creating a valid author."""
        author = Author(
            author_id="auth1",
            username="testuser",
            email="test@example.com",
        )

        assert author.author_id == "auth1"
        assert author.username == "testuser"
        assert author.bio == ""  # Default

    def test_author_with_bio(self):
        """Test creating author with bio."""
        author = Author(
            author_id="auth1",
            username="blogger",
            email="blogger@test.com",
            bio="Python enthusiast",
        )

        assert author.bio == "Python enthusiast"

    def test_invalid_email(self):
        """Test that invalid email is rejected."""
        with pytest.raises(ValidationError):
            Author(
                author_id="auth1",
                username="testuser",
                email="not-an-email",
            )

    def test_username_too_short(self):
        """Test that username must be at least 3 characters."""
        with pytest.raises(ValidationError):
            Author(
                author_id="auth1",
                username="ab",
                email="test@example.com",
            )


class TestComment:
    """Tests for the Comment model."""

    def test_create_comment(self):
        """Test creating a valid comment."""
        author = Author(
            author_id="auth1",
            username="commenter",
            email="commenter@test.com",
        )
        comment = Comment(
            comment_id="c1",
            author=author,
            content="Great post!",
            created_at=datetime(2024, 1, 15, 10, 30),
        )

        assert comment.comment_id == "c1"
        assert comment.author.username == "commenter"
        assert comment.likes == 0  # Default

    def test_comment_with_likes(self):
        """Test comment with likes."""
        author = Author(
            author_id="auth1",
            username="commenter",
            email="commenter@test.com",
        )
        comment = Comment(
            comment_id="c1",
            author=author,
            content="Amazing!",
            created_at=datetime.now(),
            likes=42,
        )

        assert comment.likes == 42

    def test_nested_author_from_dict(self):
        """Test creating comment with author as dict."""
        comment = Comment(
            comment_id="c1",
            author={
                "author_id": "auth1",
                "username": "dictuser",
                "email": "dict@test.com",
            },
            content="Test comment",
            created_at=datetime.now(),
        )

        assert isinstance(comment.author, Author)
        assert comment.author.username == "dictuser"

    def test_negative_likes_rejected(self):
        """Test that negative likes are rejected."""
        author = Author(
            author_id="auth1",
            username="commenter",
            email="commenter@test.com",
        )
        with pytest.raises(ValidationError):
            Comment(
                comment_id="c1",
                author=author,
                content="Bad comment",
                created_at=datetime.now(),
                likes=-5,
            )


class TestPost:
    """Tests for the Post model."""

    @pytest.fixture
    def author(self):
        """Create a test author."""
        return Author(
            author_id="auth1",
            username="testauthor",
            email="author@test.com",
        )

    def test_create_post(self, author):
        """Test creating a valid post."""
        post = Post(
            post_id="post1",
            title="Test Post",
            content="This is test content",
            author=author,
            published_at=datetime(2024, 1, 15),
        )

        assert post.post_id == "post1"
        assert post.title == "Test Post"
        assert post.status == "draft"  # Default
        assert post.tags == []  # Default
        assert post.comments == []  # Default

    def test_post_with_all_fields(self, author):
        """Test creating post with all fields."""
        comment = Comment(
            comment_id="c1",
            author=author,
            content="Nice!",
            created_at=datetime.now(),
        )

        post = Post(
            post_id="post1",
            title="Full Post",
            content="Content here",
            author=author,
            published_at=datetime.now(),
            tags=["python", "test"],
            comments=[comment],
            status="published",
        )

        assert post.status == "published"
        assert len(post.tags) == 2
        assert len(post.comments) == 1

    def test_invalid_status_rejected(self, author):
        """Test that invalid status is rejected."""
        with pytest.raises(ValidationError):
            Post(
                post_id="post1",
                title="Bad Post",
                content="Content",
                author=author,
                published_at=datetime.now(),
                status="invalid_status",
            )

    def test_get_top_comments(self, author):
        """Test get_top_comments method."""
        comments = [
            Comment(
                comment_id=f"c{i}",
                author=author,
                content=f"Comment {i}",
                created_at=datetime.now(),
                likes=likes,
            )
            for i, likes in enumerate([5, 10, 3, 8, 1])
        ]

        post = Post(
            post_id="post1",
            title="Post with comments",
            content="Content",
            author=author,
            published_at=datetime.now(),
            comments=comments,
        )

        top_2 = post.get_top_comments(2)
        assert len(top_2) == 2
        assert top_2[0].likes == 10
        assert top_2[1].likes == 8


class TestBlog:
    """Tests for the Blog model."""

    @pytest.fixture
    def author(self):
        """Create a test author."""
        return Author(
            author_id="auth1",
            username="blogger",
            email="blogger@test.com",
        )

    @pytest.fixture
    def posts(self, author):
        """Create test posts."""
        return [
            Post(
                post_id="p1",
                title="Published Post",
                content="Content 1",
                author=author,
                published_at=datetime.now(),
                status="published",
                comments=[
                    Comment(
                        comment_id="c1",
                        author=author,
                        content="Comment 1",
                        created_at=datetime.now(),
                    ),
                    Comment(
                        comment_id="c2",
                        author=author,
                        content="Comment 2",
                        created_at=datetime.now(),
                    ),
                ],
            ),
            Post(
                post_id="p2",
                title="Draft Post",
                content="Content 2",
                author=author,
                published_at=datetime.now(),
                status="draft",
                comments=[
                    Comment(
                        comment_id="c3",
                        author=author,
                        content="Comment 3",
                        created_at=datetime.now(),
                    ),
                ],
            ),
            Post(
                post_id="p3",
                title="Another Published",
                content="Content 3",
                author=author,
                published_at=datetime.now(),
                status="published",
            ),
        ]

    def test_create_blog(self, author, posts):
        """Test creating a valid blog."""
        blog = Blog(
            name="Test Blog",
            authors=[author],
            posts=posts,
        )

        assert blog.name == "Test Blog"
        assert len(blog.authors) == 1
        assert len(blog.posts) == 3
        assert blog.description == ""  # Default

    def test_get_published_posts(self, author, posts):
        """Test get_published_posts method."""
        blog = Blog(
            name="Test Blog",
            posts=posts,
        )

        published = blog.get_published_posts()
        assert len(published) == 2
        assert all(p.status == "published" for p in published)

    def test_total_comments(self, author, posts):
        """Test total_comments method."""
        blog = Blog(
            name="Test Blog",
            posts=posts,
        )

        # 2 comments on p1, 1 on p2, 0 on p3 = 3 total
        assert blog.total_comments() == 3

    def test_empty_blog(self):
        """Test blog with no posts."""
        blog = Blog(name="Empty Blog")

        assert blog.get_published_posts() == []
        assert blog.total_comments() == 0

    def test_create_from_nested_dict(self):
        """Test creating blog from nested dictionaries."""
        data = {
            "name": "Dict Blog",
            "description": "Created from dict",
            "authors": [
                {"author_id": "a1", "username": "author1", "email": "a1@test.com"}
            ],
            "posts": [
                {
                    "post_id": "p1",
                    "title": "Dict Post",
                    "content": "Content",
                    "author": {
                        "author_id": "a1",
                        "username": "author1",
                        "email": "a1@test.com",
                    },
                    "published_at": "2024-01-15T10:00:00",
                    "status": "published",
                    "comments": [
                        {
                            "comment_id": "c1",
                            "author": {
                                "author_id": "a2",
                                "username": "commenter",
                                "email": "c@test.com",
                            },
                            "content": "Nice!",
                            "created_at": "2024-01-15T11:00:00",
                        }
                    ],
                }
            ],
        }

        blog = Blog(**data)

        assert blog.name == "Dict Blog"
        assert isinstance(blog.posts[0], Post)
        assert isinstance(blog.posts[0].author, Author)
        assert isinstance(blog.posts[0].comments[0], Comment)
        assert isinstance(blog.posts[0].comments[0].author, Author)
