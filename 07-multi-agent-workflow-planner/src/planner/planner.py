import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors

from src.models.schemas import Task, WorkflowPlan


class Planner:
    """Creates a structured workflow plan from a user's goal."""

    def __init__(self):
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY was not found in the environment."
            )

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.8-flash"
        self.planner_mode = "not_started"

    def create_plan(self, goal: str) -> WorkflowPlan:
        """Create a plan using Gemini, with retry and fallback."""

        prompt = f"""
You are the planner for a multi-agent startup accelerator.

USER GOAL:
{goal}

Create an ordered workflow using these specialist agents:

1. researcher
   Gathers factual market and competitor information.

2. analyst
   Identifies patterns, opportunities, risks, and important insights.

3. strategist
   Develops positioning, recommendations, and strategic direction.

4. writer
   Creates the final startup or pitch deliverable.

5. reviewer
   Evaluates the final deliverable and provides feedback.

Create clear tasks in a logical order.

Use only these agent roles:
researcher, analyst, strategist, writer, reviewer.
"""

        max_attempts = 3

        for attempt in range(1, max_attempts + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config={
                        "response_mime_type": "application/json",
                        "response_json_schema": (
                            WorkflowPlan.model_json_schema()
                        ),
                    },
                )

                plan = WorkflowPlan.model_validate_json(
                    response.text
                )

                self.planner_mode = "gemini"

                print("\nPlanner mode: GEMINI")

                return plan

            except errors.ServerError as exc:
                print(
                    f"\nGemini server error on attempt "
                    f"{attempt}/{max_attempts}: {exc}"
                )

                if attempt < max_attempts:
                    wait_seconds = 2 ** attempt

                    print(
                        f"Retrying in {wait_seconds} seconds..."
                    )

                    time.sleep(wait_seconds)

            except errors.ClientError as exc:
                print(f"\nGemini API/client error: {exc}")
                print(
                    "Switching to deterministic fallback planner."
                )

                return self._create_fallback_plan(goal)

        print(
            "\nGemini remained unavailable after all retries."
        )
        print(
            "Switching to deterministic fallback planner."
        )

        return self._create_fallback_plan(goal)

    def _create_fallback_plan(
        self,
        goal: str,
    ) -> WorkflowPlan:
        """Create a deterministic workflow without an LLM."""

        self.planner_mode = "fallback"

        tasks = [
            Task(
                title="Market and Competitor Research",
                description=(
                    "Research the market, target users, competitors, "
                    "trends, and relevant facts for the goal: "
                    f"{goal}"
                ),
                assigned_agent="researcher",
            ),
            Task(
                title="Research Analysis",
                description=(
                    "Analyze the research to identify patterns, "
                    "opportunities, risks, and important insights."
                ),
                assigned_agent="analyst",
            ),
            Task(
                title="Strategy Development",
                description=(
                    "Develop positioning, recommendations, priorities, "
                    "and an actionable strategy."
                ),
                assigned_agent="strategist",
            ),
            Task(
                title="Final Deliverable",
                description=(
                    "Create a professional final deliverable using "
                    "the research, analysis, and strategy."
                ),
                assigned_agent="writer",
            ),
            Task(
                title="Quality Review",
                description=(
                    "Review the deliverable for accuracy, clarity, "
                    "completeness, consistency, and actionability."
                ),
                assigned_agent="reviewer",
            ),
        ]

        return WorkflowPlan(
            goal=goal,
            tasks=tasks,
        )