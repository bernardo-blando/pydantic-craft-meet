"""Tests for Unit 6: Serialization and Parsing."""

import json
from datetime import datetime

import pytest

from units.unit_06_serialization.solution import (
    AuditAction,
    AuditEntry,
    AuditLog,
    import_entry,
    import_log,
)


class TestAuditAction:
    """Tests for the AuditAction enum."""

    def test_all_actions_defined(self):
        """Test that all required actions are defined."""
        actions = [a.value for a in AuditAction]
        assert "create" in actions
        assert "read" in actions
        assert "update" in actions
        assert "delete" in actions
        assert "login" in actions
        assert "logout" in actions


class TestAuditEntry:
    """Tests for the AuditEntry model."""

    @pytest.fixture
    def sample_entry(self):
        """Create a sample entry for testing."""
        return AuditEntry(
            entry_id="aud-001",
            action=AuditAction.CREATE,
            resource_type="document",
            resource_id="doc-123",
            actor_id="user-456",
            timestamp=datetime(2024, 1, 15, 10, 30, 0),
            new_values={"title": "Test"},
        )

    def test_create_entry(self, sample_entry):
        """Test creating an audit entry."""
        assert sample_entry.entry_id == "aud-001"
        assert sample_entry.action == AuditAction.CREATE
        assert sample_entry.success is True  # Default

    def test_default_timestamp(self):
        """Test that timestamp defaults to now."""
        before = datetime.now()
        entry = AuditEntry(
            entry_id="aud-001",
            action=AuditAction.READ,
            resource_type="doc",
            resource_id="1",
            actor_id="user",
        )
        after = datetime.now()

        assert before <= entry.timestamp <= after

    def test_timestamp_serialization(self, sample_entry):
        """Test timestamp is serialized to expected format."""
        data = sample_entry.model_dump()
        assert data["timestamp"] == "2024-01-15 10:30:00"

    def test_action_serialization(self, sample_entry):
        """Test action is serialized to lowercase string."""
        data = sample_entry.model_dump()
        assert data["action"] == "create"

    def test_json_serialization(self, sample_entry):
        """Test JSON serialization."""
        json_str = sample_entry.model_dump_json()
        parsed = json.loads(json_str)

        assert parsed["entry_id"] == "aud-001"
        assert parsed["action"] == "create"
        assert parsed["timestamp"] == "2024-01-15 10:30:00"

    def test_exclude_none(self, sample_entry):
        """Test excluding None values."""
        data = sample_entry.model_dump(exclude_none=True)

        assert "new_values" in data
        assert "old_values" not in data
        assert "ip_address" not in data


