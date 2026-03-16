"""Unit 3 Solution: Blog System.

This is the complete solution for the blog system exercise.
Compare your solution with this one after completing the exercise.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class Author(BaseModel):
    """Blog author model.

    Represents a user who can create posts and comments.
    """

    author_id: str = Field(min_length=1, description="Unique author identifier")
    username: str = Field(min_length=3, max_length=50, description="Display username")
    email: str = Field(
        pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$",
        description="Author's email address",
    )
    bio: str = Field(default="", description="Author biography")


class Comment(BaseModel):
    """Comment on a blog post.

    Comments are nested within posts and reference an Author.
    """

    comment_id: str = Field(min_length=1, description="Unique comment identifier")
    author: Author  # Nested model
    content: str = Field(min_length=1, max_length=1000, description="Comment text")
    created_at: datetime = Field(description="When comment was created")
    likes: int = Field(default=0, ge=0, description="Number of likes")


class Post(BaseModel):
    """Blog post with author and comments.

    Posts can contain multiple comments and have a publication status.
    """

    post_id: str = Field(min_length=1, description="Unique post identifier")
    title: str = Field(min_length=1, max_length=200, description="Post title")
    content: str = Field(min_length=1, description="Post content")
    author: Author  # Nested model
    published_at: datetime = Field(description="Publication datetime")
    tags: list[str] = Field(default=[], description="Post tags")
    comments: list[Comment] = Field(default=[], description="List of comments")
    status: Literal["draft", "published", "archived"] = Field(
        default="draft", description="Post status"
    )

    def get_top_comments(self, n: int = 3) -> list[Comment]:
        """Get the n most-liked comments.

        Args:
            n: Number of top comments to return.

        Returns:
            List of comments sorted by likes (descending).
        """
        sorted_comments = sorted(self.comments, key=lambda c: c.likes, reverse=True)
        return sorted_comments[:n]


class Blog(BaseModel):
    """Blog containing posts and authors.

    Top-level model that aggregates all blog content.
    """

    name: str = Field(min_length=1, max_length=100, description="Blog name")
    description: str = Field(default="", description="Blog description")
    authors: list[Author] = Field(default=[], description="Registered authors")
    posts: list[Post] = Field(default=[], description="All posts")

    def get_published_posts(self) -> list[Post]:
        """Return only published posts.

        Returns:
            List of posts with status "published".
        """
        return [post for post in self.posts if post.status == "published"]

    def total_comments(self) -> int:
        """Count all comments across all posts.

        Returns:
            Total number of comments.
        """
        return sum(len(post.comments) for post in self.posts)

    def get_posts_by_author(self, author_id: str) -> list[Post]:
        """Get all posts by a specific author.

        Args:
            author_id: The author's ID.

        Returns:
            List of posts by the author.
        """
        return [post for post in self.posts if post.author.author_id == author_id]


def main() -> None:
    """Demonstrate the blog system."""
    # Create authors
    print("=== Creating Authors ===")
    alice = Author(
        author_id="auth1",
        username="alice_writes",
        email="alice@blog.com",
        bio="Tech blogger and Python enthusiast",
    )
    bob = Author(
        author_id="auth2",
        username="bob_codes",
        email="bob@blog.com",
        bio="Backend developer",
    )
    print(f"Created authors: {alice.username}, {bob.username}")
    print()

    # Create comments
    print("=== Creating Comments ===")
    comment1 = Comment(
        comment_id="c1",
        author=bob,
        content="Great article! Very helpful for beginners.",
        created_at=datetime(2024, 1, 15, 14, 30),
        likes=10,
    )
    comment2 = Comment(
        comment_id="c2",
        author=Author(
            author_id="auth3",
            username="reader123",
            email="reader@example.com",
        ),
        content="Thanks for sharing!",
        created_at=datetime(2024, 1, 15, 15, 45),
        likes=3,
    )
    print(f"Created {2} comments")
    print()

    # Create posts
    print("=== Creating Posts ===")
    post1 = Post(
        post_id="post1",
        title="Introduction to Pydantic",
        content="Pydantic is a powerful data validation library...",
        author=alice,
        published_at=datetime(2024, 1, 15, 10, 0),
        tags=["python", "pydantic", "tutorial"],
        comments=[comment1, comment2],
        status="published",
    )

    post2 = Post(
        post_id="post2",
        title="Advanced Pydantic Features",
        content="In this post, we'll explore advanced features...",
        author=alice,
        published_at=datetime(2024, 1, 20, 12, 0),
        tags=["python", "pydantic", "advanced"],
        status="draft",
    )
    print(f"Created posts: {post1.title}, {post2.title}")
    print()

    # Create blog
    print("=== Creating Blog ===")
    blog = Blog(
        name="Python Tips & Tricks",
        description="A blog about Python programming",
        authors=[alice, bob],
        posts=[post1, post2],
    )
    print(f"Blog: {blog.name}")
    print(f"Total authors: {len(blog.authors)}")
    print(f"Total posts: {len(blog.posts)}")
    print(f"Published posts: {len(blog.get_published_posts())}")
    print(f"Total comments: {blog.total_comments()}")
    print()

    # Create from nested dictionaries
    print("=== Creating from Nested Dictionaries ===")
    blog_data = {
        "name": "Tech Blog",
        "description": "Latest in technology",
        "authors": [
            {"author_id": "a1", "username": "techwriter", "email": "tech@blog.com"}
        ],
        "posts": [
            {
                "post_id": "p1",
                "title": "My First Post",
                "content": "Hello, world!",
                "author": {
                    "author_id": "a1",
                    "username": "techwriter",
                    "email": "tech@blog.com",
                },
                "published_at": "2024-01-15T10:30:00",
                "status": "published",
                "comments": [
                    {
                        "comment_id": "c1",
                        "author": {
                            "author_id": "a2",
                            "username": "commenter",
                            "email": "comment@example.com",
                        },
                        "content": "Nice post!",
                        "created_at": "2024-01-15T11:00:00",
                        "likes": 5,
                    }
                ],
            }
        ],
    }

    tech_blog = Blog(**blog_data)
    print(f"Blog name: {tech_blog.name}")
    print(f"First post author: {tech_blog.posts[0].author.username}")
    print(f"First comment author: {tech_blog.posts[0].comments[0].author.username}")
    print()

    # Get top comments
    print("=== Top Comments ===")
    top = post1.get_top_comments(2)
    for c in top:
        print(f"  {c.author.username}: {c.likes} likes")

    # Serialize to dict
    print()
    print("=== Serialization ===")
    data = post1.model_dump()
    print(f"Post dict keys: {list(data.keys())}")
    print(f"Author is dict: {isinstance(data['author'], dict)}")
    print(f"Comments is list: {isinstance(data['comments'], list)}")


if __name__ == "__main__":
    main()
