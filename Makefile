.PHONY: all install setup test test-cov lint format run clean help docker-build docker-run

HOST ?= 0.0.0.0
PORT ?= 8000

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

test-cov:
	uv run pytest --cov=src --cov-report=term-missing --cov-report=xml

# =============================================================================
# Code Quality
# =============================================================================

lint:
	uv run ruff check src tests
	uv run mypy src

format:
	uv run ruff format src tests
	uv run ruff check --fix src tests

# =============================================================================
# Run Application
# =============================================================================


run:
	uv run fastapi dev src/app/main.py --host $(HOST) --port $(PORT)


# =============================================================================
# Docker
# =============================================================================

docker-build:
	docker build -t pydantic-craft-meet .

docker-run:
	docker run -p $(PORT):$(PORT) -e PORT=$(PORT) pydantic-craft-meet

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
	@echo "make setup       - Install dependencies and pre-commit hooks"
	@echo "make test        - Run tests"
	@echo "make lint        - Run ruff and mypy"
	@echo "make format      - Format code"
	@echo "make run         - Start the application"
	@echo "make docker-build - Build Docker image"
	@echo "make docker-run  - Run Docker container"
	@echo "make clean       - Remove generated files"
	@echo "make all         - Run lint + test"
