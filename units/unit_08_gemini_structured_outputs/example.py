"""Unit 8 Example: Gemini Structured Outputs.

This example demonstrates extracting structured person information
from unstructured text using Gemini and Pydantic.

Prerequisites:
1. Set GEMINI_API_KEY environment variable or add to .env file
2. Install: pip install google-genai

Run with: make example8
"""

import json
import os
import re
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

# Load .env file
load_dotenv()

# === Pydantic Models for Structured Output ===


class Address(BaseModel):
    """Address information."""

    street: str | None = None
    city: str
    state: str | None = None
    country: str
    postal_code: str | None = None


class Person(BaseModel):
    """Person information extracted from text."""

    name: str = Field(description="Full name of the person")
    age: int | None = None
    occupation: str | None = None
    email: str | None = None
    phone: str | None = None
    address: Address | None = None
    skills: list[str] = Field(default_factory=list)
    summary: str = Field(description="Brief summary of the person")


class ExtractionResult(BaseModel):
    """Result of a text extraction operation."""

    success: bool
    data: Person | None = None
    error: str | None = None
    raw_response: str | None = None


def extract_person_with_gemini(text: str) -> ExtractionResult:
    """Extract person information from text using Gemini.

    Args:
        text: Unstructured text containing person information.

    Returns:
        ExtractionResult with the extracted Person or error information.
    """
    try:
        from google import genai

        # Get API key
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return ExtractionResult(
                success=False,
                error="GEMINI_API_KEY not set. Please set it in environment or .env file.",
            )

        # Create client
        client = genai.Client(api_key=api_key)

        # Create prompt
        prompt = f"""Extract person information from the following text.
Return a JSON object with these fields:
- name (string, required): Full name
- age (integer or null): Age in years
- occupation (string or null): Job or profession
- email (string or null): Email address
- phone (string or null): Phone number
- address (object or null): With city (required), country (required), street, state, postal_code
- skills (array of strings): List of skills mentioned
- summary (string, required): Brief 1-2 sentence summary

Text to extract from:
{text}

Return ONLY valid JSON, no additional text."""

        # Generate with structured output
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": Person,
            },
        )

        # Parse response
        raw_text = response.text
        data = json.loads(raw_text)
        person = Person.model_validate(data)

        return ExtractionResult(
            success=True,
            data=person,
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


def extract_person_mock(text: str) -> ExtractionResult:
    """Mock extraction for demonstration without API key.

    This simulates what Gemini would return for common inputs.
    """
    # Simple mock extraction based on keywords
    mock_data: dict[str, Any] = {
        "name": "Unknown",
        "summary": "Person mentioned in text",
        "skills": [],
    }

    text_lower = text.lower()

    # Extract name (simplified)
    if "john" in text_lower:
        mock_data["name"] = "John Smith"
    elif "alice" in text_lower:
        mock_data["name"] = "Alice Johnson"
    elif "sarah" in text_lower:
        mock_data["name"] = "Sarah Chen"

    # Extract age
    age_match = re.search(r"(\d+)[\s-]?year", text_lower)
    if age_match:
        mock_data["age"] = int(age_match.group(1))

    # Extract occupation
    occupations = ["engineer", "developer", "manager", "designer", "scientist"]
    for occ in occupations:
        if occ in text_lower:
            mock_data["occupation"] = occ.title()
            break

    # Extract skills
    skills = ["python", "javascript", "java", "machine learning", "data science"]
    mock_data["skills"] = [s.title() for s in skills if s in text_lower]

    # Extract location
    if "san francisco" in text_lower:
        mock_data["address"] = {
            "city": "San Francisco",
            "country": "USA",
            "state": "California",
        }
    elif "new york" in text_lower:
        mock_data["address"] = {
            "city": "New York",
            "country": "USA",
            "state": "New York",
        }
    elif "london" in text_lower:
        mock_data["address"] = {"city": "London", "country": "UK"}

    # Generate summary
    parts = []
    if mock_data.get("occupation"):
        parts.append(f"A {mock_data['occupation'].lower()}")
    if mock_data.get("age"):
        parts.append(f"aged {mock_data['age']}")
    if mock_data.get("address"):
        parts.append(f"based in {mock_data['address']['city']}")
    mock_data["summary"] = " ".join(parts) if parts else "Person mentioned in text"

    try:
        person = Person.model_validate(mock_data)
        return ExtractionResult(
            success=True,
            data=person,
            raw_response=json.dumps(mock_data, indent=2),
        )
    except ValidationError as e:
        return ExtractionResult(
            success=False,
            error=f"Mock data validation failed: {e}",
        )


def main() -> None:
    """Demonstrate Gemini structured outputs."""
    # Sample texts to extract from
    sample_texts = [
        """
        John Smith is a 32-year-old software engineer working at TechCorp in
        San Francisco. He specializes in Python and machine learning, with
        over 8 years of experience. You can reach him at john.smith@email.com
        or call (555) 123-4567.
        """,
        """
        Meet Alice Johnson, a senior product manager based in New York City.
        At 28, she has already led multiple successful product launches.
        Alice is known for her expertise in agile methodologies and user research.
        Contact: alice.j@company.io
        """,
        """
        Dr. Sarah Chen, 45, is a renowned data scientist and researcher at
        Stanford University. Her work focuses on machine learning applications
        in healthcare. She has published over 50 papers and holds 3 patents.
        Sarah lives in Palo Alto, California.
        """,
    ]

    print("=" * 60)
    print("Gemini Structured Output Demo")
    print("=" * 60)

    # Check for API key
    api_key = os.getenv("GEMINI_API_KEY")
    use_mock = not api_key

    if use_mock:
        print("\nNote: GEMINI_API_KEY not found. Using mock extraction.")
        print("Set GEMINI_API_KEY to use real Gemini API.\n")
        extract_func = extract_person_mock
    else:
        print("\nUsing Gemini API for extraction.\n")
        extract_func = extract_person_with_gemini

    for i, text in enumerate(sample_texts, 1):
        print(f"\n--- Sample {i} ---")
        print(f"Input text: {text[:80].strip()}...")

        result = extract_func(text)

        if result.success and result.data:
            print("\nExtracted Person:")
            print(f"  Name: {result.data.name}")
            print(f"  Age: {result.data.age or 'Not specified'}")
            print(f"  Occupation: {result.data.occupation or 'Not specified'}")
            print(f"  Email: {result.data.email or 'Not specified'}")
            if result.data.address:
                print(
                    f"  Location: {result.data.address.city}, {result.data.address.country}"
                )
            print(
                f"  Skills: {', '.join(result.data.skills) if result.data.skills else 'None listed'}"
            )
            print(f"  Summary: {result.data.summary}")
        else:
            print(f"\nExtraction failed: {result.error}")

        print("-" * 40)

    # Demonstrate model serialization
    print("\n=== Model Serialization ===")
    sample_person = Person(
        name="Demo User",
        age=30,
        occupation="Developer",
        skills=["Python", "FastAPI"],
        summary="A developer demonstrating Pydantic models",
    )
    print(f"JSON output:\n{sample_person.model_dump_json(indent=2)}")


if __name__ == "__main__":
    main()
