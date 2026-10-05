import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from tools import TOOLS, SCHEMAS
from validator import validate_arguments


# Load the existing .env from the parent folder
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(ENV_PATH)

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "openai/gpt-oss-20b"
MAX_STEPS = 8
MAX_TOKENS = 500


def execute_tool_call(tool_call):
    """
    Safely handle one model-generated tool call.

    Stages:
    1. Parse JSON
    2. Look up tool
    3. Validate arguments
    4. Execute tool

    Every failure becomes a string instead of crashing.
    """

    tool_name = tool_call.function.name
    raw_arguments = tool_call.function.arguments

    # 1. Parse JSON
    try:
        arguments = json.loads(raw_arguments)
    except (json.JSONDecodeError, TypeError):
        return f"Tool error: invalid JSON arguments: {raw_arguments}"

    # 2. Look up tool
    if tool_name not in TOOLS:
        return f"Tool error: unknown tool '{tool_name}'"

    # 3. Validate
    validation_error = validate_arguments(tool_name, arguments)

    if validation_error:
        return f"Tool error: {validation_error}"

    # 4. Execute
    try:
        result = TOOLS[tool_name](**arguments)
        return json.dumps(result)
    except Exception as e:
        return f"Tool error: execution failed: {e}"


def run_agent(question):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a movie information assistant. "
                "Use the available tools when needed. "
                "Do not invent movie information."
            )
        },
        {
            "role": "user",
            "content": question
        }
    ]

    seen_calls = set()
    max_tokens = MAX_TOKENS

    for step in range(1, MAX_STEPS + 1):

        print(f"\n--- Step {step} ---")

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=list(SCHEMAS.values()),
            tool_choice="auto",
            max_tokens=max_tokens
        )

        choice = response.choices[0]
        message = choice.message
        finish_reason = choice.finish_reason

        print("finish_reason:", finish_reason)

        # Retry truncated responses with more tokens
        if finish_reason == "length":
            print("Response truncated. Retrying with more tokens...")
            max_tokens *= 2
            continue

        # Normal final answer
        if finish_reason == "stop":
            print("Final answer:", message.content)
            return message.content

        # Tool calls
        if finish_reason == "tool_calls":
            tool_calls = message.tool_calls or []

            messages.append(message)

            if not tool_calls:
                return "Tool error: tool_calls finish reason but no tool calls received."

            for tool_call in tool_calls:

                call_signature = (
                    tool_call.function.name,
                    tool_call.function.arguments
                )

                # Detect repeated identical calls
                if call_signature in seen_calls:
                    error_message = (
                        "Tool error: repeated identical tool call detected. "
                        "Stopping to prevent an infinite loop."
                    )

                    print(error_message)

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": error_message
                    })

                    return error_message

                seen_calls.add(call_signature)

                print(
                    "Tool call:",
                    tool_call.function.name,
                    tool_call.function.arguments
                )

                result = execute_tool_call(tool_call)

                print("Tool result:", result)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

            continue

        # Unexpected finish reason
        return f"Agent stopped because of unexpected finish_reason: {finish_reason}"

    return f"Agent stopped after maximum of {MAX_STEPS} steps."


if __name__ == "__main__":
    question = input("Ask about a movie: ")

    answer = run_agent(question)

    print("\nFinal:", answer)