"""Unit 3 Exercise: Build a Blog System.

Your task is to create a blog system with nested models
for Author, Post, Comment, and Blog.

Instructions:
1. Complete all four model classes below
2. Add the required methods to the Blog model
3. Run tests with: pytest units/03_nested_models/test_solution.py -v
"""

from pydantic import BaseModel


class Author(BaseModel):
    """Blog author model.

    TODO: Add the following fields:
    - author_id: str (min 1 char) - Unique author identifier
    - username: str (min 3, max 50 chars) - Display username
    - email: str (valid email pattern) - Author's email
    - bio: str (default "") - Author biography
    """

    # TODO: Add author_id field
    # Hint: author_id: str = Field(min_length=1)

    # TODO: Add username field
    # Hint: username: str = Field(min_length=3, max_length=50)

    # TODO: Add email field with pattern
    # Hint: email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")

    # TODO: Add bio field with default
    # Hint: bio: str = ""

    pass  # Remove this line once you add fields


class Comment(BaseModel):
    """Comment on a blog post.

    TODO: Add the following fields:
    - comment_id: str (min 1 char) - Unique comment identifier
    - author: Author - Nested Author model
    - content: str (min 1, max 1000 chars) - Comment text
    - created_at: datetime - When comment was created
    - likes: int (>= 0, default 0) - Number of likes
    """

    # TODO: Add comment_id field

    # TODO: Add author field (nested model)
    # Hint: author: Author

    # TODO: Add content field

    # TODO: Add created_at field
    # Hint: created_at: datetime

    # TODO: Add likes field with default
    # Hint: likes: int = Field(default=0, ge=0)

    pass  # Remove this line once you add fields


class Post(BaseModel):
    """Blog post with author and comments.

    TODO: Add the following fields:
    - post_id: str (min 1 char) - Unique post identifier
    - title: str (min 1, max 200 chars) - Post title
    - content: str (min 1 char) - Post content
    - author: Author - Nested Author model
    - published_at: datetime - Publication datetime
    - tags: list[str] (default []) - Post tags
    - comments: list[Comment] (default []) - List of comments
    - status: Literal["draft", "published", "archived"] (default "draft")
    """

    # TODO: Add post_id field

    # TODO: Add title field

    # TODO: Add content field

    # TODO: Add author field (nested model)

    # TODO: Add published_at field

    # TODO: Add tags field
    # Hint: tags: list[str] = []

    # TODO: Add comments field (list of nested models)
    # Hint: comments: list[Comment] = []

    # TODO: Add status field with Literal type
    # Hint: status: Literal["draft", "published", "archived"] = "draft"

    pass  # Remove this line once you add fields


class Blog(BaseModel):
    """Blog containing posts and authors.

    TODO: Add the following fields:
    - name: str (min 1, max 100 chars) - Blog name
    - description: str (default "") - Blog description
    - authors: list[Author] (default []) - Registered authors
    - posts: list[Post] (default []) - All posts
    """

    # TODO: Add name field

    # TODO: Add description field

    # TODO: Add authors field

    # TODO: Add posts field

    pass  # Remove this line once you add fields

    def get_published_posts(self) -> list["Post"]:
        """Return only published posts.

        TODO: Implement this method
        Returns: List of posts where status == "published"

        Hint: Use list comprehension to filter self.posts
        """
        # TODO: Implement this method
        pass

    def total_comments(self) -> int:
        """Count all comments across all posts.

        TODO: Implement this method
        Returns: Total number of comments

        Hint: Sum len(post.comments) for all posts
        """
        # TODO: Implement this method
        pass


def main() -> None:
    """Test your implementation."""
    # TODO: Uncomment and test once you complete the models

    # # Create an author
    # alice = Author(
    #     author_id="auth1",
    #     username="alice_writes",
    #     email="alice@blog.com",
    #     bio="Tech blogger and Python enthusiast"
    # )
    # print(f"Author: {alice.username}")
    # print()
    #
    # # Create a comment
    # comment = Comment(
    #     comment_id="comment1",
    #     author=Author(
    #         author_id="auth2",
    #         username="reader123",
    #         email="reader@example.com"
    #     ),
    #     content="Great article! Very helpful.",
    #     created_at=datetime.now(),
    #     likes=5
    # )
    # print(f"Comment by: {comment.author.username}")
    # print()
    #
    # # Create a post
    # post = Post(
    #     post_id="post1",
    #     title="Introduction to Pydantic",
    #     content="Pydantic is a data validation library...",
    #     author=alice,
    #     published_at=datetime.now(),
    #     tags=["python", "pydantic", "tutorial"],
    #     comments=[comment],
    #     status="published"
    # )
    # print(f"Post: {post.title}")
    # print(f"Tags: {post.tags}")
    # print(f"Comments: {len(post.comments)}")
    # print()
    #
    # # Create a blog from nested dictionaries
    # blog_data = {
    #     "name": "Tech Blog",
    #     "description": "A blog about technology",
    #     "authors": [
    #         {"author_id": "auth1", "username": "alice", "email": "alice@blog.com"}
    #     ],
    #     "posts": [
    #         {
    #             "post_id": "post1",
    #             "title": "My First Post",
    #             "content": "Hello world!",
    #             "author": {"author_id": "auth1", "username": "alice", "email": "alice@blog.com"},
    #             "published_at": "2024-01-15T10:30:00",
    #             "status": "published"
    #         },
    #         {
    #             "post_id": "post2",
    #             "title": "Draft Post",
    #             "content": "Work in progress...",
    #             "author": {"author_id": "auth1", "username": "alice", "email": "alice@blog.com"},
    #             "published_at": "2024-01-16T09:00:00",
    #             "status": "draft"
    #         }
    #     ]
    # }
    #
    # blog = Blog(**blog_data)
    # print(f"Blog: {blog.name}")
    # print(f"Total posts: {len(blog.posts)}")
    # print(f"Published posts: {len(blog.get_published_posts())}")
    # print(f"Total comments: {blog.total_comments()}")

    print("Complete the models and uncomment the test code!")


if __name__ == "__main__":
    main()
