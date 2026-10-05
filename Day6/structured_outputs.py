import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# Load existing .env
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(ENV_PATH)

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "openai/gpt-oss-20b"


QUESTION = """
Return the answer as JSON.
Extract the following movie information from this sentence:

"Inception is a 2010 science fiction movie directed by Christopher Nolan
with a rating of 8.8."

Return:
movie, year, genre, director, rating
"""


SCHEMA = {
    "type": "object",
    "properties": {
        "movie": {"type": "string"},
        "year": {"type": "integer"},
        "genre": {"type": "string"},
        "director": {"type": "string"},
        "rating": {"type": "number"}
    },
    "required": [
        "movie",
        "year",
        "genre",
        "director",
        "rating"
    ],
    "additionalProperties": False
}


def run_case(title, response_format=None):
    print(f"\n{'=' * 60}")
    print(title)
    print("=" * 60)

    try:
        kwargs = {
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": QUESTION
                }
            ],
            "max_tokens": 300
        }

        if response_format is not None:
            kwargs["response_format"] = response_format

        response = client.chat.completions.create(**kwargs)

        raw = response.choices[0].message.content

        print("Raw reply:")
        print(raw)

        try:
            parsed = json.loads(raw)

            print("\nParsed result:")
            print(json.dumps(parsed, indent=2))

        except json.JSONDecodeError as e:
            print("\nParse error:", e)

    except Exception as e:
        print("\nAPI/format error:", e)


# 1. No constraint
run_case(
    "CASE 1 — NO CONSTRAINT"
)


# 2. JSON mode
run_case(
    "CASE 2 — JSON MODE",
    {
        "type": "json_object"
    }
)


# 3. JSON Schema mode
run_case(
    "CASE 3 — JSON SCHEMA MODE",
    {
        "type": "json_schema",
        "json_schema": {
            "name": "movie_extraction",
            "strict": True,
            "schema": SCHEMA
        }
    }
)