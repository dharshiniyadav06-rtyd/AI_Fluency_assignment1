from config import COURSE_FEES


def get_course_fee(course_code):
    course_code = course_code.upper()
    return COURSE_FEES.get(course_code)


def calculator(expression):
    return eval(expression)