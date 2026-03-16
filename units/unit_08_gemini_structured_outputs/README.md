# Unit 8: Gemini Structured Outputs

## Learning Objectives

By the end of this unit, you will be able to:

- Use Gemini API to extract structured data from text
- Define Pydantic models as response schemas
- Handle API errors and validation gracefully
- Parse complex nested structures from natural language

## Key Concepts

### What is Structured Output?

Structured output allows you to get responses from LLMs in a specific format (like JSON) that matches a Pydantic model. This is useful for:

- Information extraction from text
- Data parsing and normalization
- Converting unstructured data to structured data

### Setting Up Gemini

```python
from google import genai

# Create client with your API key
client = genai.Client(api_key="your-api-key")
```

### Defining Response Schemas

You can use Pydantic models to define the expected response structure:

```python
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
    occupation: str

# Generate with response schema
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Extract person info from: John is a 30-year-old software engineer.",
    config={
        "response_mime_type": "application/json",
        "response_schema": Person,
    },
)
```

### Parsing the Response

```python
import json

# Parse the JSON response
data = json.loads(response.text)
person = Person.model_validate(data)
```

### Error Handling

```python
from pydantic import ValidationError

try:
    response = client.models.generate_content(...)
    data = json.loads(response.text)
    result = MyModel.model_validate(data)
except json.JSONDecodeError as e:
    print(f"Invalid JSON from Gemini: {e}")
except ValidationError as e:
    print(f"Response doesn't match schema: {e}")
except Exception as e:
    print(f"API error: {e}")
```

### Nested Models

```python
class Address(BaseModel):
    street: str
    city: str
    country: str

class Company(BaseModel):
    name: str
    address: Address
    employees: list[str]

# Gemini can extract nested structures
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Extract company info from the text...",
    config={
        "response_mime_type": "application/json",
        "response_schema": Company,
    },
)
```

### Best Practices

1. **Be specific in prompts** - The clearer your prompt, the better the extraction
2. **Handle missing data** - Use `| None` for fields that might not be present
3. **Validate always** - Always validate the response with Pydantic
4. **Add context** - Include examples in your prompt for complex extractions
5. **Use appropriate model** - `gemini-2.0-flash` for speed, `gemini-2.0-pro` for accuracy

## Prerequisites

1. Get a Gemini API key from https://aistudio.google.com/app/apikey
2. Create a `.env` file with: `GEMINI_API_KEY=your-key-here`
3. Install dependency: `pip install google-genai`

## Files in This Unit

- `example.py` - Person extraction from text
- `exercise.md` - Exercise description
- `exercise.py` - Starter code for meeting notes extraction
- `solution.py` - Complete solution
- `test_solution.py` - Tests (mock-based, no API key required)

## Running the Examples

```bash
# Set your API key in .env file
echo "GEMINI_API_KEY=your-key-here" > .env

# Run the example
make example8
```

## Important Notes

- Real API calls require a valid Gemini API key
- Tests use mocks and don't require an API key
- Be mindful of API rate limits and costs
