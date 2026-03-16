"""Unit 8 Solution: Meeting Notes Extraction System.

This is the complete solution for the meeting notes extraction exercise.
"""

import json
import os
import re
from typing import Generic, Literal, TypeVar

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

# Load .env file
load_dotenv()

# === Pydantic Models ===


class ActionItem(BaseModel):
    """An action item from the meeting."""

    task: str = Field(description="Description of the task")
    assignee: str = Field(description="Person responsible for the task")
    due_date: str | None = Field(default=None, description="Due date if mentioned")
    priority: Literal["low", "medium", "high"] | None = Field(
        default=None, description="Priority level"
    )


class Decision(BaseModel):
    """A decision made during the meeting."""

    topic: str = Field(description="What the decision was about")
    decision: str = Field(description="What was decided")
    rationale: str | None = Field(
        default=None, description="Why this decision was made"
    )


class Participant(BaseModel):
    """A meeting participant."""

    name: str = Field(description="Participant name")
    role: str | None = Field(default=None, description="Job title or role")


class MeetingNotes(BaseModel):
    """Structured meeting notes extracted from text."""

    title: str = Field(description="Meeting title")
    date: str | None = Field(default=None, description="Meeting date")
    participants: list[Participant] = Field(
        default_factory=list, description="Meeting attendees"
    )
    summary: str = Field(description="Brief meeting summary")
    key_points: list[str] = Field(
        default_factory=list, description="Main discussion points"
    )
    action_items: list[ActionItem] = Field(
        default_factory=list, description="Tasks to be done"
    )
    decisions: list[Decision] = Field(
        default_factory=list, description="Decisions made"
    )
    next_steps: list[str] = Field(
        default_factory=list, description="Planned follow-ups"
    )

    def to_markdown(self) -> str:
        """Export meeting notes as markdown."""
        lines = [f"# {self.title}"]

        if self.date:
            lines.append(f"\n**Date:** {self.date}")

        if self.participants:
            lines.append("\n## Participants")
            for p in self.participants:
                role = f" ({p.role})" if p.role else ""
                lines.append(f"- {p.name}{role}")

        lines.append("\n## Summary")
        lines.append(self.summary)

        if self.key_points:
            lines.append("\n## Key Points")
            for point in self.key_points:
                lines.append(f"- {point}")

        if self.action_items:
            lines.append("\n## Action Items")
            for item in self.action_items:
                priority = f" [{item.priority}]" if item.priority else ""
                due = f" (due: {item.due_date})" if item.due_date else ""
                lines.append(f"- [ ] {item.task} - **{item.assignee}**{priority}{due}")

        if self.decisions:
            lines.append("\n## Decisions")
            for d in self.decisions:
                lines.append(f"- **{d.topic}:** {d.decision}")
                if d.rationale:
                    lines.append(f"  - Rationale: {d.rationale}")

        if self.next_steps:
            lines.append("\n## Next Steps")
            for step in self.next_steps:
                lines.append(f"- {step}")

        return "\n".join(lines)


# === Generic Result Type ===

T = TypeVar("T", bound=BaseModel)


class ExtractionResult(BaseModel, Generic[T]):
    """Result of an extraction operation."""

    success: bool
    data: T | None = None
    error: str | None = None
    raw_response: str | None = None


# === Extraction Functions ===


def extract_meeting_notes(text: str) -> ExtractionResult[MeetingNotes]:
    """Extract meeting notes from text using Gemini.

    Args:
        text: Meeting notes or transcript text.

    Returns:
        ExtractionResult with MeetingNotes or error.
    """
    try:
        from google import genai

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return ExtractionResult(
                success=False,
                error="GEMINI_API_KEY not set. Please set it in environment or .env file.",
            )

        client = genai.Client(api_key=api_key)

        prompt = f"""Extract structured meeting information from the following notes.

Return a JSON object with these fields:
- title (string): Meeting title or subject
- date (string or null): Meeting date if mentioned
- participants (array): List of {{name, role}} objects
- summary (string): 2-3 sentence summary of the meeting
- key_points (array of strings): Main topics or points discussed
- action_items (array): List of {{task, assignee, due_date, priority}} objects
  - priority should be "low", "medium", or "high" if determinable
- decisions (array): List of {{topic, decision, rationale}} objects
- next_steps (array of strings): Follow-up actions or plans

Meeting notes to extract from:
{text}

Return ONLY valid JSON, no additional text or markdown."""

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": MeetingNotes,
            },
        )

        raw_text = response.text
        data = json.loads(raw_text)
        notes = MeetingNotes.model_validate(data)

        return ExtractionResult(
            success=True,
            data=notes,
            raw_response=raw_text,
        )

    except ImportError:
        return ExtractionResult(
            success=False,
            error="google-genai not installed. Run: pip install google-genai",
        )
    except json.JSONDecodeError as e:
        return ExtractionResult(
            success=False,
            error=f"Invalid JSON response: {e}",
        )
    except ValidationError as e:
        return ExtractionResult(
            success=False,
            error=f"Response validation failed: {e}",
        )
    except Exception as e:
        return ExtractionResult(
            success=False,
            error=f"API error: {e}",
        )


