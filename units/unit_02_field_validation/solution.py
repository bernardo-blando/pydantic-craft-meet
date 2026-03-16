"""Unit 2 Solution: BankAccount Model.

This is the complete solution for the BankAccount model exercise.
Compare your solution with this one after completing the exercise.
"""

from pydantic import BaseModel, Field


class BankAccount(BaseModel):
    """Bank account model with strict field validation.

    This model demonstrates:
    - Pattern validation with regex
    - String length constraints
    - Numeric range constraints
    - Optional fields with constraints
    - Default values
    - Field descriptions
    """

    account_number: str = Field(
        pattern=r"^\d{10}$",
        description="Unique 10-digit account number",
        examples=["1234567890"],
    )

    account_holder: str = Field(
        min_length=2,
        max_length=100,
        description="Full name of account holder",
    )

    account_type: str = Field(
        min_length=1,
        description="Account type (e.g., checking, savings)",
    )

    balance: float = Field(
        ge=0,
        description="Current account balance (must be non-negative)",
    )

    currency: str = Field(
        pattern=r"^[A-Z]{3}$",
        description="Currency code (e.g., USD, EUR, GBP)",
        examples=["USD", "EUR", "GBP"],
    )

    is_active: bool = Field(
        default=True,
        description="Whether the account is active",
    )

    overdraft_limit: float | None = Field(
        default=None,
        ge=0,
        description="Optional overdraft limit (must be non-negative if provided)",
    )

    email: str | None = Field(
        default=None,
        pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$",
        description="Contact email for notifications",
    )

    def can_withdraw(self, amount: float) -> bool:
        """Check if a withdrawal is possible.

        Args:
            amount: The amount to withdraw.

        Returns:
            True if the withdrawal is allowed, False otherwise.
        """
        if amount <= 0:
            return False

        available = self.balance
        if self.overdraft_limit is not None:
            available += self.overdraft_limit

        return amount <= available


def main() -> None:
    """Demonstrate the BankAccount model."""
    from pydantic import ValidationError

    # Example 1: Basic account
    print("=== Example 1: Basic Account ===")
    account = BankAccount(
        account_number="1234567890",
        account_holder="Alice Johnson",
        account_type="checking",
        balance=1500.00,
        currency="USD",
    )
    print(f"Account: {account.account_number}")
    print(f"Holder: {account.account_holder}")
    print(f"Balance: {account.currency} {account.balance:,.2f}")
    print(f"Active: {account.is_active}")
    print(f"Overdraft: {account.overdraft_limit}")
    print()

    # Example 2: Account with all fields
    print("=== Example 2: Full Account ===")
    full_account = BankAccount(
        account_number="9876543210",
        account_holder="Bob Smith",
        account_type="savings",
        balance=5000.00,
        currency="EUR",
        is_active=True,
        overdraft_limit=500.00,
        email="bob.smith@example.com",
    )
    print(f"Account: {full_account.account_number}")
    print(f"Email: {full_account.email}")
    print(
        f"Overdraft limit: {full_account.currency} {full_account.overdraft_limit:,.2f}"
    )
    print()

    # Example 3: Can withdraw check
    print("=== Example 3: Withdrawal Check ===")
    print(f"Balance: {full_account.balance}, Overdraft: {full_account.overdraft_limit}")
    print(f"Can withdraw 4000? {full_account.can_withdraw(4000)}")  # True
    print(
        f"Can withdraw 5500? {full_account.can_withdraw(5500)}"
    )  # True (with overdraft)
    print(f"Can withdraw 6000? {full_account.can_withdraw(6000)}")  # False
    print()

    # Example 4: Validation errors
    print("=== Example 4: Validation Errors ===")

    # Invalid account number (not 10 digits)
    try:
        BankAccount(
            account_number="12345",
            account_holder="Test User",
            account_type="checking",
            balance=100,
            currency="USD",
        )
    except ValidationError as e:
        print(f"Invalid account_number: {e.errors()[0]['msg']}")

    # Negative balance
    try:
        BankAccount(
            account_number="1234567890",
            account_holder="Test User",
            account_type="checking",
            balance=-100,
            currency="USD",
        )
    except ValidationError as e:
        print(f"Negative balance: {e.errors()[0]['msg']}")

    # Invalid currency (lowercase)
    try:
        BankAccount(
            account_number="1234567890",
            account_holder="Test User",
            account_type="checking",
            balance=100,
            currency="usd",
        )
    except ValidationError as e:
        print(f"Invalid currency: {e.errors()[0]['msg']}")

    # Invalid email format
    try:
        BankAccount(
            account_number="1234567890",
            account_holder="Test User",
            account_type="checking",
            balance=100,
            currency="USD",
            email="not-an-email",
        )
    except ValidationError as e:
        print(f"Invalid email: {e.errors()[0]['msg']}")

    # Account holder name too short
    try:
        BankAccount(
            account_number="1234567890",
            account_holder="X",
            account_type="checking",
            balance=100,
            currency="USD",
        )
    except ValidationError as e:
        print(f"Name too short: {e.errors()[0]['msg']}")


if __name__ == "__main__":
    main()
