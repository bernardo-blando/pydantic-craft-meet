"""Tests for Unit 4: Custom Validators."""

from datetime import datetime, timedelta

import pytest
from pydantic import ValidationError

from units.unit_04_custom_validators.solution import PasswordReset


class TestPasswordReset:
    """Tests for the PasswordReset model."""

    @pytest.fixture
    def valid_data(self):
        """Return valid password reset data."""
        return {
            "user_id": "user123",
            "email": "test@example.com",
            "new_password": "SecurePass1!",
            "confirm_password": "SecurePass1!",
            "reset_token": "abc123def456ghi789jkl012mno345pq",
            "requested_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(hours=1),
        }

    def test_create_valid_reset(self, valid_data):
        """Test creating a valid password reset."""
        reset = PasswordReset(**valid_data)

        assert reset.user_id == "user123"
        assert reset.email == "test@example.com"

    def test_email_normalized(self, valid_data):
        """Test that email is normalized to lowercase."""
        valid_data["email"] = "  TEST@EXAMPLE.COM  "
        reset = PasswordReset(**valid_data)

        assert reset.email == "test@example.com"

    def test_email_invalid_no_at(self, valid_data):
        """Test that email without @ is rejected."""
        valid_data["email"] = "invalid-email"
        with pytest.raises(ValidationError) as exc_info:
            PasswordReset(**valid_data)

        assert "email" in str(exc_info.value).lower()

    def test_email_invalid_no_dot(self, valid_data):
        """Test that email without dot in domain is rejected."""
        valid_data["email"] = "test@example"
        with pytest.raises(ValidationError) as exc_info:
            PasswordReset(**valid_data)

        assert "email" in str(exc_info.value).lower()

    def test_password_too_short(self, valid_data):
        """Test that password under 8 characters is rejected."""
        valid_data["new_password"] = "Short1!"
        valid_data["confirm_password"] = "Short1!"

        with pytest.raises(ValidationError) as exc_info:
            PasswordReset(**valid_data)

        assert "8 characters" in str(exc_info.value)

    def test_password_missing_uppercase(self, valid_data):
        """Test that password without uppercase is rejected."""
        valid_data["new_password"] = "lowercase1!"
        valid_data["confirm_password"] = "lowercase1!"

        with pytest.raises(ValidationError) as exc_info:
            PasswordReset(**valid_data)

        assert "uppercase" in str(exc_info.value)

    def test_password_missing_lowercase(self, valid_data):
        """Test that password without lowercase is rejected."""
        valid_data["new_password"] = "UPPERCASE1!"
        valid_data["confirm_password"] = "UPPERCASE1!"

        with pytest.raises(ValidationError) as exc_info:
            PasswordReset(**valid_data)

        assert "lowercase" in str(exc_info.value)

    def test_password_missing_digit(self, valid_data):
        """Test that password without digit is rejected."""
        valid_data["new_password"] = "NoDigits!!"
        valid_data["confirm_password"] = "NoDigits!!"

        with pytest.raises(ValidationError) as exc_info:
            PasswordReset(**valid_data)

        assert "digit" in str(exc_info.value)

    def test_password_missing_special(self, valid_data):
        """Test that password without special character is rejected."""
        valid_data["new_password"] = "NoSpecial1"
        valid_data["confirm_password"] = "NoSpecial1"

        with pytest.raises(ValidationError) as exc_info:
            PasswordReset(**valid_data)

        assert "special" in str(exc_info.value)

    def test_passwords_must_match(self, valid_data):
        """Test that passwords must match."""
        valid_data["confirm_password"] = "DifferentPass1!"

        with pytest.raises(ValidationError) as exc_info:
            PasswordReset(**valid_data)

        assert "match" in str(exc_info.value).lower()

    def test_token_normalized(self, valid_data):
        """Test that token is normalized to lowercase."""
        valid_data["reset_token"] = "ABC123DEF456GHI789JKL012MNO345PQ"
        reset = PasswordReset(**valid_data)

        assert reset.reset_token == "abc123def456ghi789jkl012mno345pq"

    def test_token_must_be_alphanumeric(self, valid_data):
        """Test that token must be alphanumeric."""
        valid_data["reset_token"] = "abc-123-def-456-ghi-789-jkl-012!"

        with pytest.raises(ValidationError) as exc_info:
            PasswordReset(**valid_data)

        assert "alphanumeric" in str(exc_info.value)

    def test_expiry_must_be_after_request(self, valid_data):
        """Test that expiry must be after request time."""
        valid_data["expires_at"] = valid_data["requested_at"] - timedelta(hours=1)

        with pytest.raises(ValidationError) as exc_info:
            PasswordReset(**valid_data)

        assert "expir" in str(exc_info.value).lower()

    def test_is_expired_false(self, valid_data):
        """Test is_expired returns False for future expiry."""
        reset = PasswordReset(**valid_data)

        assert reset.is_expired is False

    def test_is_expired_true(self, valid_data):
        """Test is_expired returns True for past expiry."""
        valid_data["requested_at"] = datetime.now() - timedelta(hours=2)
        valid_data["expires_at"] = datetime.now() - timedelta(hours=1)

        reset = PasswordReset(**valid_data)

        assert reset.is_expired is True

    def test_password_strength_weak(self, valid_data):
        """Test password_strength returns weak for 8-11 chars."""
        valid_data["new_password"] = "Secure1!!"  # 9 chars
        valid_data["confirm_password"] = "Secure1!!"

        reset = PasswordReset(**valid_data)

        assert reset.password_strength == "weak"

    def test_password_strength_medium(self, valid_data):
        """Test password_strength returns medium for 12-15 chars."""
        valid_data["new_password"] = "SecurePass12!"  # 13 chars
        valid_data["confirm_password"] = "SecurePass12!"

        reset = PasswordReset(**valid_data)

        assert reset.password_strength == "medium"

    def test_password_strength_strong(self, valid_data):
        """Test password_strength returns strong for 16+ chars."""
        valid_data["new_password"] = "VerySecurePass123!"  # 18 chars
        valid_data["confirm_password"] = "VerySecurePass123!"

        reset = PasswordReset(**valid_data)

        assert reset.password_strength == "strong"

    def test_time_until_expiry_returns_timedelta(self, valid_data):
        """Test time_until_expiry returns timedelta when not expired."""
        reset = PasswordReset(**valid_data)

        result = reset.time_until_expiry()

        assert isinstance(result, timedelta)
        assert result > timedelta(0)

    def test_time_until_expiry_returns_none_when_expired(self, valid_data):
        """Test time_until_expiry returns None when expired."""
        valid_data["requested_at"] = datetime.now() - timedelta(hours=2)
        valid_data["expires_at"] = datetime.now() - timedelta(hours=1)

        reset = PasswordReset(**valid_data)

        assert reset.time_until_expiry() is None

    def test_computed_fields_in_model_dump(self, valid_data):
        """Test that computed fields appear in model_dump."""
        reset = PasswordReset(**valid_data)
        data = reset.model_dump()

        assert "is_expired" in data
        assert "password_strength" in data
