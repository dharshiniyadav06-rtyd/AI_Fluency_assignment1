\# Day 8 – College Helpdesk Agent Results



\## Configuration

\- \*\*Embedding model:\*\* BAAI/bge-small-en-v1.5

\- \*\*Chat model:\*\* openai/gpt-oss-20b (Groq)

\- \*\*Vector database:\*\* Chroma

\- \*\*Maximum cosine distance:\*\* 0.40

\- \*\*Knowledge base:\*\* 6 documents, 27 chunks



\## Retrieval Threshold Testing

\- Placement eligibility query: Relevant result from `placement\_policy.md`, distance 0.185.

\- Capital of France query: Nearest results had distances around 0.573–0.577.

\- Threshold selected: 0.40. Relevant policy results are retained, while the unrelated France question is rejected.



\## Agent Test Results



| # | Tools Called | Expected Answer | Correct? | Notes |

|---|---|---|---|---|

| 1 | `search\_handbook` | CGPA of 6.5 or above with no standing arrears is required for placements. Source: `placement\_policy.md`. | Yes | Correct answer |

| 2 | `check\_exam\_eligibility` | At 70% attendance, the student may apply for condonation by paying Rs. 500 per course and providing a medical or official certificate. | Yes | Correct answer |

| 3 | `search\_handbook`, `get\_course\_fee`, `calculator` | Rs. 12,000 + Rs. 18,000 + Rs. 2,000 = Rs. 32,000. | Yes | Correct calculation |

| 4 | `calculator` and conversation memory | Five-day late fee = Rs. 500. Total = Rs. 12,000 + Rs. 18,000 + Rs. 500 = Rs. 30,500. | Yes | Correct follow-up answer |

| 5 | No tool call | The college handbook does not contain information about the capital of France. | Yes | Correctly rejected an out-of-scope question |



\## Summary

The College Helpdesk Agent uses retrieval-augmented generation (RAG) to search college policy documents. It includes tools for handbook search, exam eligibility, course fee lookup and arithmetic calculations. Conversation memory supports follow-up questions, and the retrieval distance threshold helps reject unrelated questions.



All five test questions produced the expected answers in the final run.