def extract_meeting_notes_mock(text: str) -> ExtractionResult[MeetingNotes]:
    """Mock extraction for testing without API key.

    Parses meeting notes using simple text patterns.
    """
    lines = text.strip().split("\n")
    text_lower = text.lower()

    # Extract title (first non-empty line)
    title = "Team Meeting"
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith(("-", "*", "#")):
            title = stripped.split(" - ")[0].strip()
            break

    # Extract date
    date = None
    date_patterns = [
        r"(\w+ \d{1,2},? \d{4})",
        r"(\d{1,2}/\d{1,2}/\d{4})",
        r"(\d{4}-\d{2}-\d{2})",
    ]
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            date = match.group(1)
            break

    # Extract participants
    participants: list[Participant] = []
    attendee_section = False
    for line in lines:
        line_lower = line.lower()
        if "attendee" in line_lower or "participant" in line_lower:
            attendee_section = True
            # Parse inline attendees: "Attendees: Alice, Bob, Charlie"
            if ":" in line:
                names_part = line.split(":", 1)[1]
                for name_part in names_part.split(","):
                    name_part = name_part.strip()
                    if name_part:
                        # Extract role if in parentheses
                        role_match = re.match(r"([^(]+)\(([^)]+)\)", name_part)
                        if role_match:
                            participants.append(
                                Participant(
                                    name=role_match.group(1).strip(),
                                    role=role_match.group(2).strip(),
                                )
                            )
                        else:
                            participants.append(Participant(name=name_part))
            continue

    # Extract key points
    key_points: list[str] = []
    in_key_section = False
    for line in lines:
        line_lower = line.lower().strip()
        if "key point" in line_lower or "discussion" in line_lower:
            in_key_section = True
            continue
        if in_key_section:
            if line.strip().startswith("-") or line.strip().startswith("*"):
                point = line.strip().lstrip("-*").strip()
                if point:
                    key_points.append(point)
            elif line.strip() == "" or any(
                x in line_lower for x in ["action", "decision", "next step"]
            ):
                in_key_section = False

    # Extract action items
    action_items: list[ActionItem] = []
    in_action_section = False
    for line in lines:
        line_lower = line.lower().strip()
        if "action item" in line_lower:
            in_action_section = True
            continue
        if in_action_section:
            if line.strip().startswith("-") or line.strip().startswith("*"):
                item_text = line.strip().lstrip("-*").strip()
                if item_text:
                    # Try to extract assignee
                    assignee = "Unassigned"
                    assignee_match = re.search(r"(\w+) to ", item_text, re.IGNORECASE)
                    if assignee_match:
                        assignee = assignee_match.group(1)

                    # Check for priority
                    priority: Literal["low", "medium", "high"] | None = None
                    if "high priority" in item_text.lower():
                        priority = "high"
                    elif "low priority" in item_text.lower():
                        priority = "low"

                    # Check for due date
                    due_date = None
                    due_match = re.search(r"by (\w+ \d+|\d+/\d+)", item_text)
                    if due_match:
                        due_date = due_match.group(1)

                    action_items.append(
                        ActionItem(
                            task=item_text,
                            assignee=assignee,
                            due_date=due_date,
                            priority=priority,
                        )
                    )
            elif line.strip() == "" or any(
                x in line_lower for x in ["decision", "next step"]
            ):
                in_action_section = False

    # Extract decisions
    decisions: list[Decision] = []
    in_decision_section = False
    for line in lines:
        line_lower = line.lower().strip()
        if "decision" in line_lower:
            in_decision_section = True
            continue
        if in_decision_section:
            if line.strip().startswith("-") or line.strip().startswith("*"):
                decision_text = line.strip().lstrip("-*").strip()
                if decision_text:
                    # Try to split topic and decision
                    if " - " in decision_text:
                        parts = decision_text.split(" - ", 1)
                        decisions.append(Decision(topic=parts[0], decision=parts[1]))
                    else:
                        decisions.append(
                            Decision(topic="General", decision=decision_text)
                        )
            elif line.strip() == "" or "next step" in line_lower:
                in_decision_section = False

    # Extract next steps
    next_steps: list[str] = []
    in_next_section = False
    for line in lines:
        line_lower = line.lower().strip()
        if "next step" in line_lower:
            in_next_section = True
            continue
        if in_next_section:
            if line.strip().startswith("-") or line.strip().startswith("*"):
                step = line.strip().lstrip("-*").strip()
                if step:
                    next_steps.append(step)
            elif line.strip() == "":
                in_next_section = False

    # Generate summary
    summary_parts = []
    if title:
        summary_parts.append(f"Meeting: {title}.")
    if participants:
        summary_parts.append(f"{len(participants)} participants attended.")
    if action_items:
        summary_parts.append(f"{len(action_items)} action items were assigned.")
    if decisions:
        summary_parts.append(f"{len(decisions)} decisions were made.")
    summary = " ".join(summary_parts) if summary_parts else "Meeting notes processed."

    mock_data = {
        "title": title,
        "date": date,
        "participants": [p.model_dump() for p in participants],
        "summary": summary,
        "key_points": key_points,
        "action_items": [a.model_dump() for a in action_items],
        "decisions": [d.model_dump() for d in decisions],
        "next_steps": next_steps,
    }

    try:
        notes = MeetingNotes.model_validate(mock_data)
        return ExtractionResult(
            success=True,
            data=notes,
            raw_response=json.dumps(mock_data, indent=2),
        )
    except ValidationError as e:
        return ExtractionResult(
            success=False,
            error=f"Validation error: {e}",
        )


