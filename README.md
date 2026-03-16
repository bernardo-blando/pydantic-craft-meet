# Pydantic Craft Meet

A Python project generated from the boilerplate template

## Quick Start

```bash
git clone <repository-url>
cd pydantic-craft-meet

# Install dependencies
make setup

# Run the app
make run

# Run tests
make test
```

## Project Structure

```
src/
├── pydantic_craft_meet/    # Business logic (framework-agnostic)
└── app/                                # Fastapi application
tests/
├── test_core/                          # Business logic tests
└── test_app/                           # App tests
```

## Development

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) - Install with:
  ```bash
  # macOS/Linux
  curl -LsSf https://astral.sh/uv/install.sh | sh

  # Windows
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

### Commands

| Command | Description |
|---------|-------------|
| `make setup` | Install dependencies and pre-commit hooks |
| `make test` | Run tests |
| `make lint` | Run linting (ruff + mypy) |
| `make format` | Format code |
| `make run` | Start the application |
| `make docker-build` | Build Docker image |
| `make docker-run` | Run Docker container |

## Configuration

Environment variables (set in `.env` or environment):

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | `Pydantic Craft Meet` |
| `DEBUG` | Enable debug mode | `false` |
| `PORT` | Server port | `8000` |

## Docker

Build and run with Docker:

```bash
# Build the image
make docker-build

# Run the container
make docker-run
```

Or manually:

```bash
docker build -t pydantic-craft-meet .
docker run -p 8000:8000 pydantic-craft-meet
```

## Contributing

1. Create a feature branch
2. Make changes
3. Run `make all` (lint + test)
4. Open a Pull Request

See [standards.md](standards.md) for coding conventions.
