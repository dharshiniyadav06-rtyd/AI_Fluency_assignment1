from config import COURSE_FEES


def workflow(question):
    q = question.lower()

    # Rule 1: Scholarship calculation
    if (
        "cs101" in q
        and "ai202" in q
        and "10%" in q
        and "scholarship" in q
    ):
        total = COURSE_FEES["CS101"] + COURSE_FEES["AI202"]
        final_fee = total * 0.90
        return f"Total fee after 10% scholarship: ₹{final_fee:,.0f}"

    # Rule 2: Direct course-fee question
    for course in COURSE_FEES:
        if (
            course.lower() in q
            and ("fee" in q or "cost" in q or "price" in q)
        ):
            return f"Fee for {course}: ₹{COURSE_FEES[course]:,}"

    return "Sorry, I do not have a rule for this type of question."


if __name__ == "__main__":
    question = input("Q: ")
    print("A:", workflow(question))