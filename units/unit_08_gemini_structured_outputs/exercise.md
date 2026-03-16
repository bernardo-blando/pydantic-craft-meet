# Exercise 8: Meeting Notes Extraction System

## Objective

Create a system that extracts structured information from meeting notes using Gemini and Pydantic models.

## Requirements

### Part 1: Create Pydantic Models

#### ActionItem Model
| Field | Type | Description |
|-------|------|-------------|
| `task` | `str` | Description of the task |
| `assignee` | `str` | Person responsible |
| `due_date` | `str \| None` | Due date if mentioned |
| `priority` | `Literal["low", "medium", "high"] \| None` | Priority level |

#### Decision Model
| Field | Type | Description |
|-------|------|-------------|
| `topic` | `str` | What the decision was about |
| `decision` | `str` | What was decided |
| `rationale` | `str \| None` | Why this decision was made |

#### Participant Model
| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Participant name |
| `role` | `str \| None` | Job title or role |

#### MeetingNotes Model
| Field | Type | Description |
|-------|------|-------------|
| `title` | `str` | Meeting title |
| `date` | `str \| None` | Meeting date |
| `participants` | `list[Participant]` | Meeting attendees |
| `summary` | `str` | Brief meeting summary |
| `key_points` | `list[str]` | Main discussion points |
| `action_items` | `list[ActionItem]` | Tasks to be done |
| `decisions` | `list[Decision]` | Decisions made |
| `next_steps` | `list[str]` | Planned follow-ups |

### Part 2: Create Extraction Function

Implement `extract_meeting_notes(text: str) -> ExtractionResult[MeetingNotes]`:

1. Takes meeting transcript/notes as input
2. Calls Gemini API with structured output schema
3. Returns extracted MeetingNotes or error information

### Part 3: Create Mock Function

Implement `extract_meeting_notes_mock(text: str) -> ExtractionResult[MeetingNotes]`:

1. Provides basic extraction without API calls
2. Useful for testing and development

## Steps

1. Open `exercise.py`
2. Complete all Pydantic models
3. Implement the extraction functions
4. Run tests with: `pytest units/unit_08_gemini_structured_outputs/test_solution.py -v`

## Hints

### Literal type for priority:
```python
from typing import Literal

priority: Literal["low", "medium", "high"] | None = None
```

### Creating the Gemini prompt:
```python
prompt = f"""Extract meeting information from the following notes.
Return a JSON object matching this structure:
- title: Meeting title/subject
- date: Meeting date if mentioned
- participants: List of {{name, role}}
- summary: 2-3 sentence summary
- key_points: Main topics discussed
- action_items: Tasks with {{task, assignee, due_date, priority}}
- decisions: Decisions with {{topic, decision, rationale}}
- next_steps: Follow-up actions

Meeting notes:
{text}
"""
```

### Gemini generation config:
```python
response = model.generate_content(
    prompt,
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema=MeetingNotes,
    ),
)
```

### Simple mock extraction:
```python
def extract_meeting_notes_mock(text: str) -> ExtractionResult[MeetingNotes]:
    # Parse key information from text
    lines = text.strip().split('\n')

    # Find title (usually first line or after "Meeting:")
    title = "Team Meeting"  # Default
    for line in lines:
        if line.strip():
            title = line.strip()
            break

    # Build mock data
    mock_data = {
        "title": title,
        "summary": "Meeting discussed team updates and next steps.",
        "key_points": ["Team updates", "Project status"],
        "participants": [],
        "action_items": [],
        "decisions": [],
        "next_steps": [],
    }

    # Parse for names, action items, etc.
    ...

    return ExtractionResult(success=True, data=MeetingNotes.model_validate(mock_data))
```

## Expected Behavior

```python
# Sample meeting notes
meeting_text = """
Product Planning Meeting - March 15, 2024

Attendees: Sarah (PM), John (Dev Lead), Alice (Designer)

Discussed Q2 roadmap and feature priorities.

Key Points:
- Mobile app redesign is top priority
- Need to hire 2 more developers
- Budget approved for new tools

Action Items:
- John to create technical spec by March 20
- Alice to prepare mockups (high priority)
- Sarah to schedule stakeholder review

Decisions:
- Chose React Native for mobile development
- Delayed the analytics feature to Q3

Next Steps:
- Weekly syncs starting next Monday
- All specs due by end of month
"""

result = extract_meeting_notes(meeting_text)

if result.success:
    notes = result.data
    print(f"Title: {notes.title}")
    print(f"Participants: {len(notes.participants)}")
    print(f"Action Items: {len(notes.action_items)}")
    print(f"Decisions: {len(notes.decisions)}")
```

## Bonus Challenge

1. Add confidence scores to extracted fields
2. Support extracting multiple meetings from a single document
3. Add export to markdown format with `to_markdown() -> str` method
