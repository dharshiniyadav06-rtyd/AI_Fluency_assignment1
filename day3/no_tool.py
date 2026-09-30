from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

question = "What is the purpose of a scholarship for college students?"

response = client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages=[
        {
            "role": "user",
            "content": question
        }
    ]
)

print("=== PLAIN LLM (NO TOOL) ===")
print("Question:", question)
print("Answer:", response.choices[0].message.content)