class TestAuditLog:
    """Tests for the AuditLog model."""

    @pytest.fixture
    def sample_log(self):
        """Create a sample log with entries."""
        log = AuditLog(log_id="log-001", service_name="test-service")
        log.add_entry(
            AuditEntry(
                entry_id="e1",
                action=AuditAction.CREATE,
                resource_type="doc",
                resource_id="1",
                actor_id="user1",
            )
        )
        log.add_entry(
            AuditEntry(
                entry_id="e2",
                action=AuditAction.UPDATE,
                resource_type="doc",
                resource_id="1",
                actor_id="user1",
            )
        )
        log.add_entry(
            AuditEntry(
                entry_id="e3",
                action=AuditAction.CREATE,
                resource_type="doc",
                resource_id="2",
                actor_id="user2",
            )
        )
        return log

    def test_create_log(self):
        """Test creating an audit log."""
        log = AuditLog(log_id="log-001", service_name="my-service")

        assert log.log_id == "log-001"
        assert log.service_name == "my-service"
        assert log.entries == []
        assert log.exported_at is None

    def test_add_entry(self, sample_log):
        """Test adding entries to log."""
        assert len(sample_log.entries) == 3

    def test_get_entries_by_action(self, sample_log):
        """Test filtering entries by action."""
        creates = sample_log.get_entries_by_action(AuditAction.CREATE)
        updates = sample_log.get_entries_by_action(AuditAction.UPDATE)
        deletes = sample_log.get_entries_by_action(AuditAction.DELETE)

        assert len(creates) == 2
        assert len(updates) == 1
        assert len(deletes) == 0

    def test_export_json(self, sample_log):
        """Test JSON export."""
        json_str = sample_log.export_json()

        assert isinstance(json_str, str)
        parsed = json.loads(json_str)
        assert parsed["log_id"] == "log-001"
        assert len(parsed["entries"]) == 3

    def test_export_json_exclude_none(self, sample_log):
        """Test JSON export excludes None values."""
        json_str = sample_log.export_json(exclude_none=True)
        parsed = json.loads(json_str)

        # exported_at is None, should be excluded
        assert "exported_at" not in parsed

    def test_export_summary(self, sample_log):
        """Test summary export."""
        summary = sample_log.export_summary()

        assert summary["log_id"] == "log-001"
        assert summary["service_name"] == "test-service"
        assert summary["entry_count"] == 3
        assert len(summary["entries"]) == 3

        # Check entry structure
        entry = summary["entries"][0]
        assert "entry_id" in entry
        assert "action" in entry
        assert "resource_type" in entry
        assert "resource_id" in entry
        assert "timestamp" in entry
        # Should NOT include detailed values
        assert "old_values" not in entry
        assert "new_values" not in entry


class TestImportFunctions:
    """Tests for import functions."""

    def test_import_entry_from_dict(self):
        """Test importing entry from dictionary."""
        data = {
            "entry_id": "aud-001",
            "action": "create",
            "resource_type": "document",
            "resource_id": "doc-123",
            "actor_id": "user-456",
        }

        entry = import_entry(data)

        assert entry.entry_id == "aud-001"
        assert entry.action == AuditAction.CREATE
        assert isinstance(entry.timestamp, datetime)

    def test_import_entry_from_json(self):
        """Test importing entry from JSON string."""
        json_str = """
        {
            "entry_id": "aud-002",
            "action": "delete",
            "resource_type": "user",
            "resource_id": "user-999",
            "actor_id": "admin-001"
        }
        """

        entry = import_entry(json_str)

        assert entry.entry_id == "aud-002"
        assert entry.action == AuditAction.DELETE

    def test_import_log_from_dict(self):
        """Test importing log from dictionary."""
        data = {
            "log_id": "log-001",
            "service_name": "test-service",
            "entries": [
                {
                    "entry_id": "e1",
                    "action": "login",
                    "resource_type": "session",
                    "resource_id": "sess-1",
                    "actor_id": "user-1",
                }
            ],
        }

        log = import_log(data)

        assert log.log_id == "log-001"
        assert len(log.entries) == 1
        assert log.entries[0].action == AuditAction.LOGIN

    def test_import_log_from_json(self):
        """Test importing log from JSON string."""
        json_str = """
        {
            "log_id": "log-002",
            "service_name": "auth-service",
            "entries": []
        }
        """

        log = import_log(json_str)

        assert log.log_id == "log-002"
        assert log.service_name == "auth-service"
        assert log.entries == []

    def test_round_trip_serialization(self):
        """Test that export->import preserves data."""
        original = AuditLog(log_id="log-001", service_name="test")
        original.add_entry(
            AuditEntry(
                entry_id="e1",
                action=AuditAction.CREATE,
                resource_type="doc",
                resource_id="1",
                actor_id="user1",
                new_values={"key": "value"},
            )
        )

        # Export and import
        json_str = original.export_json(exclude_none=False)
        restored = import_log(json_str)

        assert restored.log_id == original.log_id
        assert restored.service_name == original.service_name
        assert len(restored.entries) == len(original.entries)
        assert restored.entries[0].entry_id == original.entries[0].entry_id
        assert restored.entries[0].action == original.entries[0].action
