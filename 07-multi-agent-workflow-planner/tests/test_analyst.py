from src.agents.researcher import ResearcherAgent
from src.agents.analyst import AnalystAgent


def main():
    goal = (
        "Create a launch and pitch strategy for an "
        "AI-powered personalized learning startup."
    )

    research_task = (
        "Research the market, target users, competitors, "
        "trends, opportunities, and risks."
    )

    researcher = ResearcherAgent()

    research = researcher.run(
        goal=goal,
        task_description=research_task,
    )

    print(
        f"\nResearcher mode: "
        f"{researcher.execution_mode}"
    )

    analyst = AnalystAgent()

    analysis = analyst.run(
        goal=goal,
        research=research,
    )

    print("\n" + "=" * 60)
    print("ANALYST RESULT")
    print("=" * 60)

    print(
        f"\nAnalyst mode: "
        f"{analyst.execution_mode}"
    )

    print("\nAnalysis output:")
    print(analysis)


if __name__ == "__main__":
    main()