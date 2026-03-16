"""Unit 3 Example: Nested Models and Complex Types.

This example demonstrates a Company/Department/Employee hierarchy
using nested Pydantic models.
"""

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class Address(BaseModel):
    """Address model used in multiple places."""

    street: str
    city: str
    state: str = Field(min_length=2, max_length=2)
    zip_code: str = Field(pattern=r"^\d{5}$")
    country: str = "USA"


class Employee(BaseModel):
    """Employee model with address."""

    employee_id: str
    name: str
    email: str
    hire_date: date
    salary: float = Field(gt=0)
    address: Address  # Nested model
    skills: list[str] = []


class Department(BaseModel):
    """Department containing employees."""

    name: str
    code: str = Field(min_length=2, max_length=10)
    budget: float = Field(ge=0)
    employees: list[Employee] = []  # List of nested models
    manager: Employee | None = None  # Optional nested model


class Company(BaseModel):
    """Company with departments - top level of hierarchy."""

    name: str
    founded: int
    headquarters: Address
    departments: list[Department] = []

    def total_employees(self) -> int:
        """Count total employees across all departments."""
        return sum(len(dept.employees) for dept in self.departments)

    def total_budget(self) -> float:
        """Sum budgets across all departments."""
        return sum(dept.budget for dept in self.departments)


# Discriminated Union Example
class FullTimeContract(BaseModel):
    """Full-time employment contract."""

    contract_type: Literal["full_time"]
    annual_salary: float
    benefits_eligible: bool = True


class PartTimeContract(BaseModel):
    """Part-time employment contract."""

    contract_type: Literal["part_time"]
    hourly_rate: float
    hours_per_week: int = Field(gt=0, le=40)


class ContractorAgreement(BaseModel):
    """Contractor agreement."""

    contract_type: Literal["contractor"]
    daily_rate: float
    contract_end_date: date


class EmployeeWithContract(BaseModel):
    """Employee with discriminated union for contract type."""

    name: str
    contract: FullTimeContract | PartTimeContract | ContractorAgreement


def main() -> None:
    """Demonstrate nested models."""
    # Example 1: Building a company from nested data
    print("=== Example 1: Creating Nested Models ===")

    # Create employees
    alice = Employee(
        employee_id="EMP001",
        name="Alice Johnson",
        email="alice@company.com",
        hire_date=date(2020, 3, 15),
        salary=85000,
        address=Address(
            street="123 Main St",
            city="Boston",
            state="MA",
            zip_code="02101",
        ),
        skills=["Python", "SQL", "Leadership"],
    )

    bob = Employee(
        employee_id="EMP002",
        name="Bob Smith",
        email="bob@company.com",
        hire_date=date(2021, 6, 1),
        salary=75000,
        address=Address(
            street="456 Oak Ave",
            city="Cambridge",
            state="MA",
            zip_code="02139",
        ),
        skills=["JavaScript", "React"],
    )

    # Create department with employees
    engineering = Department(
        name="Engineering",
        code="ENG",
        budget=500000,
        employees=[alice, bob],
        manager=alice,
    )

    # Create company
    company = Company(
        name="Tech Corp",
        founded=2015,
        headquarters=Address(
            street="1 Tech Plaza",
            city="Boston",
            state="MA",
            zip_code="02110",
        ),
        departments=[engineering],
    )

    print(f"Company: {company.name}")
    print(f"Total Employees: {company.total_employees()}")
    print(f"Total Budget: ${company.total_budget():,.2f}")
    print()

    # Example 2: Creating from nested dictionaries
    print("=== Example 2: From Nested Dictionaries ===")

    company_data = {
        "name": "Startup Inc",
        "founded": 2022,
        "headquarters": {
            "street": "789 Innovation Way",
            "city": "San Francisco",
            "state": "CA",
            "zip_code": "94105",
        },
        "departments": [
            {
                "name": "Product",
                "code": "PROD",
                "budget": 200000,
                "employees": [
                    {
                        "employee_id": "EMP100",
                        "name": "Charlie Brown",
                        "email": "charlie@startup.com",
                        "hire_date": "2022-01-15",
                        "salary": 95000,
                        "address": {
                            "street": "100 Market St",
                            "city": "San Francisco",
                            "state": "CA",
                            "zip_code": "94103",
                        },
                    }
                ],
            }
        ],
    }

    startup = Company(**company_data)
    print(f"Company: {startup.name}")
    print(f"HQ City: {startup.headquarters.city}")
    print(f"First Employee: {startup.departments[0].employees[0].name}")
    print()

    # Example 3: Discriminated Unions
    print("=== Example 3: Discriminated Unions ===")

    full_timer = EmployeeWithContract(
        name="Diana Prince",
        contract=FullTimeContract(
            contract_type="full_time",
            annual_salary=90000,
        ),
    )

    part_timer = EmployeeWithContract(
        name="Peter Parker",
        contract=PartTimeContract(
            contract_type="part_time",
            hourly_rate=50,
            hours_per_week=20,
        ),
    )

    contractor = EmployeeWithContract(
        name="Bruce Wayne",
        contract=ContractorAgreement(
            contract_type="contractor",
            daily_rate=1000,
            contract_end_date=date(2024, 12, 31),
        ),
    )

    for emp in [full_timer, part_timer, contractor]:
        print(f"{emp.name}: {emp.contract.contract_type}")
        if isinstance(emp.contract, FullTimeContract):
            print(f"  Salary: ${emp.contract.annual_salary:,.2f}")
        elif isinstance(emp.contract, PartTimeContract):
            print(f"  Rate: ${emp.contract.hourly_rate}/hr")
        elif isinstance(emp.contract, ContractorAgreement):
            print(f"  Daily Rate: ${emp.contract.daily_rate}")
    print()

    # Example 4: model_dump with nested models
    print("=== Example 4: Serializing Nested Models ===")
    data = alice.model_dump()
    print(f"Employee dict keys: {list(data.keys())}")
    print(f"Address is dict: {isinstance(data['address'], dict)}")
    print(f"Address city: {data['address']['city']}")


if __name__ == "__main__":
    main()
