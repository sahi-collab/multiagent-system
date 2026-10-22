from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict):
    """Information passed from one agent node to the next."""

    user_input: str
    research: str
    analysis: str
    final_answer: str


def researcher(state: AgentState) -> dict[str, str]:
    """Create a few introductory research points from the user's topic."""
    topic = state["user_input"].strip()
    research = (
        f"- {topic} is the subject being explored.\n"
        f"- A useful starting point is to understand the main ideas behind {topic}.\n"
        f"- Its practical examples can help explain why {topic} matters."
    )
    print("\n[Researcher] Gathered a few starting points.")
    return {"research": research}


def analyst(state: AgentState) -> dict[str, str]:
    """Summarize the research points into a central takeaway."""
    topic = state["user_input"].strip()
    point_count = sum(1 for line in state["research"].splitlines() if line.startswith("- "))
    analysis = (
        f"The {point_count} research points introduce {topic}, emphasize learning its key ideas, "
        "and connect the topic with practical examples. This is a brief overview, not an in-depth assessment."
    )
    print("[Analyst] Summarized the research.")
    return {"analysis": analysis}


def writer(state: AgentState) -> dict[str, str]:
    """Turn the analysis into a concise final response."""
    summary = state["analysis"].split(" This is", maxsplit=1)[0]
    final_answer = f"{summary} Start with its key ideas, then use practical examples to understand them."
    print("[Writer] Prepared the final response.")
    return {"final_answer": final_answer}


def build_graph():
    """Build and compile the three-agent, sequential workflow."""
    workflow = StateGraph(AgentState)
    workflow.add_node("researcher", researcher)
    workflow.add_node("analyst", analyst)
    workflow.add_node("writer", writer)

    workflow.add_edge(START, "researcher")
    workflow.add_edge("researcher", "analyst")
    workflow.add_edge("analyst", "writer")
    workflow.add_edge("writer", END)

    return workflow.compile()
