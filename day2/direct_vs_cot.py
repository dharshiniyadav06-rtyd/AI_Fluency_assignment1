QUESTIONS = [
    {
        "question": "A student pays ₹90,000 for 8 instalments after a 15% scholarship. What is the original fee per instalment?",
        "direct": "₹13,235.29 per instalment.",
        "cot": "Original total = 90,000 / 0.85 = ₹105,882.35. Per instalment = 105,882.35 / 8 = ₹13,235.29.",
    },
    {
        "question": "A course has 10 sessions. A student attends 90% of them. How many sessions did the student attend?",
        "direct": "9 sessions.",
        "cot": "90% of 10 = 0.90 × 10 = 9 sessions.",
    },
    {
        "question": "Ravi is taller than Arun. Arun is taller than Priya. Who is the tallest and who is the shortest?",
        "direct": "Ravi is tallest and Priya is shortest.",
        "cot": "Ravi > Arun > Priya. Therefore, Ravi is tallest and Priya is shortest.",
    },
]


print("DIRECT PROMPTING vs CHAIN-OF-THOUGHT")
print("=" * 60)

for i, item in enumerate(QUESTIONS, 1):
    print(f"\nQuestion {i}: {item['question']}")

    print("\nDirect Prompting:")
    print(item["direct"])

    print("\nChain-of-Thought:")
    print(item["cot"])