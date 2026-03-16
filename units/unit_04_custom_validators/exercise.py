"""Unit 4 Exercise: Create a PasswordReset Model.

Your task is to create a password reset model with cross-field
validation and computed fields.

Instructions:
1. Complete the PasswordReset class below
2. Implement all validators and computed fields
3. Run tests with: pytest units/04_custom_validators/test_solution.py -v
"""

from pydantic import BaseModel


class PasswordReset(BaseModel):
    """Password reset request model with validation.

    TODO: Add the following fields:
    - user_id: str (min 1 char)
    - email: str
    - new_password: str
    - confirm_password: str
    - reset_token: str (min 32 chars)
    - requested_at: datetime
    - expires_at: datetime

    TODO: Implement these validators:
    1. validate_email - normalize and validate email format
    2. validate_password - check password requirements
    3. validate_token - normalize and validate token
    4. validate_passwords_match - ensure passwords match (model validator)
    5. validate_expiry - ensure expires_at > requested_at (model validator)

    TODO: Implement these computed fields:
    1. is_expired - True if current time > expires_at
    2. password_strength - "weak"/"medium"/"strong" based on length
    """

    # TODO: Add fields here
    # user_id: str = Field(min_length=1)
    # email: str
    # new_password: str
    # confirm_password: str
    # reset_token: str = Field(min_length=32)
    # requested_at: datetime
    # expires_at: datetime

    pass  # Remove this line once you add fields

    # TODO: Implement email validator
    # @field_validator("email")
    # @classmethod
    # def validate_email(cls, v: str) -> str:
    #     """Validate and normalize email.
    #
    #     - Strip whitespace
    #     - Convert to lowercase
    #     - Check for @ and . after @
    #     """
    #     pass

    # TODO: Implement password validator
    # @field_validator("new_password")
    # @classmethod
    # def validate_password(cls, v: str) -> str:
    #     """Validate password requirements.
    #
    #     Requirements:
    #     - Minimum 8 characters
    #     - At least one uppercase letter
    #     - At least one lowercase letter
    #     - At least one digit
    #     - At least one special character (!@#$%^&*)
    #
    #     Hint: Use re.search() for pattern matching
    #     """
    #     import re
    #     # Check length
    #     # Check uppercase: re.search(r"[A-Z]", v)
    #     # Check lowercase: re.search(r"[a-z]", v)
    #     # Check digit: re.search(r"\d", v)
    #     # Check special: re.search(r"[!@#$%^&*]", v)
    #     pass

    # TODO: Implement token validator
    # @field_validator("reset_token")
    # @classmethod
    # def validate_token(cls, v: str) -> str:
    #     """Validate reset token.
    #
    #     - Convert to lowercase
    #     - Must be alphanumeric only
    #     """
    #     pass

    # TODO: Implement model validator for password match
    # @model_validator(mode="after")
    # def validate_passwords_match(self) -> "PasswordReset":
    #     """Ensure new_password equals confirm_password."""
    #     pass

    # TODO: Implement model validator for expiry
    # @model_validator(mode="after")
    # def validate_expiry(self) -> "PasswordReset":
    #     """Ensure expires_at is after requested_at."""
    #     pass

    # TODO: Implement computed field for is_expired
    # @computed_field
    # @property
    # def is_expired(self) -> bool:
    #     """Check if reset request has expired."""
    #     pass

    # TODO: Implement computed field for password_strength
    # @computed_field
    # @property
    # def password_strength(self) -> str:
    #     """Calculate password strength based on length.
    #
    #     Returns:
    #     - "weak": 8-11 characters
    #     - "medium": 12-15 characters
    #     - "strong": 16+ characters
    #     """
    #     pass


def main() -> None:
    """Test your implementation."""
    # TODO: Uncomment and test once you complete the model

    # from datetime import timedelta
    # from pydantic import ValidationError
    #
    # # Test valid password reset
    # reset = PasswordReset(
    #     user_id="user123",
    #     email="  TEST@EXAMPLE.COM  ",
    #     new_password="SecurePass1!",
    #     confirm_password="SecurePass1!",
    #     reset_token="abc123def456ghi789jkl012mno345pq",
    #     requested_at=datetime.now(),
    #     expires_at=datetime.now() + timedelta(hours=1),
    # )
    #
    # print(f"User ID: {reset.user_id}")
    # print(f"Email (normalized): {reset.email}")
    # print(f"Is expired: {reset.is_expired}")
    # print(f"Password strength: {reset.password_strength}")
    # print()
    #
    # # Test validation errors
    # print("Testing validation errors:")
    #
    # # Passwords don't match
    # try:
    #     PasswordReset(
    #         user_id="user123",
    #         email="test@example.com",
    #         new_password="SecurePass1!",
    #         confirm_password="DifferentPass1!",
    #         reset_token="abc123def456ghi789jkl012mno345pq",
    #         requested_at=datetime.now(),
    #         expires_at=datetime.now() + timedelta(hours=1),
    #     )
    # except ValidationError as e:
    #     print(f"  Password mismatch: {e.errors()[0]['msg']}")
    #
    # # Weak password
    # try:
    #     PasswordReset(
    #         user_id="user123",
    #         email="test@example.com",
    #         new_password="weak",
    #         confirm_password="weak",
    #         reset_token="abc123def456ghi789jkl012mno345pq",
    #         requested_at=datetime.now(),
    #         expires_at=datetime.now() + timedelta(hours=1),
    #     )
    # except ValidationError as e:
    #     print(f"  Weak password: {e.errors()[0]['msg']}")

    print("Complete the PasswordReset model and uncomment the test code!")


if __name__ == "__main__":
    main()
