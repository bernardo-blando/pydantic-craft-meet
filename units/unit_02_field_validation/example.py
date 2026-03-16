"""Unit 2 Example: Field Validation and Constraints.

This example demonstrates how to use Field() for validation
in an Employee model with salary ranges and other constraints.
"""

from pydantic import BaseModel, Field, ValidationError


class Employee(BaseModel):
    """Employee model with field validation.

    This model demonstrates various Field() constraints:
    - String length limits
    - Numeric ranges
    - Regex patterns
    - Optional fields
    """

    # Employee ID must match pattern: 2 letters followed by 4 digits
    employee_id: str = Field(
        pattern=r"^[A-Z]{2}\d{4}$",
        description="Employee ID (format: XX0000)",
        examples=["AB1234", "CD5678"],
    )

    # Name with length constraints
    name: str = Field(
        min_length=2,
        max_length=100,
        description="Employee's full name",
    )

    # Email with basic pattern validation
    email: str = Field(
        pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$",
        description="Work email address",
    )

    # Age must be between 18 and 100
    age: int = Field(
        ge=18,
        le=100,
        description="Employee age (must be 18+)",
    )

    # Salary with minimum value
    salary: float = Field(
        gt=0,
        description="Annual salary (must be positive)",
    )

    # Department with allowed values (basic enum-like validation)
    department: str = Field(
        min_length=1,
        max_length=50,
        description="Department name",
    )

    # Optional manager ID
    manager_id: str | None = Field(
        default=None,
        pattern=r"^[A-Z]{2}\d{4}$",
        description="Manager's employee ID (optional)",
    )

    # Years of experience (non-negative)
    years_experience: int = Field(
        default=0,
        ge=0,
        description="Years of professional experience",
    )


def main() -> None:
    """Demonstrate field validation."""
    # Example 1: Valid employee
    print("=== Example 1: Valid Employee ===")
    employee = Employee(
        employee_id="AB1234",
        name="Alice Johnson",
        email="alice.johnson@company.com",
        age=32,
        salary=85000.00,
        department="Engineering",
        manager_id="CD5678",
        years_experience=8,
    )
    print(f"Employee: {employee.name}")
    print(f"ID: {employee.employee_id}")
    print(f"Salary: ${employee.salary:,.2f}")
    print()

    # Example 2: Employee with defaults
    print("=== Example 2: Using Default Values ===")
    new_hire = Employee(
        employee_id="XY9999",
        name="Bob Smith",
        email="bob.smith@company.com",
        age=25,
        salary=55000.00,
        department="Marketing",
        # manager_id defaults to None
        # years_experience defaults to 0
    )
    print(f"Manager ID: {new_hire.manager_id}")  # None
    print(f"Experience: {new_hire.years_experience} years")  # 0
    print()

    # Example 3: Handling validation errors
    print("=== Example 3: Validation Errors ===")

    # Invalid employee ID format
    try:
        Employee(
            employee_id="invalid",  # Should be XX0000 format
            name="Test User",
            email="test@company.com",
            age=30,
            salary=50000,
            department="Test",
        )
    except ValidationError as e:
        print("Error 1 - Invalid employee_id:")
        for error in e.errors():
            print(f"  Field: {error['loc'][0]}")
            print(f"  Message: {error['msg']}")
        print()

    # Age too young
    try:
        Employee(
            employee_id="AA1111",
            name="Too Young",
            email="young@company.com",
            age=16,  # Must be >= 18
            salary=50000,
            department="Test",
        )
    except ValidationError as e:
        print("Error 2 - Age too low:")
        for error in e.errors():
            print(f"  Field: {error['loc'][0]}")
            print(f"  Message: {error['msg']}")
        print()

    # Negative salary
    try:
        Employee(
            employee_id="BB2222",
            name="Negative Salary",
            email="neg@company.com",
            age=30,
            salary=-1000,  # Must be > 0
            department="Test",
        )
    except ValidationError as e:
        print("Error 3 - Negative salary:")
        for error in e.errors():
            print(f"  Field: {error['loc'][0]}")
            print(f"  Message: {error['msg']}")
        print()

    # Name too short
    try:
        Employee(
            employee_id="CC3333",
            name="X",  # Must be >= 2 characters
            email="x@company.com",
            age=30,
            salary=50000,
            department="Test",
        )
    except ValidationError as e:
        print("Error 4 - Name too short:")
        for error in e.errors():
            print(f"  Field: {error['loc'][0]}")
            print(f"  Message: {error['msg']}")

    # Example 4: Multiple errors at once
    print()
    print("=== Example 4: Multiple Validation Errors ===")
    try:
        Employee(
            employee_id="bad",  # Invalid format
            name="A",  # Too short
            email="not-an-email",  # Invalid email
            age=10,  # Too young
            salary=-100,  # Negative
            department="",  # Too short
        )
    except ValidationError as e:
        print(f"Total errors: {len(e.errors())}")
        for error in e.errors():
            print(f"  - {error['loc'][0]}: {error['msg']}")


if __name__ == "__main__":
    main()
