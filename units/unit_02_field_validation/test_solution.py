"""Tests for Unit 2: Field Validation and Constraints."""

import pytest
from pydantic import ValidationError

from units.unit_02_field_validation.solution import BankAccount


class TestBankAccount:
    """Tests for the BankAccount model."""

    def test_create_valid_account(self):
        """Test creating a valid bank account."""
        account = BankAccount(
            account_number="1234567890",
            account_holder="Alice Johnson",
            account_type="checking",
            balance=1500.00,
            currency="USD",
        )

        assert account.account_number == "1234567890"
        assert account.account_holder == "Alice Johnson"
        assert account.account_type == "checking"
        assert account.balance == 1500.00
        assert account.currency == "USD"

    def test_default_values(self):
        """Test that optional fields have correct defaults."""
        account = BankAccount(
            account_number="1234567890",
            account_holder="Test User",
            account_type="savings",
            balance=100.00,
            currency="EUR",
        )

        assert account.is_active is True
        assert account.overdraft_limit is None
        assert account.email is None

    def test_create_account_with_all_fields(self):
        """Test creating account with all fields specified."""
        account = BankAccount(
            account_number="9876543210",
            account_holder="Bob Smith",
            account_type="savings",
            balance=5000.00,
            currency="GBP",
            is_active=False,
            overdraft_limit=1000.00,
            email="bob@example.com",
        )

        assert account.is_active is False
        assert account.overdraft_limit == 1000.00
        assert account.email == "bob@example.com"

    def test_invalid_account_number_too_short(self):
        """Test that account number must be exactly 10 digits."""
        with pytest.raises(ValidationError) as exc_info:
            BankAccount(
                account_number="12345",
                account_holder="Test User",
                account_type="checking",
                balance=100,
                currency="USD",
            )

        assert "account_number" in str(exc_info.value)

    def test_invalid_account_number_too_long(self):
        """Test that account number must be exactly 10 digits."""
        with pytest.raises(ValidationError) as exc_info:
            BankAccount(
                account_number="12345678901234",
                account_holder="Test User",
                account_type="checking",
                balance=100,
                currency="USD",
            )

        assert "account_number" in str(exc_info.value)

    def test_invalid_account_number_letters(self):
        """Test that account number must contain only digits."""
        with pytest.raises(ValidationError) as exc_info:
            BankAccount(
                account_number="123456789A",
                account_holder="Test User",
                account_type="checking",
                balance=100,
                currency="USD",
            )

        assert "account_number" in str(exc_info.value)

    def test_account_holder_too_short(self):
        """Test that account holder name must be at least 2 characters."""
        with pytest.raises(ValidationError) as exc_info:
            BankAccount(
                account_number="1234567890",
                account_holder="X",
                account_type="checking",
                balance=100,
                currency="USD",
            )

        assert "account_holder" in str(exc_info.value)

    def test_account_holder_too_long(self):
        """Test that account holder name must not exceed 100 characters."""
        with pytest.raises(ValidationError) as exc_info:
            BankAccount(
                account_number="1234567890",
                account_holder="X" * 101,
                account_type="checking",
                balance=100,
                currency="USD",
            )

        assert "account_holder" in str(exc_info.value)

    def test_negative_balance_rejected(self):
        """Test that negative balance is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            BankAccount(
                account_number="1234567890",
                account_holder="Test User",
                account_type="checking",
                balance=-100,
                currency="USD",
            )

        assert "balance" in str(exc_info.value)

    def test_zero_balance_allowed(self):
        """Test that zero balance is allowed."""
        account = BankAccount(
            account_number="1234567890",
            account_holder="Test User",
            account_type="checking",
            balance=0,
            currency="USD",
        )

        assert account.balance == 0

    def test_invalid_currency_lowercase(self):
        """Test that currency must be uppercase."""
        with pytest.raises(ValidationError) as exc_info:
            BankAccount(
                account_number="1234567890",
                account_holder="Test User",
                account_type="checking",
                balance=100,
                currency="usd",
            )

        assert "currency" in str(exc_info.value)

    def test_invalid_currency_wrong_length(self):
        """Test that currency must be exactly 3 characters."""
        with pytest.raises(ValidationError) as exc_info:
            BankAccount(
                account_number="1234567890",
                account_holder="Test User",
                account_type="checking",
                balance=100,
                currency="USDD",
            )

        assert "currency" in str(exc_info.value)

    def test_invalid_email_format(self):
        """Test that email must be valid format."""
        with pytest.raises(ValidationError) as exc_info:
            BankAccount(
                account_number="1234567890",
                account_holder="Test User",
                account_type="checking",
                balance=100,
                currency="USD",
                email="not-an-email",
            )

        assert "email" in str(exc_info.value)

    def test_valid_email_accepted(self):
        """Test that valid email is accepted."""
        account = BankAccount(
            account_number="1234567890",
            account_holder="Test User",
            account_type="checking",
            balance=100,
            currency="USD",
            email="user@example.com",
        )

        assert account.email == "user@example.com"

    def test_negative_overdraft_rejected(self):
        """Test that negative overdraft limit is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            BankAccount(
                account_number="1234567890",
                account_holder="Test User",
                account_type="checking",
                balance=100,
                currency="USD",
                overdraft_limit=-500,
            )

        assert "overdraft_limit" in str(exc_info.value)

    def test_can_withdraw_within_balance(self):
        """Test can_withdraw returns True when within balance."""
        account = BankAccount(
            account_number="1234567890",
            account_holder="Test User",
            account_type="checking",
            balance=1000,
            currency="USD",
        )

        assert account.can_withdraw(500) is True
        assert account.can_withdraw(1000) is True

    def test_can_withdraw_exceeds_balance_no_overdraft(self):
        """Test can_withdraw returns False when exceeding balance without overdraft."""
        account = BankAccount(
            account_number="1234567890",
            account_holder="Test User",
            account_type="checking",
            balance=1000,
            currency="USD",
        )

        assert account.can_withdraw(1001) is False

    def test_can_withdraw_with_overdraft(self):
        """Test can_withdraw considers overdraft limit."""
        account = BankAccount(
            account_number="1234567890",
            account_holder="Test User",
            account_type="checking",
            balance=1000,
            currency="USD",
            overdraft_limit=500,
        )

        assert account.can_withdraw(1000) is True
        assert account.can_withdraw(1500) is True
        assert account.can_withdraw(1501) is False

    def test_can_withdraw_zero_or_negative(self):
        """Test can_withdraw returns False for zero or negative amounts."""
        account = BankAccount(
            account_number="1234567890",
            account_holder="Test User",
            account_type="checking",
            balance=1000,
            currency="USD",
        )

        assert account.can_withdraw(0) is False
        assert account.can_withdraw(-100) is False
