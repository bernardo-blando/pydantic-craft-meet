"""Unit 8 Solution: Meeting Notes Extraction System.

This is the complete solution for the meeting notes extraction exercise.
"""

import json
import os
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

    print("\nExtracting meeting notes using Gemini API...")
    result = extract_meeting_notes(sample_meeting)

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
