# Exercise 3: Build a Blog System

## Objective

Create a blog system with nested models for Author, Post, and Comment.

## Requirements

Create the following models:

### Author Model
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `author_id` | `str` | Min 1 char | Unique author identifier |
| `username` | `str` | Min 3, Max 50 chars | Display username |
| `email` | `str` | Valid email pattern | Author's email |
| `bio` | `str` | Default: "" | Author biography |

### Comment Model
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `comment_id` | `str` | Min 1 char | Unique comment identifier |
| `author` | `Author` | Required | Nested Author model |
| `content` | `str` | Min 1, Max 1000 chars | Comment text |
| `created_at` | `datetime` | Required | When comment was created |
| `likes` | `int` | >= 0, Default: 0 | Number of likes |

### Post Model
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `post_id` | `str` | Min 1 char | Unique post identifier |
| `title` | `str` | Min 1, Max 200 chars | Post title |
| `content` | `str` | Min 1 char | Post content |
| `author` | `Author` | Required | Nested Author model |
| `published_at` | `datetime` | Required | Publication datetime |
| `tags` | `list[str]` | Default: [] | Post tags |
| `comments` | `list[Comment]` | Default: [] | List of comments |
| `status` | `Literal["draft", "published", "archived"]` | Default: "draft" | Post status |

### Blog Model
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `name` | `str` | Min 1, Max 100 chars | Blog name |
| `description` | `str` | Default: "" | Blog description |
| `authors` | `list[Author]` | Default: [] | Registered authors |
| `posts` | `list[Post]` | Default: [] | All posts |

Add these methods to the `Blog` model:
- `get_published_posts() -> list[Post]`: Return only published posts
- `total_comments() -> int`: Count all comments across all posts

## Steps

1. Open `exercise.py`
2. Complete all four model classes
3. Implement the helper methods on `Blog`
4. Run tests with: `pytest units/unit_03_nested_models/test_solution.py -v`

## Hints

### Nested model field:
```python
author: Author  # This expects an Author instance or dict
```

### List of nested models:
```python
comments: list[Comment] = []
```

### Literal type for status:
```python
from typing import Literal
status: Literal["draft", "published", "archived"] = "draft"
```

### Filtering published posts:
```python
def get_published_posts(self) -> list[Post]:
    return [post for post in self.posts if post.status == "published"]
```

## Expected Behavior

```python
from datetime import datetime

# Create an author
alice = Author(
    author_id="auth1",
    username="alice_writes",
    email="alice@blog.com",
    bio="Tech blogger"
)

# Create a post with nested author
post = Post(
    post_id="post1",
    title="Introduction to Pydantic",
    content="Pydantic is amazing...",
    author=alice,
    published_at=datetime.now(),
    status="published"
)

# Create from nested dictionaries
blog_data = {
    "name": "Tech Blog",
    "posts": [
        {
            "post_id": "post1",
            "title": "My First Post",
            "content": "Hello world!",
            "author": {
                "author_id": "auth1",
                "username": "blogger",
                "email": "blogger@example.com"
            },
            "published_at": "2024-01-15T10:30:00",
            "status": "published"
        }
    ]
}
blog = Blog(**blog_data)
```

## Bonus Challenge

Add a method to `Post`:
- `get_top_comments(n: int = 3) -> list[Comment]`: Return the n most-liked comments
