"""Unit 1 Exercise: Create a Product Model.

Your task is to create a Pydantic model for an e-commerce product.

Instructions:
1. Complete the Product class below
2. Add all required fields with proper types
3. Implement the calculate_total_value() method
4. Run tests with: pytest units/01_basic_models/test_solution.py -v
"""

from pydantic import BaseModel


class Product(BaseModel):
    """E-commerce product model.

    TODO: Add the following fields:
    - sku: str (required) - Stock Keeping Unit identifier
    - name: str (required) - Product name
    - price: float (required) - Product price
    - quantity: int (required) - Items in stock
    - is_available: bool (optional, default True) - Whether product is available
    - tags: list[str] (optional, default []) - Product tags/categories
    - description: str (optional, default "") - Product description
    """

    # TODO: Add your fields here
    # Hint: Required fields have no default value
    # Example: name: str

    # TODO: Add optional fields with defaults
    # Hint: Optional fields have a default value
    # Example: is_active: bool = True

    pass  # Remove this line once you add fields

    def calculate_total_value(self) -> float:
        """Calculate the total value of products in stock.

        TODO: Implement this method
        Returns: price * quantity

        Hint: Access fields using self.field_name
        """
        # TODO: Implement this method
        pass


def main() -> None:
    """Test your implementation."""
    # Create a product
    product = Product(sku="LAPTOP-001", name="Gaming Laptop", price=999.99, quantity=10)

    print(f"Product: {product.name}")
    print(f"SKU: {product.sku}")
    print(f"Price: ${product.price}")
    print(f"In Stock: {product.quantity}")
    print(f"Available: {product.is_available}")
    print(f"Total Value: ${product.calculate_total_value()}")
    print()

    # Test type coercion
    product2 = Product(
        sku="PHONE-001",
        name="Smartphone",
        price="599.99",  # String -> float
        quantity="5",  # String -> int
    )
    print(f"Price type: {type(product2.price).__name__}")
    print(f"Quantity type: {type(product2.quantity).__name__}")
    print()

    # Convert to dictionary
    data = product.model_dump()
    print(f"As dictionary: {data}")
    print("Complete the Product model and uncomment the test code!")


if __name__ == "__main__":
    main()
