import json
from types import SimpleNamespace

from agent import execute_tool_call


def make_tool_call(tool_name, arguments):
    """Create a fake tool call like the OpenAI SDK object."""
    return SimpleNamespace(
        id="fault-test",
        function=SimpleNamespace(
            name=tool_name,
            arguments=arguments
        )
    )


faults = [
    (
        "1. Invalid JSON",
        make_tool_call(
            "get_movie_info",
            '{"movie":"Inception"'
        )
    ),

    (
        "2. Unknown tool",
        make_tool_call(
            "get_unknown_movie",
            '{"movie":"Inception"}'
        )
    ),

    (
        "3. Missing required argument",
        make_tool_call(
            "get_movie_info",
            '{}'
        )
    ),

    (
        "4. Wrong argument type",
        make_tool_call(
            "get_movie_info",
            '{"movie":123}'
        )
    ),

    (
        "5. Invalid enum value",
        make_tool_call(
            "get_movie_info",
            '{"movie":"Avatar"}'
        )
    ),

    (
        "6. Invented argument",
        make_tool_call(
            "get_movie_info",
            '{"movie":"Inception","director":"Christopher Nolan"}'
        )
    ),

    (
        "7. JSON array instead of object",
        make_tool_call(
            "get_movie_info",
            '["Inception"]'
        )
    ),

    (
        "8. Empty arguments",
        make_tool_call(
            "get_movie_rating",
            ''
        )
    )
]


print("=== DAY 6 FAULT INJECTION TEST ===")

for name, tool_call in faults:
    print(f"\n--- {name} ---")

    try:
        result = execute_tool_call(tool_call)

        print("Result:", result)
        print("Continued: YES")

    except Exception as e:
        print("CRASH:", e)
        print("Continued: NO")