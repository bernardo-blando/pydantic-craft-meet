"""Tests for Unit 8: Gemini Structured Outputs.

These tests use mock extraction and don't require an API key.
"""

import pytest

from units.unit_08_gemini_structured_outputs.solution import (
    ActionItem,
    Decision,
    ExtractionResult,
    MeetingNotes,
    Participant,
    extract_meeting_notes_mock,
)


class TestModels:
    """Tests for the Pydantic models."""

    def test_action_item_creation(self):
        """Test creating an action item."""
        item = ActionItem(
            task="Complete the report",
            assignee="John",
            due_date="March 20",
            priority="high",
        )

        assert item.task == "Complete the report"
        assert item.assignee == "John"
        assert item.priority == "high"

    def test_action_item_defaults(self):
        """Test action item default values."""
        item = ActionItem(task="Do something", assignee="Someone")

        assert item.due_date is None
        assert item.priority is None

    def test_decision_creation(self):
        """Test creating a decision."""
        decision = Decision(
            topic="Technology choice",
            decision="Use React Native",
            rationale="Better cross-platform support",
        )

        assert decision.topic == "Technology choice"
        assert decision.decision == "Use React Native"
        assert decision.rationale == "Better cross-platform support"

    def test_participant_creation(self):
        """Test creating a participant."""
        participant = Participant(name="Alice", role="Project Manager")

        assert participant.name == "Alice"
        assert participant.role == "Project Manager"

    def test_participant_without_role(self):
        """Test participant with no role."""
        participant = Participant(name="Bob")

        assert participant.name == "Bob"
        assert participant.role is None

    def test_meeting_notes_creation(self):
        """Test creating meeting notes."""
        notes = MeetingNotes(
            title="Sprint Planning",
            date="2024-03-15",
            summary="Planned next sprint",
            participants=[Participant(name="Alice", role="PM")],
            key_points=["Review backlog", "Estimate stories"],
            action_items=[ActionItem(task="Create tickets", assignee="Bob")],
            decisions=[Decision(topic="Sprint length", decision="2 weeks")],
            next_steps=["Start sprint Monday"],
        )

        assert notes.title == "Sprint Planning"
        assert len(notes.participants) == 1
        assert len(notes.action_items) == 1

    def test_meeting_notes_defaults(self):
        """Test meeting notes default values."""
        notes = MeetingNotes(
            title="Quick Sync",
            summary="Brief team sync",
        )

        assert notes.date is None
        assert notes.participants == []
        assert notes.key_points == []
        assert notes.action_items == []
        assert notes.decisions == []
        assert notes.next_steps == []


class TestMeetingNotesMarkdown:
    """Tests for markdown export."""

    def test_to_markdown_basic(self):
        """Test basic markdown export."""
        notes = MeetingNotes(
            title="Test Meeting",
            summary="A test meeting",
        )

        md = notes.to_markdown()

        assert "# Test Meeting" in md
        assert "A test meeting" in md

    def test_to_markdown_with_participants(self):
        """Test markdown with participants."""
        notes = MeetingNotes(
            title="Test Meeting",
            summary="Summary",
            participants=[
                Participant(name="Alice", role="PM"),
                Participant(name="Bob"),
            ],
        )

        md = notes.to_markdown()

        assert "## Participants" in md
        assert "Alice (PM)" in md
        assert "- Bob" in md

    def test_to_markdown_with_action_items(self):
        """Test markdown with action items."""
        notes = MeetingNotes(
            title="Test Meeting",
            summary="Summary",
            action_items=[
                ActionItem(
                    task="Complete report",
                    assignee="John",
                    priority="high",
                    due_date="March 20",
                )
            ],
        )

        md = notes.to_markdown()

        assert "## Action Items" in md
        assert "Complete report" in md
        assert "**John**" in md
        assert "[high]" in md


class TestExtractionResult:
    """Tests for ExtractionResult."""

    def test_successful_result(self):
        """Test successful extraction result."""
        notes = MeetingNotes(title="Test", summary="Test summary")
        result = ExtractionResult[MeetingNotes](
            success=True,
            data=notes,
        )

        assert result.success is True
        assert result.data is not None
        assert result.data.title == "Test"

    def test_failed_result(self):
        """Test failed extraction result."""
        result = ExtractionResult[MeetingNotes](
            success=False,
            error="API error occurred",
        )

        assert result.success is False
        assert result.data is None
        assert result.error == "API error occurred"


