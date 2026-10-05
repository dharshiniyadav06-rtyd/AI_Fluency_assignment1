\# Day 6 Analysis — Reliable Tool Calling



\## 1. Scenario



\### Movie Information Assistant



This project demonstrates reliable tool calling using an OpenAI-compatible API.



The assistant has two tools:



1\. `get\_movie\_info`

&#x20;  - Returns movie name, genre, director, and year.



2\. `get\_movie\_rating`

&#x20;  - Returns the movie rating.



The tools use a shared JSON Schema and the same schema is used by the validator.



\---



\# 2. Chat Completions Format



The agent uses the Chat Completions API.



The main request fields are:



\- `model` — specifies the model.

\- `messages` — contains the conversation.

\- `tools` — contains available tool definitions.

\- `tool\_choice` — controls whether tools can be selected.

\- `max\_tokens` — limits the generated output.



The response contains:



\- `choices`

\- `message`

\- `finish\_reason`



Important `finish\_reason` values observed in this project:



\### `stop`



The model has finished generating a normal answer.



Example:



```text

finish\_reason: stop

Final answer: The rating for Inception is 8.8.