def main() -> None:
    """Demonstrate meeting notes extraction."""
    sample_meeting = """
Product Planning Meeting - March 15, 2024

Attendees: Sarah (PM), John (Dev Lead), Alice (Designer), Bob (QA)

We met to discuss the Q2 roadmap and prioritize features for the next release.
The team reviewed current progress and identified blockers.

Key Discussion Points:
- Mobile app redesign is the top priority for Q2
- We need to hire 2 more developers to meet deadlines
- Budget has been approved for new development tools
- Customer feedback indicates need for better performance

Action Items:
- John to create technical specification by March 20 (high priority)
- Alice to prepare UI mockups for stakeholder review
- Sarah to schedule stakeholder review meeting by March 18
- Bob to set up automated testing pipeline

Decisions Made:
- Chose React Native for mobile development - better cross-platform support
- Delayed the analytics feature to Q3 - resource constraints
- Approved new CI/CD tooling budget - improves deployment speed

Next Steps:
- Weekly sync meetings starting next Monday
- All specifications due by end of month
- Beta release targeted for April 15
"""

    print("=" * 60)
    print("Meeting Notes Extraction Demo")
    print("=" * 60)

    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        print("\nUsing Gemini API for extraction...")
        result = extract_meeting_notes(sample_meeting)
    else:
        print("\nUsing mock extraction (no API key found)...")
        print("Set GEMINI_API_KEY to use real Gemini API.\n")
        result = extract_meeting_notes_mock(sample_meeting)

    if result.success and result.data:
        notes = result.data

        print(f"\n{'=' * 40}")
        print("EXTRACTED MEETING NOTES")
        print(f"{'=' * 40}")

        print(f"\nTitle: {notes.title}")
        print(f"Date: {notes.date or 'Not specified'}")
        print(f"Summary: {notes.summary}")

        print(f"\nParticipants ({len(notes.participants)}):")
        for p in notes.participants:
            role = f" - {p.role}" if p.role else ""
            print(f"  - {p.name}{role}")

        print(f"\nKey Points ({len(notes.key_points)}):")
        for point in notes.key_points:
            print(f"  - {point}")

        print(f"\nAction Items ({len(notes.action_items)}):")
        for item in notes.action_items:
            priority = f" [{item.priority}]" if item.priority else ""
            due = f" (due: {item.due_date})" if item.due_date else ""
            print(f"  - {item.task}")
            print(f"    Assignee: {item.assignee}{priority}{due}")

        print(f"\nDecisions ({len(notes.decisions)}):")
        for d in notes.decisions:
            print(f"  - {d.topic}: {d.decision}")
            if d.rationale:
                print(f"    Rationale: {d.rationale}")

        print(f"\nNext Steps ({len(notes.next_steps)}):")
        for step in notes.next_steps:
            print(f"  - {step}")

        # Demonstrate markdown export
        print(f"\n{'=' * 40}")
        print("MARKDOWN EXPORT")
        print(f"{'=' * 40}")
        print(notes.to_markdown())

    else:
        print(f"\nExtraction failed: {result.error}")


if __name__ == "__main__":
    main()
