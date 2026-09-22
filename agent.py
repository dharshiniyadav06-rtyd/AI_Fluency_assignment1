from groq import Groq
from dotenv import load_dotenv
import os
import json

from tools import get_course_fee, calculator

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_course_fee",
            "description": "Get the private course fee for a course code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_code": {
                        "type": "string",
                        "description": "Course code such as CS101, AI202, or DS303"
                    }
                },
                "required": ["course_code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to calculate"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


def run_tool(name, arguments):
    if name == "get_course_fee":
        return get_course_fee(arguments["course_code"])

    if name == "calculator":
        return calculator(arguments["expression"])

    return None


def agent(question):
    messages = [
        {
            "role": "system",
            "content": """
You are a college course-fee assistant.

All course fees are in Indian Rupees (₹).
Always display course fees using ₹, never $.

You have access to private course-fee data through tools.

Use the get_course_fee tool whenever you need course-fee information.

Use the calculator tool whenever calculations are required.

You may call tools multiple times until you have enough information
to answer the user's question accurately.
"""
        },
        {"role": "user", "content": question}
    ]

    steps = []

    for _ in range(10):
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return message.content, steps

        messages.append(message)

        for tool_call in message.tool_calls:
            name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            result = run_tool(name, arguments)

            steps.append(
                f"{name}({arguments}) -> {result}"
            )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                }
            )

    return "The agent could not complete the request.", steps


if __name__ == "__main__":
    question = input("Q: ")

    answer, steps = agent(question)

    for i, step in enumerate(steps, 1):
        print(f"step {i}: {step}")

    print("A:", answer)