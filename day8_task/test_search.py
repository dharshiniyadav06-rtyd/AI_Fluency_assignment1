
from task_agent import search_handbook

for query in [
    "CGPA eligibility placements",
    "maximum late fee",
    "capital of France",
]:
    print(f"\nQuestion: {query}")
    result = search_handbook.invoke({"query": query})
    print("Result:", repr(result))
