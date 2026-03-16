"""Unit 6 Example: Serialization and Parsing.

This example demonstrates an event logging system with custom
datetime handling and various serialization options.
"""

import json
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_serializer


class EventLevel(str, Enum):
    """Event severity levels."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class EventMetadata(BaseModel):
    """Metadata attached to events."""

    source: str
    version: str = "1.0"
    tags: list[str] = []


class Event(BaseModel):
    """Event log entry with custom serialization."""

    event_id: str
    level: EventLevel = EventLevel.INFO
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: EventMetadata | None = None
    details: dict[str, Any] = {}

    @field_serializer("timestamp")
    def serialize_timestamp(self, value: datetime) -> str:
        """Serialize timestamp to ISO format with timezone."""
        return value.isoformat()

    @field_serializer("level")
    def serialize_level(self, value: EventLevel) -> str:
        """Serialize enum to uppercase string."""
        return value.value.upper()


class EventBatch(BaseModel):
    """Batch of events for bulk operations."""

    batch_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    events: list[Event] = []
    total_count: int = 0

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> int:
        """Serialize datetime as Unix timestamp."""
        return int(value.timestamp())


def main() -> None:
    """Demonstrate serialization and parsing."""
    # Example 1: Basic model_dump()
    print("=== Example 1: Basic Serialization ===")
    event = Event(
        event_id="evt-001",
        level=EventLevel.INFO,
        message="User logged in",
        metadata=EventMetadata(source="auth-service", tags=["auth", "login"]),
        details={"user_id": "user-123", "ip": "192.168.1.1"},
    )

    data = event.model_dump()
    print(f"Dictionary type: {type(data)}")
    print(f"Keys: {list(data.keys())}")
    print(f"Level (custom serialized): {data['level']}")
    print()

    # Example 2: JSON serialization
    print("=== Example 2: JSON Serialization ===")
    json_str = event.model_dump_json(indent=2)
    print(json_str)
    print()

    # Example 3: Parsing from dict
    print("=== Example 3: Parsing from Dictionary ===")
    event_data = {
        "event_id": "evt-002",
        "level": "warning",
        "message": "High memory usage detected",
        "timestamp": "2024-01-15T10:30:00",
        "details": {"memory_percent": 85.5},
    }
    parsed_event = Event.model_validate(event_data)
    print(f"Parsed event ID: {parsed_event.event_id}")
    print(f"Level type: {type(parsed_event.level)}")
    print(f"Timestamp type: {type(parsed_event.timestamp)}")
    print()

    # Example 4: Parsing from JSON
    print("=== Example 4: Parsing from JSON ===")
    json_input = """
    {
        "event_id": "evt-003",
        "level": "error",
        "message": "Database connection failed",
        "metadata": {
            "source": "db-service",
            "version": "2.0",
            "tags": ["database", "critical"]
        }
    }
    """
    parsed_from_json = Event.model_validate_json(json_input)
    print(f"Event: {parsed_from_json.message}")
    print(f"Source: {parsed_from_json.metadata.source}")
    print()

    # Example 5: Selective serialization
    print("=== Example 5: Selective Serialization ===")

    # Exclude fields
    minimal = event.model_dump(exclude={"details", "metadata"})
    print(f"Excluded: {list(minimal.keys())}")

    # Include only specific fields
    summary = event.model_dump(include={"event_id", "level", "message"})
    print(f"Included: {list(summary.keys())}")

    # Exclude None values
    event_no_meta = Event(event_id="evt-004", message="Simple event")
    with_none = event_no_meta.model_dump()
    without_none = event_no_meta.model_dump(exclude_none=True)
    print(f"With None - metadata: {with_none.get('metadata')}")
    print(f"Without None - has metadata: {'metadata' in without_none}")
    print()

    # Example 6: Nested exclusion
    print("=== Example 6: Nested Field Exclusion ===")
    nested_exclude = event.model_dump(
        exclude={"metadata": {"version", "tags"}, "details": True}
    )
    print(f"Metadata (version excluded): {nested_exclude.get('metadata')}")
    print(f"Details excluded: {'details' not in nested_exclude}")
    print()

    # Example 7: EventBatch with different timestamp format
    print("=== Example 7: Different Serialization for Same Type ===")
    batch = EventBatch(
        batch_id="batch-001",
        events=[
            Event(event_id="evt-010", message="Event 1"),
            Event(event_id="evt-011", message="Event 2"),
        ],
        total_count=2,
    )

    batch_data = batch.model_dump()
    print(f"Batch created_at (Unix timestamp): {batch_data['created_at']}")
    print(f"Event timestamp (ISO): {batch_data['events'][0]['timestamp']}")
    print()

    # Example 8: Round-trip serialization
    print("=== Example 8: Round-trip Serialization ===")
    original = Event(
        event_id="evt-100",
        level=EventLevel.CRITICAL,
        message="System failure",
        metadata=EventMetadata(source="monitoring", tags=["alert"]),
    )

    # Serialize to JSON
    json_output = original.model_dump_json()
    print(f"JSON: {json_output[:50]}...")

    # Parse back
    restored = Event.model_validate_json(json_output)
    print(f"Restored ID: {restored.event_id}")
    print(f"Restored level: {restored.level}")
    print(f"Types match: {type(original.level) == type(restored.level)}")

    # Example 9: Working with raw JSON
    print()
    print("=== Example 9: Integrating with json module ===")
    data = event.model_dump()
    # Can use with standard json module
    json_via_stdlib = json.dumps(data, indent=2)
    print(f"Via stdlib json: {json_via_stdlib[:50]}...")


if __name__ == "__main__":
    main()
