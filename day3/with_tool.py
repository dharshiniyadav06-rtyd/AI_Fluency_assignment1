from groq import Groq
from dotenv import load_dotenv
import os
import json

from calculator_tool import calculator

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

question = "What is the purpose of a scholarship for college students?"
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculates a mathematical expression accurately.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to calculate."
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

messages = [
    {
        "role": "user",
        "content": question
    }
]

response = client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages=messages,
    tools=tools,
    tool_choice="auto"
        
    
)

message = response.choices[0].message

print("=== LLM WITH ONE TOOL ===")
print("Question:", question)

if message.tool_calls:
    tool_call = message.tool_calls[0]

    print("\n--- TOOL CALL ---")
    print("Tool:", tool_call.function.name)
    print("Arguments:", tool_call.function.arguments)

    arguments = json.loads(tool_call.function.arguments)

    tool_result = calculator(arguments["expression"])

    print("Tool result:", tool_result)

    messages.append(message)
    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": tool_result
        }
    )

    final_response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages
    )

    print("\n--- FINAL ANSWER ---")
    print(final_response.choices[0].message.content)

else:
    print("\nNo tool was called.")
    print("Answer:", message.content)