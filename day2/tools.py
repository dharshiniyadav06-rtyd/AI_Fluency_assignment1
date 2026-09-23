COURSE_FEES = {
    "CS101": 12000,
    "AI202": 18000,
    "DS303": 15000,
}


def get_course_fee(course_code):
    return COURSE_FEES.get(course_code.upper(), "Course not found")


def calculator(expression):
    try:
        return eval(expression, {"__builtins__": {}}, {})
    except Exception as e:
        return f"Error: {e}"
