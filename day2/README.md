# Reasoning and Acting: Direct Prompting, Chain-of-Thought, and ReAct

## Project Overview

This project compares three AI problem-solving approaches:

1. Direct Prompting
2. Chain-of-Thought (CoT)
3. ReAct (Reasoning and Acting)

The project uses a course-fee scenario involving scholarships, calculations, and external tool usage.

## Scenario

The course fees used in the project are:

* CS101 = ₹12,000
* AI202 = ₹18,000
* DS303 = ₹15,000

The ReAct agent compares:

* CS101 + AI202 with a 10% scholarship
* All three courses with a 25% scholarship

The correct result is that the first option costs ₹27,000, while the second option costs ₹33,750. Therefore, the first option is cheaper by ₹6,750.

## Project Files

| File                  | Purpose                                             |
| --------------------- | --------------------------------------------------- |
| `agent.py`            | ReAct agent demonstrating tool use and observations |
| `tools.py`            | Course-fee lookup and calculator tools              |
| `direct_vs_cot.py`    | Comparison of Direct Prompting and Chain-of-Thought |
| `self_consistency.py` | Self-consistency experiment                         |
| `analysis.md`         | Complete project analysis and comparison            |
| `screenshots/`        | Output screenshots                                  |

## How to Run

Activate the virtual environment and run:

```bash
python direct_vs_cot.py
```

```bash
python self_consistency.py
```

```bash
python agent.py
```

## Main Learning

Direct Prompting is useful for simple questions, Chain-of-Thought is useful for multi-step reasoning, and ReAct is useful when reasoning needs to be combined with external tools.

## Conclusion

The project demonstrates how different AI approaches behave on reasoning and tool-use tasks and highlights the importance of selecting an approach according to the requirements of the problem.
