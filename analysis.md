# Analysis

## 1. Task Overview

The AI Fluency Assignment 1 focuses on understanding how an AI application can use Large Language Models, tools, workflows, and agents to solve a user query.

The task demonstrates the progression from a basic chatbot response to a workflow-based solution and finally to an AI agent that can select and use tools to obtain the required information.

## 2. Problem Statement

The application is tested using the following question:

**"What is the total fee for CS101 and AI202 after a 10% scholarship?"**

The course fees used by the application are:

* CS101: ₹12,000
* AI202: ₹18,000

Total fee:

**₹12,000 + ₹18,000 = ₹30,000**

After a 10% scholarship:

**₹30,000 × 90% = ₹27,000**

Therefore, the final fee is **₹27,000**.

## 3. Implementation Approach

The project contains three approaches:

### Chatbot

The chatbot provides a response to the user query using the configured language model.

### Workflow

The workflow follows a predefined sequence of steps to process the query and calculate the final fee.

The calculation is:

**₹30,000 × 0.9 = ₹27,000**

### AI Agent

The agent uses tools to obtain the required course fees and then performs the calculation.

The agent execution consists of:

1. Retrieve the fee for CS101.
2. Retrieve the fee for AI202.
3. Calculate the combined fee after applying the 10% scholarship.
4. Generate the final response.

## 4. Tool Calling

The agent uses tools to perform specific operations.

For the given query:

* `get_course_fee("CS101")` → ₹12,000
* `get_course_fee("AI202")` → ₹18,000
* `calculator("30000*0.9")` → ₹27,000

This demonstrates how an AI agent can combine information from tools and use the results to complete a task.

## 5. Workflow vs Agent

A workflow follows predefined steps in a fixed order.

An AI agent can determine which tools or actions are required to solve a task.

In this project, the workflow demonstrates structured execution, while the agent demonstrates tool selection and tool-based reasoning.

## 6. Output Verification

The outputs were tested using the same user query.

The workflow produced:

**Total fee after 10% scholarship: ₹27,000**

The agent produced a detailed response showing the individual course fees, combined fee, scholarship calculation, and final amount.

The results were verified against the expected mathematical calculation.

## 7. Key Learning

Through this assignment, I learned:

* How an AI application processes a user prompt.
* How tools can provide specific information to an AI system.
* How workflows can organize multiple steps.
* How AI agents can use tools to solve tasks.
* How calculations can be delegated to a calculator tool.
* How to verify AI-generated results.
* How to manage and submit a Python project using Git and GitHub.

## 8. Conclusion

This assignment provided practical understanding of AI agents, tool calling, workflows, and LLM-based applications.

The project demonstrates that combining an AI model with reliable tools can produce more useful and verifiable results for task-specific queries.
