import json
from tools import SCHEMAS


def validate_arguments(tool_name, arguments):
    """
    Validate tool arguments against the schema.

    Returns:
        None if valid
        Error message string if invalid
    """

    if tool_name not in SCHEMAS:
        return f"Unknown tool: {tool_name}"

    schema = SCHEMAS[tool_name]["function"]["parameters"]

    # Check that arguments are a dictionary
    if not isinstance(arguments, dict):
        return "Invalid arguments: expected a JSON object."

    properties = schema.get("properties", {})
    required = schema.get("required", [])

    # 1. Check missing required arguments
    for field in required:
        if field not in arguments:
            return f"Missing required argument: {field}"

    # 2. Check invented/extra arguments
    if schema.get("additionalProperties") is False:
        for field in arguments:
            if field not in properties:
                return f"Invented/extra argument: {field}"

    # 3. Check argument types
    for field, value in arguments.items():
        if field not in properties:
            continue

        expected_type = properties[field].get("type")

        if expected_type == "string" and not isinstance(value, str):
            return f"Wrong type for '{field}': expected string."

        if expected_type == "integer" and not isinstance(value, int):
            return f"Wrong type for '{field}': expected integer."

        if expected_type == "number" and not isinstance(value, (int, float)):
            return f"Wrong type for '{field}': expected number."

        if expected_type == "boolean" and not isinstance(value, bool):
            return f"Wrong type for '{field}': expected boolean."

    # 4. Check enum values
    for field, value in arguments.items():
        if field not in properties:
            continue

        allowed_values = properties[field].get("enum")

        if allowed_values is not None and value not in allowed_values:
            return (
                f"Invalid value for '{field}': '{value}'. "
                f"Expected one of: {allowed_values}"
            )

    return None


# Small test section
if __name__ == "__main__":
    tests = [
        (
            "Valid",
            "get_movie_info",
            {"movie": "Inception"}
        ),
        (
            "Missing argument",
            "get_movie_info",
            {}
        ),
        (
            "Extra argument",
            "get_movie_info",
            {
                "movie": "Inception",
                "director": "Christopher Nolan"
            }
        ),
        (
            "Wrong type",
            "get_movie_info",
            {"movie": 123}
        ),
        (
            "Invalid enum",
            "get_movie_info",
            {"movie": "Avatar"}
        )
    ]

    for name, tool_name, arguments in tests:
        result = validate_arguments(tool_name, arguments)

        if result is None:
            print(f"{name}: VALID")
        else:
            print(f"{name}: {result}")