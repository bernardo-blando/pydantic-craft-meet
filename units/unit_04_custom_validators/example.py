"""Unit 4 Example: Custom Validators.

This example demonstrates an Order model with custom validators
and computed fields for calculating totals.
"""

from datetime import date, datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    computed_field,
    field_validator,
    model_validator,
)


class OrderItem(BaseModel):
    """Individual item in an order."""

    product_name: str = Field(min_length=1)
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(gt=0, decimal_places=2)

    @field_validator("product_name")
    @classmethod
    def normalize_product_name(cls, v: str) -> str:
        """Normalize product name to title case."""
        return v.strip().title()

    @computed_field
    @property
    def line_total(self) -> Decimal:
        """Calculate total for this line item."""
        return self.quantity * self.unit_price


class Order(BaseModel):
    """Order with custom validation and computed fields."""

    order_id: str = Field(min_length=1)
    customer_email: str
    items: list[OrderItem] = Field(min_length=1)
    order_date: date
    shipping_date: date | None = None
    discount_percent: Decimal = Field(default=Decimal("0"), ge=0, le=100)
    notes: str = ""

    @field_validator("customer_email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate and normalize email."""
        v = v.strip().lower()
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Invalid email format")
        return v

    @field_validator("notes")
    @classmethod
    def clean_notes(cls, v: str) -> str:
        """Clean up notes field."""
        return v.strip()

    @field_validator("order_date", mode="before")
    @classmethod
    def parse_order_date(cls, v: str | date) -> date:
        """Parse order date from various formats."""
        if isinstance(v, date):
            return v
        # Try common formats
        for fmt in ["%Y-%m-%d", "%m/%d/%Y", "%d-%m-%Y"]:
            try:
                return datetime.strptime(v, fmt).date()
            except ValueError:
                continue
        raise ValueError(f"Cannot parse date: {v}")

    @model_validator(mode="after")
    def validate_shipping_after_order(self) -> "Order":
        """Ensure shipping date is after order date."""
        if self.shipping_date and self.shipping_date < self.order_date:
            raise ValueError("Shipping date cannot be before order date")
        return self

    @computed_field
    @property
    def subtotal(self) -> Decimal:
        """Calculate subtotal before discount."""
        return sum(item.line_total for item in self.items)

    @computed_field
    @property
    def discount_amount(self) -> Decimal:
        """Calculate discount amount."""
        return (self.subtotal * self.discount_percent / 100).quantize(Decimal("0.01"))

    @computed_field
    @property
    def total(self) -> Decimal:
        """Calculate final total after discount."""
        return self.subtotal - self.discount_amount


class DiscountCode(BaseModel):
    """Discount code with validation."""

    code: str
    percent_off: int = Field(ge=1, le=100)
    min_order_value: Decimal = Field(default=Decimal("0"), ge=0)
    expiry_date: date

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        """Validate and normalize discount code."""
        v = v.strip().upper()
        if not v.isalnum():
            raise ValueError("Code must be alphanumeric")
        if len(v) < 4 or len(v) > 20:
            raise ValueError("Code must be 4-20 characters")
        return v

    @model_validator(mode="after")
    def validate_not_expired(self) -> "DiscountCode":
        """Check if code is not expired."""
        if self.expiry_date < date.today():
            raise ValueError("Discount code has expired")
        return self


def main() -> None:
    """Demonstrate custom validators."""
    # Example 1: Basic order with computed fields
    print("=== Example 1: Order with Computed Fields ===")
    order = Order(
        order_id="ORD-001",
        customer_email="  ALICE@EXAMPLE.COM  ",  # Will be normalized
        items=[
            OrderItem(
                product_name="  laptop  ",  # Will be normalized
                quantity=2,
                unit_price=Decimal("999.99"),
            ),
            OrderItem(
                product_name="mouse",
                quantity=3,
                unit_price=Decimal("29.99"),
            ),
        ],
        order_date="2024-01-15",
        discount_percent=Decimal("10"),
    )

    print(f"Order ID: {order.order_id}")
    print(f"Customer: {order.customer_email}")  # Normalized
    print(f"First item: {order.items[0].product_name}")  # Normalized
    print(f"Subtotal: ${order.subtotal}")
    print(f"Discount ({order.discount_percent}%): ${order.discount_amount}")
    print(f"Total: ${order.total}")
    print()

    # Example 2: Date parsing with mode="before"
    print("=== Example 2: Date Format Parsing ===")
    order2 = Order(
        order_id="ORD-002",
        customer_email="bob@test.com",
        items=[
            OrderItem(
                product_name="Keyboard",
                quantity=1,
                unit_price=Decimal("149.99"),
            )
        ],
        order_date="01/20/2024",  # US format
    )
    print(f"Parsed date: {order2.order_date}")

    order3 = Order(
        order_id="ORD-003",
        customer_email="charlie@test.com",
        items=[
            OrderItem(
                product_name="Monitor",
                quantity=1,
                unit_price=Decimal("399.99"),
            )
        ],
        order_date="15-01-2024",  # European format
    )
    print(f"Parsed date: {order3.order_date}")
    print()

    # Example 3: Model validator (cross-field)
    print("=== Example 3: Cross-field Validation ===")
    try:
        Order(
            order_id="ORD-004",
            customer_email="test@test.com",
            items=[
                OrderItem(
                    product_name="Widget",
                    quantity=1,
                    unit_price=Decimal("10.00"),
                )
            ],
            order_date=date(2024, 1, 20),
            shipping_date=date(2024, 1, 15),  # Before order date!
        )
    except ValidationError as e:
        print(f"Validation error: {e.errors()[0]['msg']}")
    print()

    # Example 4: Field validator errors
    print("=== Example 4: Field Validation Errors ===")
    try:
        Order(
            order_id="ORD-005",
            customer_email="not-an-email",
            items=[
                OrderItem(
                    product_name="Item",
                    quantity=1,
                    unit_price=Decimal("10.00"),
                )
            ],
            order_date=date.today(),
        )
    except ValidationError as e:
        print(f"Email error: {e.errors()[0]['msg']}")

    # Example 5: Computed fields in model_dump
    print()
    print("=== Example 5: Computed Fields in Serialization ===")
    data = order.model_dump()
    print(f"Keys include computed: {'subtotal' in data}")
    print(f"Subtotal in dict: {data.get('subtotal')}")


if __name__ == "__main__":
    main()
