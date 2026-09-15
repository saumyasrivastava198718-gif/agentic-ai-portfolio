from src.agents.researcher import ResearcherAgent


def main():
    goal = (
        "Create a launch and pitch strategy for an "
        "AI-powered personalized learning startup."
    )

    task_description = (
        "Research the market, target users, competitors, "
        "trends, opportunities, and risks."
    )

    researcher = ResearcherAgent()

    result = researcher.run(
        goal=goal,
        task_description=task_description,
    )

    print("\n" + "=" * 60)
    print("RESEARCHER RESULT")
    print("=" * 60)

    print(f"\nExecution mode: {researcher.execution_mode}")

    print("\nResearch output:")
    print(result)


if __name__ == "__main__":
    main()