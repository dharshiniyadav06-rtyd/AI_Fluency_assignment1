# AI Fluency Assignment 1

## Overview

This project demonstrates the use of AI concepts including AI agents, tool calling, workflows, and interaction with external tools.

The project uses Python to implement a chatbot, workflow, and AI agent that can answer a course-fee question using available tools.

## Project Structure

```text
AI_F_A1/
├── agent.py
├── chatbot.py
├── workflow.py
├── tools.py
├── challenge.py
├── check_setup.py
├── config.py
├── requirements.txt
├── .gitignore
└── Output/
    ├── agent.png
    ├── chatbot.png
    └── workflow.png
```

## Components

### chatbot.py

Implements the chatbot interaction and generates an answer to the user's question.

### workflow.py

Implements a predefined workflow to retrieve course fees, calculate the total, and apply the scholarship.

### agent.py

Demonstrates an AI agent that selects and uses tools to solve the user's question step by step.

### tools.py

Contains the tools used by the chatbot, workflow, and agent, including course-fee retrieval and calculation.

## Example Question

**Question:**

What is the total fee for CS101 and AI202 after a 10% scholarship?

**Course Fees:**

* CS101: ₹12,000
* AI202: ₹18,000
* Combined fee: ₹30,000

**After 10% scholarship:**

₹30,000 × 0.90 = ₹27,000

**Final Answer:** ₹27,000

## AI Agent Execution

The agent performs the following steps:

1. Retrieves the fee for CS101.
2. Retrieves the fee for AI202.
3. Uses the calculator tool to calculate the discounted amount.
4. Generates the final response.

## Output

The `Output` folder contains screenshots demonstrating the execution of:

* Chatbot
* Workflow
* AI Agent

## Technologies Used

* Python
* Generative AI
* AI Agents
* Tool Calling / Function Calling
* Workflow-based processing
* Git
* GitHub

## How to Run

Activate the Python virtual environment and install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the chatbot:

```bash
python chatbot.py
```

Run the workflow:

```bash
python workflow.py
```

Run the AI agent:

```bash
python agent.py
```

## Note

Sensitive information such as API keys should not be committed to the repository. Environment variables are managed separately and excluded using `.gitignore`.
