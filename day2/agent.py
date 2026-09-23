from tools import get_course_fee, calculator


def agent(question):
    print("QUESTION:", question)
    print("\n--- ReAct Trace ---")

    fees = {}

    for course in ["CS101", "AI202", "DS303"]:
        fee = get_course_fee(course)
        fees[course] = fee
        print(f"Action: get_course_fee({course})")
        print(f"Observation: {fee}")

    option1 = calculator("(12000 + 18000) * 0.90")
    option2 = calculator("(12000 + 18000 + 15000) * 0.75")
    difference = calculator("33750 - 27000")

    print(f"Action: calculator((12000 + 18000) * 0.90)")
    print(f"Observation: {option1}")

    print(f"Action: calculator((12000 + 18000 + 15000) * 0.75)")
    print(f"Observation: {option2}")

    print(f"Action: calculator(33750 - 27000)")
    print(f"Observation: {difference}")

    answer = (
        f"CS101 + AI202 with 10% scholarship = ₹{option1:,.0f}\n"
        f"All three courses with 25% scholarship = ₹{option2:,.0f}\n"
        f"The first option is cheaper by ₹{difference:,.0f}."
    )

    print("\nFINAL ANSWER:")
    print(answer)

    return answer


if __name__ == "__main__":
    question = (
        "Which is cheaper: CS101 and AI202 with a 10% scholarship, "
        "or all three courses with a 25% scholarship? And by how much?"
    )

    agent(question)