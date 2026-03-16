"""Tests for Unit 1: Basic Models and Types."""

import pytest
from pydantic import ValidationError

from units.unit_01_basic_models.solution import Product


class TestProduct:
    """Tests for the Product model."""

    def test_create_product_with_required_fields(self):
        """Test creating a product with only required fields."""
        product = Product(
            sku="TEST-001",
            name="Test Product",
            price=99.99,
            quantity=10,
        )

        assert product.sku == "TEST-001"
        assert product.name == "Test Product"
        assert product.price == 99.99
        assert product.quantity == 10

    def test_default_values(self):
        """Test that optional fields have correct defaults."""
        product = Product(
            sku="TEST-001",
            name="Test Product",
            price=99.99,
            quantity=10,
        )

        assert product.is_available is True
        assert product.tags == []
        assert product.description == ""

    def test_create_product_with_all_fields(self):
        """Test creating a product with all fields specified."""
        product = Product(
            sku="FULL-001",
            name="Full Product",
            price=199.99,
            quantity=5,
            is_available=False,
            tags=["tag1", "tag2"],
            description="A complete product",
        )

        assert product.is_available is False
        assert product.tags == ["tag1", "tag2"]
        assert product.description == "A complete product"

    def test_type_coercion_string_to_float(self):
        """Test that string prices are coerced to float."""
        product = Product(
            sku="COERCE-001",
            name="Coerced Product",
            price="149.99",  # String
            quantity=1,
        )

        assert product.price == 149.99
        assert isinstance(product.price, float)

    def test_type_coercion_string_to_int(self):
        """Test that string quantities are coerced to int."""
        product = Product(
            sku="COERCE-002",
            name="Coerced Product",
            price=99.99,
            quantity="25",  # String
        )

        assert product.quantity == 25
        assert isinstance(product.quantity, int)

    def test_type_coercion_string_to_bool(self):
        """Test that string booleans are coerced to bool."""
        product = Product(
            sku="COERCE-003",
            name="Coerced Product",
            price=99.99,
            quantity=1,
            is_available="true",  # String
        )

        assert product.is_available is True
        assert isinstance(product.is_available, bool)

    def test_calculate_total_value(self):
        """Test the calculate_total_value method."""
        product = Product(
            sku="CALC-001",
            name="Calculator Test",
            price=25.00,
            quantity=4,
        )

        assert product.calculate_total_value() == 100.00

    def test_calculate_total_value_with_decimals(self):
        """Test calculate_total_value with decimal prices."""
        product = Product(
            sku="CALC-002",
            name="Decimal Test",
            price=19.99,
            quantity=3,
        )

        # Note: floating point arithmetic
        assert abs(product.calculate_total_value() - 59.97) < 0.01

    def test_model_dump(self):
        """Test converting model to dictionary."""
        product = Product(
            sku="DUMP-001",
            name="Dump Test",
            price=50.00,
            quantity=2,
            tags=["test"],
        )

        data = product.model_dump()

        assert isinstance(data, dict)
        assert data["sku"] == "DUMP-001"
        assert data["name"] == "Dump Test"
        assert data["price"] == 50.00
        assert data["quantity"] == 2
        assert data["tags"] == ["test"]
        assert data["is_available"] is True
        assert data["description"] == ""

    def test_create_from_dict(self):
        """Test creating a product from a dictionary."""
        data = {
            "sku": "DICT-001",
            "name": "From Dict",
            "price": 75.00,
            "quantity": 10,
        }

        product = Product(**data)

        assert product.sku == "DICT-001"
        assert product.name == "From Dict"

    def test_missing_required_field_raises_error(self):
        """Test that missing required fields raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Product(
                sku="MISSING-001",
                name="Missing Quantity",
                price=99.99,
                # quantity is missing
            )

        assert "quantity" in str(exc_info.value)

    def test_invalid_type_raises_error(self):
        """Test that invalid types raise ValidationError."""
        with pytest.raises(ValidationError):
            Product(
                sku="INVALID-001",
                name="Invalid Price",
                price="not a number",  # Invalid
                quantity=1,
            )
