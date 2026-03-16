"""Unit 4 Solution: PasswordReset Model.

This is the complete solution for the PasswordReset model exercise.
Compare your solution with this one after completing the exercise.
"""

import re
from datetime import datetime, timedelta

from pydantic import BaseModel, Field, computed_field, field_validator, model_validator


class PasswordReset(BaseModel):
    """Password reset request model with comprehensive validation.

    This model demonstrates:
    - Field validators for individual field validation
    - Model validators for cross-field validation
    - Computed fields for derived values
    - Various validation techniques
    """

    user_id: str = Field(min_length=1, description="User identifier")
    email: str = Field(description="User's email address")
    new_password: str = Field(description="The new password")
    confirm_password: str = Field(description="Password confirmation")
    reset_token: str = Field(
        min_length=32, description="Reset token (min 32 characters)"
    )
    requested_at: datetime = Field(description="When reset was requested")
    expires_at: datetime = Field(description="When reset expires")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate and normalize email.

        - Strips whitespace
        - Converts to lowercase
        - Validates basic email format
        """
        v = v.strip().lower()
        if "@" not in v:
            raise ValueError("Email must contain @")
        if "." not in v.split("@")[-1]:
            raise ValueError("Email domain must contain a dot")
        return v

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password meets security requirements.

        Requirements:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character (!@#$%^&*)
        """
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")

        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")

        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")

        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")

        if not re.search(r"[!@#$%^&*]", v):
            raise ValueError(
                "Password must contain at least one special character (!@#$%^&*)"
            )

        return v

    @field_validator("reset_token")
    @classmethod
    def validate_token(cls, v: str) -> str:
        """Validate and normalize reset token.

        - Converts to lowercase
        - Must be alphanumeric only
        """
        v = v.lower()
        if not v.isalnum():
            raise ValueError("Token must be alphanumeric")
        return v

    @model_validator(mode="after")
    def validate_passwords_match(self) -> "PasswordReset":
        """Ensure new_password matches confirm_password."""
        if self.new_password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self

    @model_validator(mode="after")
    def validate_expiry(self) -> "PasswordReset":
        """Ensure expires_at is after requested_at."""
        if self.expires_at <= self.requested_at:
            raise ValueError("Expiry time must be after request time")
        return self

    @computed_field
    @property
    def is_expired(self) -> bool:
        """Check if the reset request has expired."""
        return datetime.now() > self.expires_at

    @computed_field
    @property
    def password_strength(self) -> str:
        """Calculate password strength based on length.

        Returns:
            - "weak": 8-11 characters
            - "medium": 12-15 characters
            - "strong": 16+ characters
        """
        length = len(self.new_password)
        if length >= 16:
            return "strong"
        elif length >= 12:
            return "medium"
        else:
            return "weak"

    def time_until_expiry(self) -> timedelta | None:
        """Calculate time remaining until expiration.

        Returns:
            Time remaining as timedelta, or None if already expired.
        """
        if self.is_expired:
            return None
        return self.expires_at - datetime.now()


def main() -> None:
    """Demonstrate the PasswordReset model."""
    from pydantic import ValidationError

    # Example 1: Valid password reset
    print("=== Example 1: Valid Password Reset ===")
    reset = PasswordReset(
        user_id="user123",
        email="  TEST@EXAMPLE.COM  ",  # Will be normalized
        new_password="SecurePass1!",
        confirm_password="SecurePass1!",
        reset_token="abc123def456ghi789jkl012mno345pq",
        requested_at=datetime.now(),
        expires_at=datetime.now() + timedelta(hours=1),
    )

    print(f"User ID: {reset.user_id}")
    print(f"Email (normalized): {reset.email}")
    print(f"Token (normalized): {reset.reset_token}")
    print(f"Is expired: {reset.is_expired}")
    print(f"Password strength: {reset.password_strength}")
    time_left = reset.time_until_expiry()
    if time_left:
        print(f"Time until expiry: {time_left}")
    print()

    # Example 2: Strong password
    print("=== Example 2: Strong Password ===")
    strong_reset = PasswordReset(
        user_id="user456",
        email="strong@test.com",
        new_password="VerySecurePassword123!",  # 22 chars
        confirm_password="VerySecurePassword123!",
        reset_token="xyz789abc012def345ghi678jkl901mn",
        requested_at=datetime.now(),
        expires_at=datetime.now() + timedelta(hours=2),
    )
    print(f"Password length: {len(strong_reset.new_password)}")
    print(f"Password strength: {strong_reset.password_strength}")
    print()

    # Example 3: Validation errors
    print("=== Example 3: Validation Errors ===")

    # Passwords don't match
    try:
        PasswordReset(
            user_id="user123",
            email="test@example.com",
            new_password="SecurePass1!",
            confirm_password="DifferentPass1!",
            reset_token="abc123def456ghi789jkl012mno345pq",
            requested_at=datetime.now(),
            expires_at=datetime.now() + timedelta(hours=1),
        )
    except ValidationError as e:
        print(f"Password mismatch: {e.errors()[0]['msg']}")

    # Password missing uppercase
    try:
        PasswordReset(
            user_id="user123",
            email="test@example.com",
            new_password="lowercase1!",
            confirm_password="lowercase1!",
            reset_token="abc123def456ghi789jkl012mno345pq",
            requested_at=datetime.now(),
            expires_at=datetime.now() + timedelta(hours=1),
        )
    except ValidationError as e:
        print(f"Missing uppercase: {e.errors()[0]['msg']}")

    # Password too short
    try:
        PasswordReset(
            user_id="user123",
            email="test@example.com",
            new_password="Short1!",
            confirm_password="Short1!",
            reset_token="abc123def456ghi789jkl012mno345pq",
            requested_at=datetime.now(),
            expires_at=datetime.now() + timedelta(hours=1),
        )
    except ValidationError as e:
        print(f"Too short: {e.errors()[0]['msg']}")

    # Invalid email
    try:
        PasswordReset(
            user_id="user123",
            email="not-an-email",
            new_password="SecurePass1!",
            confirm_password="SecurePass1!",
            reset_token="abc123def456ghi789jkl012mno345pq",
            requested_at=datetime.now(),
            expires_at=datetime.now() + timedelta(hours=1),
        )
    except ValidationError as e:
        print(f"Invalid email: {e.errors()[0]['msg']}")

    # Expiry before request
    try:
        PasswordReset(
            user_id="user123",
            email="test@example.com",
            new_password="SecurePass1!",
            confirm_password="SecurePass1!",
            reset_token="abc123def456ghi789jkl012mno345pq",
            requested_at=datetime.now(),
            expires_at=datetime.now() - timedelta(hours=1),  # In the past!
        )
    except ValidationError as e:
        print(f"Invalid expiry: {e.errors()[0]['msg']}")

    # Example 4: Expired reset
    print()
    print("=== Example 4: Expired Reset ===")
    expired_reset = PasswordReset(
        user_id="user789",
        email="expired@test.com",
        new_password="SecurePass1!",
        confirm_password="SecurePass1!",
        reset_token="abc123def456ghi789jkl012mno345pq",
        requested_at=datetime.now() - timedelta(hours=2),
        expires_at=datetime.now() - timedelta(hours=1),  # Already expired
    )
    print(f"Is expired: {expired_reset.is_expired}")
    print(f"Time until expiry: {expired_reset.time_until_expiry()}")


if __name__ == "__main__":
    main()
