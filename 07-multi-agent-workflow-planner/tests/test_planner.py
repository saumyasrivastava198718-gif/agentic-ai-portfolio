from src.planner.planner import Planner


def main():
    planner = Planner()

    goal = (
        "Create a launch and pitch strategy for an "
        "AI-powered personalized learning startup."
    )

    plan = planner.create_plan(goal)

    print("\nGOAL:")
    print(plan.goal)

    print("\nTASKS:")

    for number, task in enumerate(plan.tasks, start=1):
        print(f"\n{number}. {task.title}")
        print(f"   Agent: {task.assigned_agent}")
        print(f"   Description: {task.description}")


if __name__ == "__main__":
    main()