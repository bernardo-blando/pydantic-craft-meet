"""Unit 8 Exercise: Meeting Notes Extraction System.

Your task is to create a system that extracts structured information
from meeting notes using Gemini and Pydantic models.

Prerequisites:
1. Set GEMINI_API_KEY environment variable (optional for mock)
2. Install: pip install google-genai

Run tests: pytest units/unit_08_gemini_structured_outputs/test_solution.py -v
"""

from typing import Generic, TypeVar

from pydantic import BaseModel

# === Part 1: Pydantic Models ===


class ActionItem(BaseModel):
    """An action item from the meeting.

    TODO: Add fields:
    - task: str - Description of the task
    - assignee: str - Person responsible
    - due_date: str | None - Due date if mentioned (default None)
    - priority: Literal["low", "medium", "high"] | None - Priority (default None)
    """

    # TODO: Add fields
    pass


class Decision(BaseModel):
    """A decision made during the meeting.

    TODO: Add fields:
    - topic: str - What the decision was about
    - decision: str - What was decided
    - rationale: str | None - Why this decision was made (default None)
    """

    # TODO: Add fields
    pass


class Participant(BaseModel):
    """A meeting participant.

    TODO: Add fields:
    - name: str - Participant name
    - role: str | None - Job title or role (default None)
    """

    # TODO: Add fields
    pass


class MeetingNotes(BaseModel):
    """Structured meeting notes extracted from text.

    TODO: Add fields:
    - title: str - Meeting title
    - date: str | None - Meeting date (default None)
    - participants: list[Participant] - Attendees (default [])
    - summary: str - Brief meeting summary
    - key_points: list[str] - Main discussion points (default [])
    - action_items: list[ActionItem] - Tasks to be done (default [])
    - decisions: list[Decision] - Decisions made (default [])
    - next_steps: list[str] - Planned follow-ups (default [])
    """

    # TODO: Add fields
    pass


# === Generic Result Type ===

T = TypeVar("T", bound=BaseModel)


class ExtractionResult(BaseModel, Generic[T]):
    """Result of an extraction operation."""

    success: bool
    data: T | None = None
    error: str | None = None
    raw_response: str | None = None


# === Part 2: Extraction Functions ===


def extract_meeting_notes(text: str) -> ExtractionResult[MeetingNotes]:
    """Extract meeting notes from text using Gemini.

    TODO: Implement this function:
    1. Configure Gemini with API key from environment
    2. Create a prompt for meeting extraction
    3. Call Gemini with response_schema=MeetingNotes
    4. Parse and validate the response
    5. Return ExtractionResult with data or error

    Args:
        text: Meeting notes or transcript text.

    Returns:
        ExtractionResult with MeetingNotes or error.
    """
    # TODO: Implement
    #
    # try:
    #     import google.generativeai as genai
    #
    #     api_key = os.getenv("GEMINI_API_KEY")
    #     if not api_key:
    #         return ExtractionResult(
    #             success=False,
    #             error="GEMINI_API_KEY not set"
    #         )
    #
    #     genai.configure(api_key=api_key)
    #     model = genai.GenerativeModel("gemini-1.5-flash")
    #
    #     prompt = f"""Extract meeting information from the following notes.
    #     Return a JSON object with: title, date, participants, summary,
    #     key_points, action_items, decisions, next_steps.
    #
    #     Meeting notes:
    #     {text}
    #     """
    #
    #     response = model.generate_content(
    #         prompt,
    #         generation_config=genai.GenerationConfig(
    #             response_mime_type="application/json",
    #             response_schema=MeetingNotes,
    #         ),
    #     )
    #
    #     data = json.loads(response.text)
    #     notes = MeetingNotes.model_validate(data)
    #
    #     return ExtractionResult(
    #         success=True,
    #         data=notes,
    #         raw_response=response.text,
    #     )
    #
    # except Exception as e:
    #     return ExtractionResult(success=False, error=str(e))

    pass


# === Part 3: Mock Extraction ===


def extract_meeting_notes_mock(text: str) -> ExtractionResult[MeetingNotes]:
    """Mock extraction for testing without API key.

    TODO: Implement basic text parsing to extract meeting info.
    This doesn't need to be sophisticated - just parse what you can.

    Hints:
    - Look for date patterns
    - Find names after "Attendees:" or similar
    - Look for "Action Items:" sections
    - Parse bullet points as key points
    """
    # TODO: Implement mock extraction
    #
    # lines = text.strip().split('\n')
    #
    # # Find title (first non-empty line)
    # title = "Team Meeting"
    # for line in lines:
    #     if line.strip():
    #         title = line.strip()
    #         break
    #
    # # Build mock data
    # mock_data = {
    #     "title": title,
    #     "summary": "Meeting discussed various topics.",
    #     "key_points": [],
    #     "participants": [],
    #     "action_items": [],
    #     "decisions": [],
    #     "next_steps": [],
    # }
    #
    # # ... parse more from text ...
    #
    # try:
    #     notes = MeetingNotes.model_validate(mock_data)
    #     return ExtractionResult(success=True, data=notes)
    # except ValidationError as e:
    #     return ExtractionResult(success=False, error=str(e))

    pass


def main() -> None:
    """Test your implementation."""
    sample_meeting = """
Product Planning Meeting - March 15, 2024

Attendees: Sarah (PM), John (Dev Lead), Alice (Designer)

We met to discuss the Q2 roadmap and prioritize features for the next release.

Key Discussion Points:
- Mobile app redesign is the top priority for Q2
- We need to hire 2 more developers to meet deadlines
- Budget has been approved for new development tools

Action Items:
- John to create technical specification by March 20 (high priority)
- Alice to prepare UI mockups for review
- Sarah to schedule stakeholder review meeting

Decisions Made:
- Chose React Native for mobile development (better cross-platform support)
- Delayed the analytics feature to Q3 (resource constraints)

Next Steps:
- Weekly sync meetings starting next Monday
- All specifications due by end of month
"""

    print("=" * 60)
    print("Meeting Notes Extraction Exercise")
    print("=" * 60)

    # TODO: Uncomment once you implement the functions

    # api_key = os.getenv("GEMINI_API_KEY")
    #
    # if api_key:
    #     print("\nUsing Gemini API...")
    #     result = extract_meeting_notes(sample_meeting)
    # else:
    #     print("\nUsing mock extraction (no API key)...")
    #     result = extract_meeting_notes_mock(sample_meeting)
    #
    # if result.success and result.data:
    #     notes = result.data
    #     print(f"\nTitle: {notes.title}")
    #     print(f"Date: {notes.date or 'Not specified'}")
    #     print(f"Summary: {notes.summary}")
    #     print(f"\nParticipants ({len(notes.participants)}):")
    #     for p in notes.participants:
    #         print(f"  - {p.name} ({p.role or 'No role'})")
    #     print(f"\nKey Points ({len(notes.key_points)}):")
    #     for point in notes.key_points:
    #         print(f"  - {point}")
    #     print(f"\nAction Items ({len(notes.action_items)}):")
    #     for item in notes.action_items:
    #         print(f"  - {item.task} (Assignee: {item.assignee})")
    #     print(f"\nDecisions ({len(notes.decisions)}):")
    #     for decision in notes.decisions:
    #         print(f"  - {decision.topic}: {decision.decision}")
    # else:
    #     print(f"\nExtraction failed: {result.error}")

    print("Complete the models and functions, then uncomment the test code!")


if __name__ == "__main__":
    main()
