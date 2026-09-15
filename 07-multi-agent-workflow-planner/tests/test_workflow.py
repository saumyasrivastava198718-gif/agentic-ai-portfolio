from src.orchestration.workflow import workflow


def main():
    """Run the complete multi-agent workflow."""

    goal = (
        "Create a launch and pitch strategy for an "
        "AI-powered personalized learning startup."
    )

    print("\n" + "=" * 70)
    print("STARTING MULTI-AGENT WORKFLOW")
    print("=" * 70)

    print(f"\nGoal:\n{goal}")

    initial_state = {
        "goal": goal,
        "revision_count": 0,
    }

    result = workflow.invoke(initial_state)

    print("\n" + "=" * 70)
    print("WORKFLOW COMPLETED")
    print("=" * 70)

    print("\nEXECUTION MODES")
    print("-" * 40)

    print(
        "Planner:",
        result.get("planner_mode", "unknown"),
    )

    print(
        "Researcher:",
        result.get("researcher_mode", "unknown"),
    )

    print(
        "Analyst:",
        result.get("analyst_mode", "unknown"),
    )

    print(
        "Strategist:",
        result.get("strategist_mode", "unknown"),
    )

    print(
        "Writer:",
        result.get("writer_mode", "unknown"),
    )

    print(
        "Reviewer:",
        result.get("reviewer_mode", "unknown"),
    )

    print("\n" + "=" * 70)
    print("REVIEW RESULT")
    print("=" * 70)

    print(
        "\nScore:",
        result.get("review_score", "N/A"),
    )

    print(
        "Decision:",
        result.get("review_decision", "N/A"),
    )

    print(
        "Revision count:",
        result.get("revision_count", 0),
    )

    print(
        "\nReviewer feedback:"
    )

    print(
        result.get(
            "reviewer_feedback",
            "No feedback available.",
        )
    )

    print("\n" + "=" * 70)
    print("FINAL DELIVERABLE")
    print("=" * 70)

    print(
        result.get(
            "draft",
            "No final draft was produced.",
        )
    )


if __name__ == "__main__":
    main()