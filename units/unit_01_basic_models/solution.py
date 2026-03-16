"""Unit 1 Solution: Product Model.

This is the complete solution for the Product model exercise.
Compare your solution with this one after completing the exercise.
"""

from pydantic import BaseModel


class Product(BaseModel):
    """E-commerce product model.

    This model demonstrates basic Pydantic features:
    - Required fields (no default value)
    - Optional fields (with default value)
    - Various data types (str, float, int, bool, list)
    - Instance methods
    """

    # Required fields - must be provided when creating an instance
    sku: str
    name: str
    price: float
    quantity: int

    # Optional fields - have default values
    is_available: bool = True
    tags: list[str] = []
    description: str = ""

    def calculate_total_value(self) -> float:
        """Calculate the total value of products in stock.

        Returns:
            The product price multiplied by quantity in stock.
        """
        return self.price * self.quantity


def main() -> None:
    """Demonstrate the Product model."""
    # Create a product with required fields only
    print("=== Basic Product Creation ===")
    product = Product(
        sku="LAPTOP-001",
        name="Gaming Laptop",
        price=999.99,
        quantity=10,
    )

    print(f"Product: {product.name}")
    print(f"SKU: {product.sku}")
    print(f"Price: ${product.price}")
    print(f"In Stock: {product.quantity}")
    print(f"Available: {product.is_available}")  # Default: True
    print(f"Tags: {product.tags}")  # Default: []
    print(f"Total Value: ${product.calculate_total_value()}")
    print()

    # Create a product with all fields
    print("=== Product with All Fields ===")
    full_product = Product(
        sku="PHONE-002",
        name="Smartphone Pro",
        price=1299.99,
        quantity=25,
        is_available=True,
        tags=["electronics", "mobile", "premium"],
        description="Latest flagship smartphone with advanced camera",
    )
    print(f"Product: {full_product.name}")
    print(f"Tags: {full_product.tags}")
    print(f"Description: {full_product.description}")
    print()

    # Demonstrate type coercion
    print("=== Type Coercion ===")
    coerced_product = Product(
        sku="TABLET-001",
        name="Digital Tablet",
        price="499.99",  # String -> float
        quantity="15",  # String -> int
        is_available="true",  # String -> bool
    )
    print(
        f"Price: {coerced_product.price} (type: {type(coerced_product.price).__name__})"
    )
    print(
        f"Quantity: {coerced_product.quantity} (type: {type(coerced_product.quantity).__name__})"
    )
    print(
        f"Available: {coerced_product.is_available} (type: {type(coerced_product.is_available).__name__})"
    )
    print()

    # Convert to dictionary
    print("=== model_dump() ===")
    data = product.model_dump()
    print(f"Dictionary: {data}")
    print()

    # Create from dictionary
    print("=== Create from Dictionary ===")
    product_data = {
        "sku": "HEADPHONES-001",
        "name": "Wireless Headphones",
        "price": 199.99,
        "quantity": 50,
        "tags": ["audio", "wireless"],
    }
    from_dict = Product(**product_data)
    print(f"Created: {from_dict.name} - ${from_dict.price}")

    # Bonus: JSON serialization
    print()
    print("=== Bonus: JSON Serialization ===")
    json_str = product.model_dump_json(indent=2)
    print(json_str)


if __name__ == "__main__":
    main()
