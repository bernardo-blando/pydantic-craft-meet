# Exercise 6: Create an AuditLog System

## Objective

Create an audit logging system with custom serialization for exporting logs to different formats.

## Requirements

### Part 1: Create Action Enum

Create an `AuditAction` enum with values:
- `CREATE`
- `READ`
- `UPDATE`
- `DELETE`
- `LOGIN`
- `LOGOUT`

### Part 2: Create AuditEntry Model

| Field | Type | Description |
|-------|------|-------------|
| `entry_id` | `str` | Unique entry identifier |
| `action` | `AuditAction` | The action performed |
| `resource_type` | `str` | Type of resource (e.g., "user", "document") |
| `resource_id` | `str` | ID of the affected resource |
| `actor_id` | `str` | ID of user who performed action |
| `timestamp` | `datetime` | When action occurred (default: now) |
| `ip_address` | `str | None` | Client IP address (default: None) |
| `old_values` | `dict[str, Any] | None` | Previous values (default: None) |
| `new_values` | `dict[str, Any] | None` | New values (default: None) |
| `success` | `bool` | Whether action succeeded (default: True) |

Custom serializers:
1. `timestamp` - serialize to "YYYY-MM-DD HH:MM:SS" format
2. `action` - serialize to lowercase string

### Part 3: Create AuditLog Model

| Field | Type | Description |
|-------|------|-------------|
| `log_id` | `str` | Unique log identifier |
| `service_name` | `str` | Name of the service |
| `entries` | `list[AuditEntry]` | List of audit entries (default: []) |
| `exported_at` | `datetime | None` | When log was exported (default: None) |

Methods to implement:
1. `add_entry(entry: AuditEntry) -> None` - Add an entry to the log
2. `get_entries_by_action(action: AuditAction) -> list[AuditEntry]` - Filter by action
3. `export_json(exclude_none: bool = True) -> str` - Export to JSON string
4. `export_summary() -> dict` - Export summary with only essential fields

### Part 4: Implement Import Functions

Create module-level functions:
1. `import_entry(data: dict | str) -> AuditEntry` - Parse from dict or JSON string
2. `import_log(data: dict | str) -> AuditLog` - Parse from dict or JSON string

## Steps

1. Open `exercise.py`
2. Complete all models and functions
3. Run tests with: `pytest units/unit_06_serialization/test_solution.py -v`

## Hints

### Enum with string values:
```python
from enum import Enum

class AuditAction(str, Enum):
    CREATE = "create"
    READ = "read"
```

### Custom serializer for datetime:
```python
@field_serializer("timestamp")
def serialize_timestamp(self, value: datetime) -> str:
    return value.strftime("%Y-%m-%d %H:%M:%S")
```

### Custom serializer for enum:
```python
@field_serializer("action")
def serialize_action(self, value: AuditAction) -> str:
    return value.value  # Returns the enum's string value
```

### Parsing from dict or JSON:
```python
def import_entry(data: dict | str) -> AuditEntry:
    if isinstance(data, str):
        return AuditEntry.model_validate_json(data)
    return AuditEntry.model_validate(data)
```

### Export summary (selective fields):
```python
def export_summary(self) -> dict:
    return self.model_dump(
        include={"log_id", "service_name", "entries"},
        # For nested models, specify which fields to include
    )
```

## Expected Behavior

```python
from datetime import datetime

# Create entries
entry1 = AuditEntry(
    entry_id="aud-001",
    action=AuditAction.CREATE,
    resource_type="document",
    resource_id="doc-123",
    actor_id="user-456",
    new_values={"title": "New Document"},
)

# Export entry to JSON
json_str = entry1.model_dump_json()
# timestamp is "YYYY-MM-DD HH:MM:SS" format
# action is lowercase "create"

# Create log and add entries
log = AuditLog(log_id="log-001", service_name="doc-service")
log.add_entry(entry1)

# Filter entries
creates = log.get_entries_by_action(AuditAction.CREATE)

# Export full log
full_json = log.export_json(exclude_none=True)

# Export summary
summary = log.export_summary()
# Only includes log_id, service_name, and essential entry info

# Import from JSON
imported = import_entry('{"entry_id": "...", ...}')
```

## Bonus Challenge

Add these features:
1. Method `entries_between(start: datetime, end: datetime) -> list[AuditEntry]`
2. Export to CSV format with `export_csv() -> str`