class TestMockExtraction:
    """Tests for mock extraction function."""

    @pytest.fixture
    def sample_meeting_text(self):
        """Sample meeting text for testing."""
        return """
Product Planning Meeting - March 15, 2024

Attendees: Sarah (PM), John (Dev Lead), Alice (Designer)

We discussed the Q2 roadmap.

Key Discussion Points:
- Mobile app redesign is priority
- Need more developers

Action Items:
- John to create spec by March 20 (high priority)
- Alice to prepare mockups

Decisions Made:
- Chose React Native - cross-platform support
- Delayed analytics to Q3

Next Steps:
- Weekly syncs starting Monday
- Specs due end of month
"""

    def test_mock_extracts_title(self, sample_meeting_text):
        """Test that mock extraction gets the title."""
        result = extract_meeting_notes_mock(sample_meeting_text)

        assert result.success is True
        assert result.data is not None
        assert "Product Planning" in result.data.title

    def test_mock_extracts_date(self, sample_meeting_text):
        """Test that mock extraction gets the date."""
        result = extract_meeting_notes_mock(sample_meeting_text)

        assert result.success is True
        assert result.data is not None
        assert result.data.date is not None
        assert "March 15" in result.data.date or "2024" in result.data.date

    def test_mock_extracts_participants(self, sample_meeting_text):
        """Test that mock extraction gets participants."""
        result = extract_meeting_notes_mock(sample_meeting_text)

        assert result.success is True
        assert result.data is not None
        assert len(result.data.participants) > 0

        names = [p.name for p in result.data.participants]
        assert any("Sarah" in name for name in names)

    def test_mock_extracts_action_items(self, sample_meeting_text):
        """Test that mock extraction gets action items."""
        result = extract_meeting_notes_mock(sample_meeting_text)

        assert result.success is True
        assert result.data is not None
        assert len(result.data.action_items) > 0

    def test_mock_extracts_decisions(self, sample_meeting_text):
        """Test that mock extraction gets decisions."""
        result = extract_meeting_notes_mock(sample_meeting_text)

        assert result.success is True
        assert result.data is not None
        assert len(result.data.decisions) > 0

    def test_mock_extracts_next_steps(self, sample_meeting_text):
        """Test that mock extraction gets next steps."""
        result = extract_meeting_notes_mock(sample_meeting_text)

        assert result.success is True
        assert result.data is not None
        assert len(result.data.next_steps) > 0

    def test_mock_generates_summary(self, sample_meeting_text):
        """Test that mock extraction generates a summary."""
        result = extract_meeting_notes_mock(sample_meeting_text)

        assert result.success is True
        assert result.data is not None
        assert len(result.data.summary) > 0

    def test_mock_handles_minimal_input(self):
        """Test mock extraction with minimal input."""
        result = extract_meeting_notes_mock("Quick team sync")

        assert result.success is True
        assert result.data is not None
        assert result.data.title == "Quick team sync"

    def test_mock_returns_raw_response(self, sample_meeting_text):
        """Test that mock extraction includes raw response."""
        result = extract_meeting_notes_mock(sample_meeting_text)

        assert result.raw_response is not None
        # Raw response should be valid JSON
        import json

        parsed = json.loads(result.raw_response)
        assert "title" in parsed


class TestActionItemPriority:
    """Tests for action item priority extraction."""

    def test_high_priority_extraction(self):
        """Test extraction of high priority items."""
        text = """
Meeting

Action Items:
- Complete urgent task (high priority)
"""
        result = extract_meeting_notes_mock(text)

        assert result.success is True
        if result.data and result.data.action_items:
            priorities = [item.priority for item in result.data.action_items]
            assert "high" in priorities

    def test_low_priority_extraction(self):
        """Test extraction of low priority items."""
        text = """
Meeting

Action Items:
- Do when possible (low priority)
"""
        result = extract_meeting_notes_mock(text)

        assert result.success is True
        if result.data and result.data.action_items:
            priorities = [item.priority for item in result.data.action_items]
            assert "low" in priorities
