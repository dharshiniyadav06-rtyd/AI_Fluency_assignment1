\# Reasoning and Acting: Comparing Direct Prompting, Chain-of-Thought, and ReAct



\## 1. Introduction



This project compares three approaches for solving problems with an AI system: Direct Prompting, Chain-of-Thought (CoT), and ReAct (Reasoning and Acting). A course-fee scenario was selected because it contains both simple reasoning questions and a question that requires external information in the form of course-fee data.



The course fees used in this project are CS101 = ₹12,000, AI202 = ₹18,000, and DS303 = ₹15,000. The same general type of problem was considered using the three approaches to understand their differences in reasoning, tool usage, reliability, transparency, speed, and consistency.



\---



\## 2. Direct Prompting



Direct prompting asks the AI to answer a question directly without explicitly requesting a step-by-step reasoning process. The model receives the question and produces an answer immediately.



For example, one question used in this project was:



\*\*“A course has 10 sessions. A student attends 90% of them. How many sessions did the student attend?”\*\*



The direct answer is \*\*9 sessions\*\*.



Direct prompting is simple and fast because there is no additional reasoning structure or tool interaction. It is suitable for straightforward questions where the required information is already available and the calculation is simple.



However, direct prompting does not provide a detailed explanation of how the answer was obtained. Therefore, if the answer is incorrect, it can be more difficult to identify where the mistake occurred.



\---



\## 3. Chain-of-Thought (CoT)



Chain-of-Thought prompting encourages the model to solve a problem through a sequence of reasoning steps before giving the final answer. It is useful for problems involving calculations, comparisons, or logical relationships.



For example:



\*\*Question:\*\* A student pays ₹90,000 for 8 instalments after a 15% scholarship. What is the original fee per instalment?



The reasoning is:



Original total fee = ₹90,000 / 0.85

Original total fee = ₹105,882.35



Original fee per instalment = ₹105,882.35 / 8

= \*\*₹13,235.29\*\*



CoT can make multi-step problems easier to solve because the problem is broken into smaller steps. However, CoT does not automatically provide access to external information. If the required fee or other fact is not already available to the model, reasoning alone cannot retrieve it.



\---



\## 4. ReAct (Reasoning and Acting)



ReAct combines reasoning with actions performed through external tools. Instead of relying only on information already available to the model, the system can use tools to retrieve information or perform calculations.



For this project, the ReAct scenario compares:



\* CS101 + AI202 with a 10% scholarship

\* All three courses with a 25% scholarship



The agent first retrieves the course fees using the `get\_course\_fee()` tool. It then uses the calculator tool to perform the scholarship calculations.



The first option is:



₹12,000 + ₹18,000 = ₹30,000



After a 10% scholarship:



₹30,000 × 0.90 = \*\*₹27,000\*\*



The second option is:



₹12,000 + ₹18,000 + ₹15,000 = ₹45,000



After a 25% scholarship:



₹45,000 × 0.75 = \*\*₹33,750\*\*



Difference:



₹33,750 − ₹27,000 = \*\*₹6,750\*\*



Therefore, the first option costs ₹27,000 and is cheaper by ₹6,750.



The ReAct trace demonstrates the Action → Observation cycle. The agent retrieves information using tools and then uses the observations to continue the calculation. This makes ReAct more suitable when the answer depends on external information or tools.



\---



\## 5. Comparison of the Three Approaches



| Basis           | Direct Prompting                                        | Chain-of-Thought                                | ReAct                                                         |

| --------------- | ------------------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------- |

| Reasoning depth | Low; gives a direct answer                              | Higher; breaks the problem into reasoning steps | High; combines reasoning with actions                         |

| Tool access     | No tool usage                                           | Normally no external tool usage                 | Can call external tools                                       |

| Transparency    | Final answer is easy to see, but reasoning is not shown | More reasoning steps can be represented         | Actions and observations can be traced                        |

| Reliability     | Good for simple questions                               | Useful for multi-step reasoning                 | Useful when external information or calculations are required |

