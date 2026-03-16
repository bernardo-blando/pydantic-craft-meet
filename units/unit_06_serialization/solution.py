"""Unit 6 Solution: AuditLog System.

This is the complete solution for the AuditLog system exercise.
Compare your solution with this one after completing the exercise.
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_serializer


class AuditAction(str, Enum):
    """Audit action types.

    Using str as a mixin allows the enum values to be
    easily serialized as strings.
    """

    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"


class AuditEntry(BaseModel):
    """Single audit log entry.

    Represents a single auditable action in the system,
    with custom serialization for timestamps and actions.
    """

    entry_id: str = Field(description="Unique entry identifier")
    action: AuditAction = Field(description="The action performed")
    resource_type: str = Field(description="Type of resource affected")
    resource_id: str = Field(description="ID of the affected resource")
    actor_id: str = Field(description="ID of user who performed action")
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="When the action occurred",
    )
    ip_address: str | None = Field(default=None, description="Client IP address")
    old_values: dict[str, Any] | None = Field(
        default=None, description="Previous values for updates"
    )
    new_values: dict[str, Any] | None = Field(
        default=None, description="New values for creates/updates"
    )
    success: bool = Field(default=True, description="Whether action succeeded")

    @field_serializer("timestamp")
    def serialize_timestamp(self, value: datetime) -> str:
        """Serialize timestamp to human-readable format."""
        return value.strftime("%Y-%m-%d %H:%M:%S")

    @field_serializer("action")
    def serialize_action(self, value: AuditAction) -> str:
        """Serialize action enum to lowercase string."""
        return value.value


class AuditLog(BaseModel):
    """Collection of audit entries for a service.

    Provides methods for managing entries and exporting
    in different formats.
    """

    log_id: str = Field(description="Unique log identifier")
    service_name: str = Field(description="Name of the service")
    entries: list[AuditEntry] = Field(
        default_factory=list, description="List of audit entries"
    )
    exported_at: datetime | None = Field(
        default=None, description="When the log was exported"
    )

    def add_entry(self, entry: AuditEntry) -> None:
        """Add an entry to the log.

        Args:
            entry: The audit entry to add.
        """
        self.entries.append(entry)

    def get_entries_by_action(self, action: AuditAction) -> list[AuditEntry]:
        """Get all entries with a specific action.

        Args:
            action: The action to filter by.

        Returns:
            List of entries matching the action.
        """
        return [entry for entry in self.entries if entry.action == action]

    def export_json(self, exclude_none: bool = True) -> str:
        """Export the log as a JSON string.

        Args:
            exclude_none: Whether to exclude None values.

        Returns:
            JSON string representation of the log.
        """
        return self.model_dump_json(indent=2, exclude_none=exclude_none)

    def export_summary(self) -> dict[str, Any]:
        """Export a summary with essential fields only.

        Returns:
            Dictionary with log_id, service_name, and simplified entries.
        """
        return {
            "log_id": self.log_id,
            "service_name": self.service_name,
            "entry_count": len(self.entries),
            "entries": [
                {
                    "entry_id": entry.entry_id,
                    "action": entry.action.value,
                    "resource_type": entry.resource_type,
                    "resource_id": entry.resource_id,
                    "timestamp": entry.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "success": entry.success,
                }
                for entry in self.entries
            ],
        }

    def entries_between(self, start: datetime, end: datetime) -> list[AuditEntry]:
        """Get entries within a time range.

        Args:
            start: Start of time range (inclusive).
            end: End of time range (inclusive).

        Returns:
            List of entries within the range.
        """
        return [entry for entry in self.entries if start <= entry.timestamp <= end]


def import_entry(data: dict[str, Any] | str) -> AuditEntry:
    """Parse an AuditEntry from dict or JSON string.

    Args:
        data: Either a dictionary or JSON string.

    Returns:
        Parsed AuditEntry instance.
    """
    if isinstance(data, str):
        return AuditEntry.model_validate_json(data)
    return AuditEntry.model_validate(data)


def import_log(data: dict[str, Any] | str) -> AuditLog:
    """Parse an AuditLog from dict or JSON string.

    Args:
        data: Either a dictionary or JSON string.

    Returns:
        Parsed AuditLog instance.
    """
    if isinstance(data, str):
        return AuditLog.model_validate_json(data)
    return AuditLog.model_validate(data)


def main() -> None:
    """Demonstrate the AuditLog system."""
    # Create entries
    print("=== Creating Entries ===")
    entry1 = AuditEntry(
        entry_id="aud-001",
        action=AuditAction.CREATE,
        resource_type="document",
        resource_id="doc-123",
        actor_id="user-456",
        ip_address="192.168.1.100",
        new_values={"title": "New Document", "content": "Hello World"},
    )

    entry2 = AuditEntry(
        entry_id="aud-002",
        action=AuditAction.UPDATE,
        resource_type="document",
        resource_id="doc-123",
        actor_id="user-456",
        old_values={"title": "New Document"},
        new_values={"title": "Updated Document"},
    )

    entry3 = AuditEntry(
        entry_id="aud-003",
        action=AuditAction.DELETE,
        resource_type="document",
        resource_id="doc-789",
        actor_id="admin-001",
        success=True,
    )

    print(f"Created {3} entries")
    print()

    # Show entry serialization
    print("=== Entry Serialization ===")
    print(entry1.model_dump_json(indent=2, exclude_none=True))
    print()

    # Create log and add entries
    print("=== Creating Log ===")
    log = AuditLog(log_id="log-001", service_name="document-service")
    log.add_entry(entry1)
    log.add_entry(entry2)
    log.add_entry(entry3)
    print(f"Log ID: {log.log_id}")
    print(f"Service: {log.service_name}")
    print(f"Entries: {len(log.entries)}")
    print()

    # Filter by action
    print("=== Filter by Action ===")
    creates = log.get_entries_by_action(AuditAction.CREATE)
    updates = log.get_entries_by_action(AuditAction.UPDATE)
    deletes = log.get_entries_by_action(AuditAction.DELETE)
    print(f"CREATE: {len(creates)}")
    print(f"UPDATE: {len(updates)}")
    print(f"DELETE: {len(deletes)}")
    print()

    # Export full JSON
    print("=== Full JSON Export ===")
    full_json = log.export_json(exclude_none=True)
    print(f"Length: {len(full_json)} chars")
    print(full_json[:300] + "...")
    print()

    # Export summary
    print("=== Summary Export ===")
    summary = log.export_summary()
    print(f"Log: {summary['log_id']}")
    print(f"Service: {summary['service_name']}")
    print(f"Entry count: {summary['entry_count']}")
    for entry in summary["entries"]:
        print(f"  - {entry['entry_id']}: {entry['action']} {entry['resource_type']}")
    print()

    # Import from JSON
    print("=== Import from JSON ===")
    json_data = """
    {
        "entry_id": "aud-100",
        "action": "login",
        "resource_type": "session",
        "resource_id": "sess-abc",
        "actor_id": "user-999",
        "ip_address": "10.0.0.1"
    }
    """
    imported_entry = import_entry(json_data)
    print(f"Imported: {imported_entry.entry_id}")
    print(f"Action: {imported_entry.action}")
    print(f"Type: {type(imported_entry.action)}")
    print()

    # Import from dict
    print("=== Import from Dict ===")
    dict_data = {
        "entry_id": "aud-101",
        "action": "logout",
        "resource_type": "session",
        "resource_id": "sess-abc",
        "actor_id": "user-999",
        "timestamp": "2024-01-15T10:30:00",
    }
    imported_from_dict = import_entry(dict_data)
    print(f"Imported: {imported_from_dict.entry_id}")
    print(f"Timestamp type: {type(imported_from_dict.timestamp)}")

    # Import full log
    print()
    print("=== Import Full Log ===")
    log_json = log.export_json()
    imported_log = import_log(log_json)
    print(f"Imported log: {imported_log.log_id}")
    print(f"Entries: {len(imported_log.entries)}")


if __name__ == "__main__":
    main()
