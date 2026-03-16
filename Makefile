.PHONY: all install setup test testcov lint format clean help
.PHONY: example1 example2 example3 example4 example5 example6 example7 example8
.PHONY: solution1 solution2 solution3 solution4 solution5 solution6 solution7 solution8
.PHONY: test1 test2 test3 test4 test5 test6 test7 test8
.PHONY: run-api

# Default target
all: lint test

# =============================================================================
# Installation
# =============================================================================

install:
	uv sync

setup:
	uv sync --all-extras
	uv run pre-commit install

# =============================================================================
# Testing
# =============================================================================

test:
	uv run pytest

testcov:
	uv run pytest --cov=units --cov-report=term-missing --cov-report=xml

# Test individual units
test1:
	uv run pytest units/unit_01_basic_models/ -v

test2:
	uv run pytest units/unit_02_field_validation/ -v

test3:
	uv run pytest units/unit_03_nested_models/ -v

test4:
	uv run pytest units/unit_04_custom_validators/ -v

test5:
	uv run pytest units/unit_05_model_config/ -v

test6:
	uv run pytest units/unit_06_serialization/ -v

test7:
	uv run pytest units/unit_07_fastapi_integration/ -v

test8:
	uv run pytest units/unit_08_gemini_structured_outputs/ -v

# =============================================================================
# Run Examples
# =============================================================================

example1:
	uv run python -m units.unit_01_basic_models.example

example2:
	uv run python -m units.unit_02_field_validation.example

example3:
	uv run python -m units.unit_03_nested_models.example

example4:
	uv run python -m units.unit_04_custom_validators.example

example5:
	uv run python -m units.unit_05_model_config.example

example6:
	uv run python -m units.unit_06_serialization.example

example7:
	@echo "Unit 7 example is a FastAPI app. Use 'make run-api' to start it."

example8:
	@echo "Unit 8 requires GEMINI_API_KEY environment variable"
	uv run python -m units.unit_08_gemini_structured_outputs.example

# =============================================================================
# Run Solutions
# =============================================================================

solution1:
	uv run python -m units.unit_01_basic_models.solution

solution2:
	uv run python -m units.unit_02_field_validation.solution

solution3:
	uv run python -m units.unit_03_nested_models.solution

solution4:
	uv run python -m units.unit_04_custom_validators.solution

solution5:
	uv run python -m units.unit_05_model_config.solution

solution6:
	uv run python -m units.unit_06_serialization.solution

solution7:
	@echo "Unit 7 solution is a FastAPI app. Use 'make run-api' to start it."

solution8:
	@echo "Unit 8 requires GEMINI_API_KEY environment variable"
	uv run python -m units.unit_08_gemini_structured_outputs.solution

# =============================================================================
# FastAPI Server (Unit 7)
# =============================================================================

HOST ?= 127.0.0.1
PORT ?= 8000

run-api:
	uv run fastapi dev units/unit_07_fastapi_integration/example.py --host $(HOST) --port $(PORT)

# =============================================================================
# Code Quality
# =============================================================================

lint:
	uv run ruff check units
	uv run mypy units

format:
	uv run ruff format units
	uv run ruff check --fix units

# =============================================================================
# Maintenance
# =============================================================================

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov dist build
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

update:
	uv lock --upgrade

# =============================================================================
# Help
# =============================================================================

help:
	@echo "=== Installation ==="
	@echo "  make setup         - Install dependencies and pre-commit hooks"
	@echo ""
	@echo "=== Run Examples ==="
	@echo "  make example1     - Run Unit 1 example (Basic Models)"
	@echo "  make example2     - Run Unit 2 example (Field Validation)"
	@echo "  make example3     - Run Unit 3 example (Nested Models)"
	@echo "  make example4     - Run Unit 4 example (Custom Validators)"
	@echo "  make example5     - Run Unit 5 example (Model Config)"
	@echo "  make example6     - Run Unit 6 example (Serialization)"
	@echo "  make example7     - (see run-api)"
	@echo "  make example8     - Run Unit 8 example (Gemini - requires API key)"
	@echo ""
	@echo "=== Run Solutions ==="
	@echo "  make solution1    - Run Unit 1 solution"
	@echo "  make solution2    - Run Unit 2 solution"
	@echo "  make solution3    - Run Unit 3 solution"
	@echo "  make solution4    - Run Unit 4 solution"
	@echo "  make solution5    - Run Unit 5 solution"
	@echo "  make solution6    - Run Unit 6 solution"
	@echo "  make solution7    - (see run-api)"
	@echo "  make solution8    - Run Unit 8 solution (Gemini - requires API key)"
	@echo ""
	@echo "=== FastAPI (Unit 7) ==="
	@echo "  make run-api       - Start FastAPI server (default: http://127.0.0.1:8000)"
	@echo ""
	@echo "=== Testing ==="
	@echo "  make test          - Run all tests"
	@echo "  make test1        - Run Unit 1 tests"
	@echo "  make test2        - Run Unit 2 tests"
	@echo "  make test3        - Run Unit 3 tests"
	@echo "  make test4        - Run Unit 4 tests"
	@echo "  make test5        - Run Unit 5 tests"
	@echo "  make test6        - Run Unit 6 tests"
	@echo "  make test7        - Run Unit 7 tests"
	@echo "  make test8        - Run Unit 8 tests"
	@echo "  make testcov      - Run tests with coverage"
	@echo ""
	@echo "=== Code Quality ==="
	@echo "  make lint          - Run ruff and mypy"
	@echo "  make format        - Format code with ruff"
	@echo ""
	@echo "=== Maintenance ==="
	@echo "  make clean         - Remove generated files"
	@echo "  make all           - Run lint + test"
