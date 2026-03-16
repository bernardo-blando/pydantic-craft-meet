"""Unit 2 Exercise: Create a BankAccount Model.

Your task is to create a Pydantic model for a bank account
with strict field validation.

Instructions:
1. Complete the BankAccount class below
2. Add all required fields with proper Field() constraints
3. Run tests with: pytest units/02_field_validation/test_solution.py -v
"""

from pydantic import BaseModel


class BankAccount(BaseModel):
    r"""Bank account model with strict validation.

    TODO: Add the following fields with constraints:

    - account_number: str
      Pattern: exactly 10 digits (^\d{10}$)
      Description: "Unique 10-digit account number"

    - account_holder: str
      Min length: 2, Max length: 100
      Description: "Full name of account holder"

    - account_type: str
      Min length: 1
      Description: "Account type (e.g., checking, savings)"

    - balance: float
      Must be >= 0
      Description: "Current account balance"

    - currency: str
      Pattern: exactly 3 uppercase letters (^[A-Z]{3}$)
      Description: "Currency code (e.g., USD, EUR, GBP)"

    - is_active: bool
      Default: True
      Description: "Whether the account is active"

    - overdraft_limit: float | None
      Default: None, must be >= 0 if provided
      Description: "Optional overdraft limit"

    - email: str | None
      Default: None, must match email pattern if provided
      Pattern: ^[\w\.-]+@[\w\.-]+\.\w+$
      Description: "Contact email for notifications"
    """

    # TODO: Add account_number field with pattern constraint
    # Hint: pattern=r"^\d{10}$"

    # TODO: Add account_holder field with length constraints
    # Hint: min_length=2, max_length=100

    # TODO: Add account_type field
    # Hint: min_length=1

    # TODO: Add balance field with minimum constraint
    # Hint: ge=0

    # TODO: Add currency field with pattern constraint
    # Hint: pattern=r"^[A-Z]{3}$"

    # TODO: Add is_active field with default value
    # Hint: is_active: bool = True

    # TODO: Add overdraft_limit optional field
    # Hint: overdraft_limit: float | None = Field(default=None, ge=0)

    # TODO: Add email optional field with pattern
    # Hint: email: str | None = Field(default=None, pattern=r"...")

    pass  # Remove this line once you add fields


def main() -> None:
    """Test your implementation."""
    # TODO: Uncomment and test once you complete the model

    # from pydantic import ValidationError
    #
    # # Test valid account
    # account = BankAccount(
    #     account_number="1234567890",
    #     account_holder="Alice Johnson",
    #     account_type="checking",
    #     balance=1500.00,
    #     currency="USD",
    # )
    # print(f"Account: {account.account_number}")
    # print(f"Holder: {account.account_holder}")
    # print(f"Balance: {account.currency} {account.balance}")
    # print(f"Active: {account.is_active}")
    # print()
    #
    # # Test with all fields
    # full_account = BankAccount(
    #     account_number="9876543210",
    #     account_holder="Bob Smith",
    #     account_type="savings",
    #     balance=5000.00,
    #     currency="EUR",
    #     is_active=True,
    #     overdraft_limit=500.00,
    #     email="bob@example.com",
    # )
    # print(f"Overdraft limit: {full_account.overdraft_limit}")
    # print(f"Email: {full_account.email}")
    # print()
    #
    # # Test validation errors
    # print("Testing validation errors:")
    #
    # try:
    #     BankAccount(
    #         account_number="123",  # Invalid: not 10 digits
    #         account_holder="Test",
    #         account_type="checking",
    #         balance=100,
    #         currency="USD",
    #     )
    # except ValidationError as e:
    #     print(f"  Invalid account number: {e.errors()[0]['msg']}")
    #
    # try:
    #     BankAccount(
    #         account_number="1234567890",
    #         account_holder="Test",
    #         account_type="checking",
    #         balance=-100,  # Invalid: negative
    #         currency="USD",
    #     )
    # except ValidationError as e:
    #     print(f"  Negative balance: {e.errors()[0]['msg']}")

    print("Complete the BankAccount model and uncomment the test code!")


if __name__ == "__main__":
    main()
