# Coding Standards

This document outlines the coding standards and best practices for this project.

## Code Style

### General

- **Line length**: 88 characters (Black/Ruff default)
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Double quotes for strings
- **Imports**: Sorted by isort (via Ruff)

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Modules | `snake_case` | `user_service.py` |
| Classes | `PascalCase` | `UserService` |
| Functions | `snake_case` | `get_user_by_id` |
| Variables | `snake_case` | `user_count` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| Private | `_leading_underscore` | `_internal_method` |

### Type Hints

All code should include type hints:

```python
# Good
def get_user(user_id: int) -> User | None:
    ...

# Bad
def get_user(user_id):
    ...
```

**Exceptions:**
- Test functions may omit return type hints
- Lambda functions (when obvious)

## Architecture

### Separation of Concerns

1. **Business logic** (e.g., `pydantic_craft_meet/`) should have NO framework dependencies
2. **App layer** (e.g., `app/`) depends on business logic, not vice versa
3. Keep modules focused and single-purpose
4. Prefer composition over inheritance

## Testing

### Structure

- Mirror the source structure in tests
- One test file per module
- Use descriptive test names

```python
# Good
def test_get_user_returns_none_when_not_found():
    ...

# Bad
def test_get_user():
    ...
```

### Coverage

- All new features must include tests
- Critical paths should have integration tests

### Fixtures

- Define shared fixtures in `conftest.py`
- Use factory fixtures for complex objects
- Prefer fixtures over setup/teardown

## Git

### Branch Prefixes

| Type | Description |
|------|-------------|
| `feature` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `refactor` | Code refactoring |


### Commit Examples

```
added user registration endpoint

- Add POST /users endpoint
- Add email validation
- Add password hashing

Closes #123
```

```
handle empty user list in pagination

Previously, requesting page 2 with no users would raise
IndexError. Now returns empty list with correct metadata.
```

### Guidelines

- First line max 72 characters
- Reference issues when applicable
- Explain **why**, not just **what**

## Pull Requests

### Checklist

Before opening a PR:

- [ ] All tests pass (`make test`)
- [ ] Linting passes (`make lint`)
- [ ] Code is formatted (`make format`)
- [ ] New code has tests
- [ ] Documentation updated if needed

### PR Description

Include:
1. **What** - Brief description of changes
2. **Why** - Motivation for the change
3. **How** - Implementation approach (if complex)
4. **Testing** - How to test the changes

## Error Handling

### Guidelines

- Use specific exceptions over generic ones
- Document exceptions in docstrings
- Log errors with context
- Return meaningful error responses in API

```python
# Good
class UserNotFoundError(Exception):
    """Raised when a user is not found in the database."""

def get_user(user_id: int) -> User:
    """
    Fetch a user by ID.

    Raises:
        UserNotFoundError: If no user exists with the given ID.
    """
    user = db.get(user_id)
    if not user:
        raise UserNotFoundError(f"User {user_id} not found")
    return user
```

## Logging

- Use structured logging
- Include relevant context
- Use appropriate log levels:
  - `DEBUG`: Detailed diagnostic information
  - `INFO`: General operational messages
  - `WARNING`: Something unexpected but not critical
  - `ERROR`: Something failed
  - `CRITICAL`: System is unusable

## Security

- Never commit secrets or credentials
- Use environment variables for configuration
- Validate all external input
- Use parameterized queries (no SQL string building)
- Keep dependencies updated

## Dependencies

- Pin major versions in `pyproject.toml`
- Review security advisories regularly
- Document why each dependency is needed
- Prefer well-maintained packages

---

## Quick Reference

```bash
# Before committing
make format    # Format code
make lint      # Check for issues
make test      # Run tests

# Full check (CI equivalent)
make all       # lint + test
```
