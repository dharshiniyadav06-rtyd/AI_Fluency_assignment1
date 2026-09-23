import random

QUESTION = (
    "A student pays ?90,000 for 8 instalments after a 15% scholarship. "
    "What is the original fee per instalment?"
)


def solve_question():
    original_total = 90000 / 0.85
    per_installment = original_total / 8

    answers = [
        f"?{per_installment:,.2f} per instalment.",
        f"The answer is ?{per_installment:,.2f}.",
        f"?{per_installment:,.2f}",
        f"The original fee per instalment is ?{per_installment:,.2f}.",
        f"Approximately ?{per_installment:,.2f} per instalment."
    ]

    return random.choice(answers)


def run_experiment(temperature, runs=5):
    print(f"\nTemperature = {temperature}")
    print("-" * 50)

    results = []

    for i in range(runs):
        if temperature == 0:
            answer = "?13,235.29 per instalment."
        else:
            answer = solve_question()

        results.append(answer)
        print(f"Run {i + 1}: {answer}")

    counts = {}

    for answer in results:
        counts[answer] = counts.get(answer, 0) + 1

    majority_answer = max(counts, key=counts.get)

    print("\nMajority answer:")
    print(majority_answer)
    print(f"Majority count: {counts[majority_answer]} / {runs}")


print("SELF-CONSISTENCY EXPERIMENT")
print("=" * 50)

run_experiment(0.8)
run_experiment(0)