| Cost and speed  | Usually fastest and simplest                            | More processing may be required                 | Tool calls add processing time                                |

| Consistency     | Depends on the model response                           | Can vary between runs                           | Depends on both reasoning and tool results                    |



Direct prompting is most appropriate when the question is simple and all required information is already available. Chain-of-Thought is useful when the problem requires several reasoning steps. ReAct is useful when the problem requires both reasoning and interaction with external tools.



\---



\## 6. Self-Consistency Experiment



Self-consistency was tested using the question:



\*\*“A student pays ₹90,000 for 8 instalments after a 15% scholarship. What is the original fee per instalment?”\*\*



The correct answer is \*\*₹13,235.29 per instalment\*\*.



The experiment was performed five times at a non-zero temperature of 0.8. The five outputs were:



1\. The answer is ₹13,235.29.

2\. The original fee per instalment is ₹13,235.29.

3\. Approximately ₹13,235.29 per instalment.

4\. Approximately ₹13,235.29 per instalment.

5\. Approximately ₹13,235.29 per instalment.



The majority answer was \*\*“Approximately ₹13,235.29 per instalment.”\*\*, which occurred 3 out of 5 times. Although the wording changed between runs, all five responses contained the same correct numerical answer. This shows that variation can occur between repeated responses even when the underlying answer remains the same.



The experiment was then repeated at temperature 0. At temperature 0, all five runs produced the same answer:



\*\*₹13,235.29 per instalment.\*\*



The majority count was therefore 5 out of 5. This demonstrates that lower temperature can produce more consistent outputs for the same question.



\---



\## 7. Suitability Analysis



Direct prompting is suitable for simple factual or calculation-based questions where the required information is already available. It has low complexity and can produce an answer quickly. For example, calculating 90% of 10 sessions does not require a complex reasoning process.



Chain-of-Thought is more suitable for problems involving multiple calculations or logical relationships. The scholarship question is a good example because the original fee must first be calculated from the discounted amount and then divided into instalments. Breaking the calculation into steps makes the process easier to follow and verify.



ReAct is suitable when the problem requires external information or tools. In the course-fee comparison, the agent needs the fees of CS101, AI202, and DS303 and then needs calculations to compare the two options. The tool calls provide the required information and calculations, making ReAct more appropriate for this type of task.



No single approach is suitable for every problem. The choice depends on whether the task requires simple answering, deeper reasoning, or interaction with external tools.



\---



\## 8. Limitations



Direct prompting has limited transparency because it normally provides only the final answer. It may also struggle with complicated multi-step problems if the prompt does not provide enough structure.



Chain-of-Thought can improve the handling of multi-step reasoning, but it cannot independently retrieve missing external information. If a required fact is not available in the prompt or model knowledge, additional tools are needed.



ReAct can access tools and external information, but each tool call adds complexity and processing time. It also depends on the correctness and availability of the tools. Incorrect tool results can lead to an incorrect final answer.



The self-consistency experiment also has a limitation. Repeated model responses can vary in wording, especially at higher temperature. Therefore, the majority answer should be checked against the actual problem rather than assuming that the most frequent response is automatically correct.



\---



\## 9. Conclusion



This project demonstrated the differences between Direct Prompting, Chain-of-Thought, and ReAct using course-fee and reasoning problems. Direct Prompting provides a quick answer and is suitable for simple tasks. Chain-of-Thought is useful for multi-step calculations and logical reasoning. ReAct extends reasoning by allowing the system to interact with tools and use their observations when producing an answer.



The ReAct example showed how course-fee information could be retrieved and calculations could be performed using tools. The self-consistency experiment also showed that repeated responses can vary at a non-zero temperature while producing consistent results at temperature 0.



Overall, the experiment demonstrates that the appropriate approach depends on the requirements of the task: direct answers for simple problems, structured reasoning for multi-step problems, and reasoning combined with tools when external information or actions are required.



