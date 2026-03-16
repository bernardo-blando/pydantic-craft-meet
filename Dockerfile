# syntax=docker/dockerfile:1

FROM python:3.13-slim AS base

# Prevents Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Keeps Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1
# Default server port (can be overridden at runtime with -e PORT=xxxx)
ENV PORT=8000

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --frozen --no-dev --no-install-project

# Copy source code
COPY src/ ./src/

# Install the project
RUN uv sync --frozen --no-dev

# Expose port
EXPOSE 8000
CMD uv run fastapi run src/app/main.py --host 0.0.0.0 --port ${PORT}
