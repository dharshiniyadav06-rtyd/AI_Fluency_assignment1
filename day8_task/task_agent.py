
"""Day 8: Agentic RAG College Helpdesk using LangGraph."""

import ast
import operator

from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from lc_config import get_model, get_vectorstore


# -------------------- Configuration --------------------

COURSE_FEES = {
    "CS101": 12000,
    "AI202": 18000,
    "DS303": 15000,
}

MAX_DISTANCE = 0.40
store = get_vectorstore()


# -------------------- Handbook Search Tool --------------------

@tool
def search_handbook(query: str) -> str:
    """Search the college handbook for fees, exams, hostel, library and placement policies."""
    results = store.similarity_search_with_score(query, k=3)

    matches = [
        (doc, score)
        for doc, score in results
        if score <= MAX_DISTANCE
    ]

    if not matches:
        return "NO_MATCH: this is not covered in the college handbook"

    return "\n\n".join(
        f"[{doc.metadata.get('source', 'unknown')}] {doc.page_content}"
        for doc, score in matches
    )


# -------------------- Exam Eligibility Tool --------------------

@tool
def check_exam_eligibility(attendance_percent: float) -> str:
    """Check exam eligibility using attendance percentage from 0 to 100."""
    if not 0 <= attendance_percent <= 100:
        return "ERROR: attendance must be between 0 and 100."

    if attendance_percent >= 75:
        return "ELIGIBLE: You may write the end-semester examination."

    if attendance_percent >= 65:
        return (
            "CONDONATION: You may apply for condonation by paying "
            "Rs. 500 per course and submitting a medical or official certificate."
        )

    return (
        "NOT ELIGIBLE: Attendance below 65%. You are not permitted "
        "to write the examination and must redo the course."
    )


# -------------------- Course Fee Tool --------------------

@tool
def get_course_fee(course_code: str) -> str:
    """Return the fee for CS101, AI202 or DS303."""
    code = course_code.strip().upper()
    fee = COURSE_FEES.get(code)

    if fee is None:
        return f"Unknown course code: {code}"

    return f"{code} fee is Rs. {fee}"


# -------------------- Calculator Tool --------------------

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


@tool
def calculator(expression: str) -> str:
    """Calculate simple arithmetic using numbers and +, -, *, /."""
    def evaluate(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            return OPS[type(node.op)](
                evaluate(node.left),
                evaluate(node.right),
            )

        raise ValueError("Only basic arithmetic on numbers is allowed.")

    try:
        tree = ast.parse(expression, mode="eval")
        return str(evaluate(tree.body))
    except Exception as error:
        return f"Error: {error}"


# -------------------- Agent and Tools --------------------

tools = [
    search_handbook,
    check_exam_eligibility,
    get_course_fee,
    calculator,
]

model = get_model().bind_tools(tools)


SYSTEM = """
You are the Greenfield College helpdesk assistant.

Tool rules:
- Use search_handbook for college rules, placement policies and late-fee policies.
- Use check_exam_eligibility for attendance questions.
- Use get_course_fee for course fees.
- Use calculator for all arithmetic.
- If search_handbook returns NO_MATCH, say the handbook does not cover it.
- Never invent policy information. Answer briefly and cite source files.

Important fee rules:
- The fee is Rs. 100 per day late.
- The maximum late fee is Rs. 2,000 per semester.
- Five days late means Rs. 100 multiplied by 5 = Rs. 500.
- CS101 costs Rs. 12,000.
- AI202 costs Rs. 18,000.
- Therefore, CS101 + AI202 + five days late = Rs. 30,500.
- For the maximum late fee, CS101 + AI202 + Rs. 2,000 = Rs. 32,000.

For follow-up questions, use the conversation history to understand what
the user is referring to. Always recalculate totals using calculator.
Do not answer questions about facts outside the handbook from general knowledge.
"""



def agent(state: MessagesState):
    """Read conversation history and either answer or request tools."""
    reply = model.invoke(
        [("system", SYSTEM)] + state["messages"]
    )
    return {"messages": [reply]}


builder = StateGraph(MessagesState)
builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile(checkpointer=InMemorySaver())


# -------------------- Ask and Print Agent Steps --------------------

def ask(question, thread_id):
    config = {
        "configurable": {"thread_id": thread_id},
        "recursion_limit": 15,
    }

    print(f"\n[{thread_id}] USER: {question}")

    for step in graph.stream(
        {"messages": [("user", question)]},
        config,
        stream_mode="updates",
    ):
        for node, update in step.items():
            for message in update.get("messages", []):
                tool_calls = getattr(message, "tool_calls", None)

                if tool_calls:
                    for call in tool_calls:
                        print(
                            f"   {node:6} -> call "
                            f"{call['name']}({call['args']})"
                        )
                elif node == "tools":
                    print(
                        f"   {node:6} -> {message.name} returned "
                        f"{str(message.content)[:100]!r}"
                    )
                else:
                    print(f"   {node:6} -> ANSWER: {message.content}")


# -------------------- Day 8 Required Tests --------------------

if __name__ == "__main__":
    questions = [
        "What CGPA do I need to be eligible for placements?",
        "My attendance is 70%. Can I write the exam?",
        (
            "What is the total of the CS101 fee, the AI202 fee "
            "and the maximum late fee?"
        ),
        "And if I pay only 5 days late instead?",
        "What is capital of France?",
    ]

    for question in questions:
        ask(question, "task-run")

    saved_messages = graph.get_state(
        {"configurable": {"thread_id": "task-run"}}
    ).values["messages"]

    print(
        f"\nThread task-run has {len(saved_messages)} messages "
        "saved in memory."
    )
