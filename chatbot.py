from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a helpful college assistant.
You do NOT have access to the college's private course-fee database.
If a question requires private course-fee information, clearly say that you do not have access to it.
"""


def chatbot(question):
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    question = input("Q: ")
    print("A:", chatbot(question))