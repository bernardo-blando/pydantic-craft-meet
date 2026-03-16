# Exercise 1: Create a Product Model

## Objective

Create a Pydantic model for an e-commerce product that validates product information.

## Requirements

Create a `Product` model with the following fields:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `sku` | `str` | Yes | - | Stock Keeping Unit identifier |
| `name` | `str` | Yes | - | Product name |
| `price` | `float` | Yes | - | Product price |
| `quantity` | `int` | Yes | - | Items in stock |
| `is_available` | `bool` | No | `True` | Whether product is available |
| `tags` | `list[str]` | No | `[]` | Product tags/categories |
| `description` | `str` | No | `""` | Product description |

## Steps

1. Open `exercise.py`
2. Complete the `Product` class by adding the required fields
3. Implement the `calculate_total_value()` method
4. Run the tests with: `pytest units/unit_01_basic_models/test_solution.py -v`

## Hints

- Use Python type hints for each field (e.g., `name: str`)
- For optional fields with defaults, use `field: type = default_value`
- The `calculate_total_value()` method should return `price * quantity`

## Expected Behavior

```python
# Create a product
product = Product(
    sku="LAPTOP-001",
    name="Gaming Laptop",
    price=999.99,
    quantity=10
)

# Access fields
print(product.name)  # "Gaming Laptop"
print(product.is_available)  # True (default)

# Type coercion works
product2 = Product(
    sku="PHONE-001",
    name="Smartphone",
    price="599.99",  # String coerced to float
    quantity="5"  # String coerced to int
)

# Calculate total value
print(product.calculate_total_value())  # 9999.9

# Convert to dictionary
data = product.model_dump()
```

## Bonus Challenge

After completing the basic requirements, try:

1. Create a product from a dictionary
2. Print the product as JSON using `model_dump_json()`
