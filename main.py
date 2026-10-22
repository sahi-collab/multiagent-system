from agents import build_graph


def main() -> None:
    topic = input("What topic would you like the agents to explore? ").strip()
    if not topic:
        print("Please enter a topic and run the program again.")
        return

    graph = build_graph()
    result = graph.invoke(
        {
            "user_input": topic,
            "research": "",
            "analysis": "",
            "final_answer": "",
        }
    )

    print("\nResearch points:")
    print(result["research"])
    print("\nAnalysis:")
    print(result["analysis"])
    print("\nFinal answer:")
    print(result["final_answer"])


if __name__ == "__main__":
    main()
