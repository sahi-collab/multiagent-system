# Three-agent LangGraph demo

A minimal Python example of a sequential multi-agent workflow. The agents use simple local logic, so no LLM provider, API key, or `.env` loading package is needed.

## What LangGraph does here

LangGraph's `StateGraph` creates a graph whose shared state is passed between Python functions. Each function below is a node, and the explicit edges set the order in which those nodes run:

```text
User input -> Researcher -> Analyst -> Writer -> Final output
```

- **Researcher** reads `user_input` and adds a few introductory points to `research`.
- **Analyst** reads the topic and research context and adds a short summary to `analysis`.
- **Writer** reads the analysis and writes a concise `final_answer`.

The state has four fields: `user_input`, `research`, `analysis`, and `final_answer`. Each node returns the field it updates; LangGraph merges that update into the shared state before running the next node.

These are deterministic example agents, not live web research or LLM calls. The goal is to show the workflow structure clearly.

## Requirements and installation

Python 3.10 or newer is recommended. Install the sole external dependency with:

```bash
python -m pip install -r requirements.txt
```

No API key is required. `.env.example` is included to make that explicit; the program does not read it.

## Run the browser demo

From this directory:

```bash
python app.py
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser, enter a topic, and select **Run agents**. The page shows the state produced by each node and the final answer. Press `Ctrl+C` in the terminal to stop the server.

You can also run the original terminal version:

```bash
python main.py
```

Enter a topic when prompted.

## Example

```text
What topic would you like the agents to explore? solar energy

[Researcher] Gathered a few starting points.
[Analyst] Summarized the research.
[Writer] Prepared the final response.

Research points:
- solar energy is the subject being explored.
- A useful starting point is to understand the main ideas behind solar energy.
- Its practical examples can help explain why solar energy matters.

Analysis:
The 3 research points introduce solar energy, emphasize learning its key ideas, and connect the topic with practical examples. This is a brief overview, not an in-depth assessment.

Final answer:
The 3 research points introduce solar energy, emphasize learning its key ideas, and connect the topic with practical examples. Start with its key ideas, then use practical examples to understand them.
```
