\# From Prompt to Action: Understanding LLMs, Tools, and Agents on a Scenario of Your Own



\## 3.1 Explanation of Concepts



\### What is an LLM?



A Large Language Model (LLM) is an AI model trained on a large amount of text to understand and generate human-like language. It can answer questions using the knowledge and patterns learned during training. For example, in this scenario, the LLM can explain the general purpose of scholarships for college students without using any external tool. However, an LLM does not automatically have access to a college's current private fee database. It can also make mistakes in factual or numerical questions, especially when information is missing, current, private, or requires exact calculation.



\### What is an Agent?



An AI agent is a system where an LLM can decide to take an action, such as calling an external tool, and then use the result to produce an answer. A plain chat model mainly generates an answer from its available knowledge and the information provided in the prompt. An agent can go beyond this by interacting with external tools when they are available. In this project, the tool-enabled LLM can use a calculator to perform fee calculations and then include the tool result in its final response.



\### What is a Tool and Tool Call?



A tool is an external function that an LLM can use to perform a specific task. A tool call is the request made by the LLM to use that function. In this project, the only tool is a calculator that receives a mathematical expression and returns the calculated result.



The tool schema tells the model what tool is available and how to use it. The schema contains the tool name, description, and parameters. The name identifies the function, the description explains what it does, and the parameters specify the information that must be provided. This information helps the model decide when the tool is useful and what arguments should be sent.



\### One Tool Call Flow



The tool-calling process in this project follows these steps:



1\. The user asks a question.

2\. The LLM receives the question and the calculator tool schema.

3\. The LLM decides whether the calculator is needed.

4\. If calculation is required, the LLM generates a tool call containing the mathematical expression.

5\. The calculator tool runs the expression.

6\. The tool returns the result as plain text.

7\. The result is sent back to the LLM.

8\. The LLM uses the tool result to generate the final answer for the user.



For example, for the question about calculating the AI202 fee after a 15% scholarship, the tool-enabled run called the calculator with the expression `18000 \* 0.85`. The tool returned `15300.0`, and the LLM used that result to produce the final answer of ₹15,300.



\### Why Return Plain Text on Failure?



A tool should return its result as plain text even when an error occurs because the agent can then receive the error as an observation and decide what to do next. If the tool raises an exception that stops the entire program, the agent cannot continue the interaction or produce a useful response. Returning an error message such as `Calculation error: ...` keeps the program running and makes the problem visible to the LLM or the user.



\## 3.2 Comparison Table



| Basis                                       | Plain LLM prompt (no tool)                                                        | LLM with one tool                                                                         |

| ------------------------------------------- | --------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |

| Source of answer                            | Uses its learned knowledge and information in the prompt                          | Uses learned knowledge plus the result from the external calculator when needed           |

| Can it fetch or compute outside own memory? | No external computation or tool access                                            | Yes, it can use the calculator provided to it                                             |

| Reliability on factual/numeric questions    | Can be correct, but may calculate incorrectly or lack current/private information | Numerical calculations can be checked through the calculator tool                         |

| Transparency                                | The external calculation process is not shown                                     | The tool name, arguments, and tool result can be displayed                                |

| Speed / cost                                | Usually requires one model response                                               | Can require an additional tool execution and model response, so it may add some time/cost |



\## 3.3 Minimal Implementation



The implementation uses one external tool: a calculator function. The `calculator\_tool.py` file contains the calculator function, which receives a mathematical expression and returns the result as text. It also returns a text error message if the calculation fails.



The `no\_tool.py` script sends a question directly to the same Groq LLM without providing any tools. This demonstrates how the LLM responds using only the prompt and its own learned knowledge.



The `with\_tool.py` script uses the same LLM but provides one calculator tool through a tool schema. When the model decides that a calculation is needed, it creates a calculator tool call with the required expression. The program executes the calculator, sends the result back to the model, and prints the final answer. The implementation uses one tool call and does not implement a full multi-step ReAct loop or multi-tool registry.



\## 3.4 Observation



Three questions were used to observe the difference between a plain LLM and an LLM with one calculator tool.



For the first calculation question, `What is the fee for AI202 after a 15% scholarship if the original fee is ₹18000?`, the plain LLM correctly calculated the answer as ₹15,300 without using a tool. When the same question was run with the calculator available, the LLM correctly called the calculator with the expression `18000 \* 0.85`. The calculator returned `15300.0`, and the final answer was ₹15,300. This shows that the plain LLM was capable of doing the calculation, while the tool-enabled version provided an explicit calculation result.



For the second calculation question, `What is the total fee of CS101 (₹12000) and AI202 (₹18000) after a 10% scholarship?`, the plain LLM correctly calculated the total as ₹27,000. The tool-enabled version used the calculator to perform the calculation and used the returned result in its final answer. This demonstrates how an external calculator can make numerical processing more explicit.



For the third question, `What is the purpose of a scholarship for college students?`, no calculation was required. The plain LLM answered the question using its general knowledge. The tool-enabled version also answered the question without calling the calculator. This demonstrates that a tool is not necessary for every type of question and that automatic tool selection can allow the model to answer directly when the available tool is not useful.



Overall, the observations show that the plain LLM can handle general knowledge and simple arithmetic, but the external calculator provides a separate, visible source for numerical computation.



\## 3.5 Suitability and Conclusion



For this college course-fee scenario, a plain LLM is suitable for general questions such as explaining the purpose of scholarships. It can also perform simple arithmetic correctly in many cases. However, when an answer depends on exact numerical computation, an external calculator can provide a more explicit and verifiable calculation result.



The main difference is that a plain LLM generates an answer from its learned knowledge and the prompt, while an LLM with a tool can take an action outside the model and use the returned result. The tool schema provides the model with information about what the tool does and what parameters it requires. The experiment shows that tools are useful when the task benefits from reliable external computation, while they are unnecessary for questions that can be answered directly from general knowledge.



