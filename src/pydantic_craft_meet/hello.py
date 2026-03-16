"""Hello world module demonstrating basic business logic."""

from pydantic_craft_meet.models import Greeting


def greet(name: str = "World") -> Greeting:
    """Return a greeting message.

    Args:
        name: The name to greet. Defaults to "World".

    Returns:
        A Greeting model with the message.
    """
    return Greeting.create(name)


def main() -> None:
    """Entry point for the hello module."""
    greeting = greet()
    print(greeting.message)


if __name__ == "__main__":
    main()
