"""Unit 6 Exercise: Create an AuditLog System.

Your task is to create an audit logging system with custom
serialization for different export formats.

Instructions:
1. Complete all models and functions below
2. Implement custom serializers
3. Run tests with: pytest units/06_serialization/test_solution.py -v
"""

from enum import Enum
from typing import Any

from pydantic import BaseModel


# Part 1: Create AuditAction enum
class AuditAction(str, Enum):
    """Audit action types.

    TODO: Add the following values:
    - CREATE = "create"
    - READ = "read"
    - UPDATE = "update"
    - DELETE = "delete"
    - LOGIN = "login"
    - LOGOUT = "logout"
    """

    # TODO: Add enum values
    pass


# Part 2: Create AuditEntry model
class AuditEntry(BaseModel):
    """Single audit log entry.

    TODO: Add these fields:
    - entry_id: str
    - action: AuditAction
    - resource_type: str
    - resource_id: str
    - actor_id: str
    - timestamp: datetime (default: now)
    - ip_address: str | None (default: None)
    - old_values: dict[str, Any] | None (default: None)
    - new_values: dict[str, Any] | None (default: None)
    - success: bool (default: True)

    TODO: Add custom serializers:
    1. timestamp -> "YYYY-MM-DD HH:MM:SS" format
    2. action -> lowercase string
    """

    # TODO: Add fields
    # entry_id: str
    # action: AuditAction
    # resource_type: str
    # resource_id: str
    # actor_id: str
    # timestamp: datetime = Field(default_factory=datetime.now)
    # ip_address: str | None = None
    # old_values: dict[str, Any] | None = None
    # new_values: dict[str, Any] | None = None
    # success: bool = True

    pass  # Remove this line once you add fields

    # TODO: Add timestamp serializer
    # @field_serializer("timestamp")
    # def serialize_timestamp(self, value: datetime) -> str:
    #     return value.strftime("%Y-%m-%d %H:%M:%S")

    # TODO: Add action serializer
    # @field_serializer("action")
    # def serialize_action(self, value: AuditAction) -> str:
    #     return value.value


# Part 3: Create AuditLog model
class AuditLog(BaseModel):
    """Collection of audit entries.

    TODO: Add these fields:
    - log_id: str
    - service_name: str
    - entries: list[AuditEntry] (default: [])
    - exported_at: datetime | None (default: None)

    TODO: Implement these methods:
    1. add_entry(entry: AuditEntry) -> None
    2. get_entries_by_action(action: AuditAction) -> list[AuditEntry]
    3. export_json(exclude_none: bool = True) -> str
    4. export_summary() -> dict
    """

    # TODO: Add fields
    # log_id: str
    # service_name: str
    # entries: list[AuditEntry] = []
    # exported_at: datetime | None = None

    pass  # Remove this line once you add fields

    def add_entry(self, entry: "AuditEntry") -> None:
        """Add an entry to the log.

        TODO: Implement this method
        Hint: self.entries.append(entry)
        """
        pass

    def get_entries_by_action(self, action: "AuditAction") -> list["AuditEntry"]:
        """Get all entries with a specific action.

        TODO: Implement this method
        Returns: List of entries matching the action
        """
        pass

    def export_json(self, exclude_none: bool = True) -> str:
        """Export the log as a JSON string.

        TODO: Implement this method
        Use model_dump_json() with exclude_none parameter
        """
        pass

    def export_summary(self) -> dict[str, Any]:
        """Export a summary with essential fields only.

        TODO: Implement this method
        Include: log_id, service_name, and for each entry:
        - entry_id, action, resource_type, resource_id, timestamp

        Hint: Use model_dump() with include parameter or build manually
        """
        pass


# Part 4: Import functions
def import_entry(data: dict[str, Any] | str) -> AuditEntry:
    """Parse an AuditEntry from dict or JSON string.

    TODO: Implement this function
    - If data is a string, use model_validate_json
    - If data is a dict, use model_validate
    """
    pass


def import_log(data: dict[str, Any] | str) -> AuditLog:
    """Parse an AuditLog from dict or JSON string.

    TODO: Implement this function
    - If data is a string, use model_validate_json
    - If data is a dict, use model_validate
    """
    pass


def main() -> None:
    """Test your implementation."""
    # TODO: Uncomment and test once you complete the models

    # # Create an entry
    # entry1 = AuditEntry(
    #     entry_id="aud-001",
    #     action=AuditAction.CREATE,
    #     resource_type="document",
    #     resource_id="doc-123",
    #     actor_id="user-456",
    #     new_values={"title": "New Document"},
    # )
    #
    # print("=== Entry Serialization ===")
    # print(entry1.model_dump_json(indent=2))
    # print()
    #
    # # Create a log
    # log = AuditLog(log_id="log-001", service_name="doc-service")
    # log.add_entry(entry1)
    # log.add_entry(
    #     AuditEntry(
    #         entry_id="aud-002",
    #         action=AuditAction.UPDATE,
    #         resource_type="document",
    #         resource_id="doc-123",
    #         actor_id="user-456",
    #         old_values={"title": "New Document"},
    #         new_values={"title": "Updated Document"},
    #     )
    # )
    #
    # print("=== Full Log Export ===")
    # print(log.export_json(exclude_none=True)[:200] + "...")
    # print()
    #
    # print("=== Summary Export ===")
    # summary = log.export_summary()
    # print(f"Log ID: {summary['log_id']}")
    # print(f"Entries: {len(summary['entries'])}")
    # print()
    #
    # print("=== Filter by Action ===")
    # creates = log.get_entries_by_action(AuditAction.CREATE)
    # print(f"CREATE actions: {len(creates)}")
    # print()
    #
    # print("=== Import from JSON ===")
    # json_data = '{"entry_id": "aud-003", "action": "delete", "resource_type": "document", "resource_id": "doc-999", "actor_id": "admin-1"}'
    # imported = import_entry(json_data)
    # print(f"Imported: {imported.entry_id} - {imported.action}")

    print("Complete the models and uncomment the test code!")


if __name__ == "__main__":
    main()
