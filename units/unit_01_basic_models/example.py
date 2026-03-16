"""Unit 1 Example: Basic Models and Types.

This example demonstrates how to create a simple Pydantic model
for a user profile with various data types.
"""

from datetime import date

from pydantic import BaseModel


class UserProfile(BaseModel):
    """A simple user profile model demonstrating basic Pydantic types.

    This model shows how Pydantic handles different data types
    and performs automatic type coercion when possible.
    """

    # Required string field
    username: str

    # Required integer field
    age: int

    # Required float field
    height: float

    # Required boolean field
    is_active: bool

    # Required date field
    join_date: date

    # Optional field with default value
    bio: str = "No bio provided"

    # List of strings with default empty list
    interests: list[str] = []


def main() -> None:
    """Demonstrate basic model creation and usage."""
    # Example 1: Create a model with all required fields
    print("=== Example 1: Basic Model Creation ===")
    user1 = UserProfile(
        username="alice_dev",
        age=28,
        height=1.65,
        is_active=True,
        join_date=date(2023, 1, 15),
    )
    print(f"User: {user1.username}")
    print(f"Age: {user1.age}")
    print(f"Active: {user1.is_active}")
    print(f"Bio: {user1.bio}")  # Uses default value
    print()

    # Example 2: Type coercion in action
    print("=== Example 2: Type Coercion ===")
    user2 = UserProfile(
        username="bob_coder",
        age="35",  # String will be coerced to int
        height="1.80",  # String will be coerced to float
        is_active="true",  # String will be coerced to bool
        join_date="2024-06-01",  # String will be parsed as date
        interests=["Python", "Pydantic"],
    )
    print(f"Age type: {type(user2.age).__name__} = {user2.age}")
    print(f"Height type: {type(user2.height).__name__} = {user2.height}")
    print(f"Active type: {type(user2.is_active).__name__} = {user2.is_active}")
    print(f"Join date type: {type(user2.join_date).__name__} = {user2.join_date}")
    print()

    # Example 3: Converting to dictionary with model_dump()
    print("=== Example 3: model_dump() ===")
    user_dict = user1.model_dump()
    print(f"Dictionary: {user_dict}")
    print(f"Type: {type(user_dict)}")
    print()

    # Example 4: Creating from dictionary
    print("=== Example 4: Creating from Dictionary ===")
    data = {
        "username": "charlie",
        "age": 42,
        "height": 1.75,
        "is_active": False,
        "join_date": "2022-03-20",
        "bio": "Software engineer",
        "interests": ["FastAPI", "Testing"],
    }
    user3 = UserProfile(**data)
    print(f"Created user: {user3.username}")
    print(f"Interests: {user3.interests}")


if __name__ == "__main__":
    main()
