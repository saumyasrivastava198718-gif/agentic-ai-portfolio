import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors


class WriterAgent:
    """Creates the final startup deliverable from strategy."""

    def __init__(self):
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY was not found in the environment."
            )

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.8-flash"
        self.execution_mode = "not_started"

    def run(
        self,
        goal: str,
        strategy: str,
        reviewer_feedback: str = "",
    ) -> str:
        """Create or revise a polished deliverable."""

        prompt = f"""
You are the Writer Agent in a multi-agent startup accelerator.

OVERALL USER GOAL:
{goal}

STRATEGY:
{strategy}

REVIEWER FEEDBACK:
{reviewer_feedback if reviewer_feedback else "No previous feedback."}

Create a concise professional startup launch and pitch document.

Include:

1. Executive Summary
2. Target Customer
3. Customer Problem
4. Value Proposition
5. Product Positioning
6. Go-to-Market Strategy
7. Recommended Actions
8. Risks and Assumptions
9. Validation Plan

Use only information supported by the supplied strategy.

Do not invent statistics, customers, partnerships,
funding, revenue, or market facts.

If reviewer feedback is provided, improve the document
according to that feedback.
"""

        max_attempts = 3

        for attempt in range(1, max_attempts + 1):
            try:
                print(
                    f"\nWriter: Gemini writing "
                    f"attempt {attempt}/{max_attempts}..."
                )

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )

                self.execution_mode = "gemini"

                return response.text

            except errors.ServerError as exc:
                print(
                    f"\nWriter Gemini error "
                    f"{attempt}/{max_attempts}: {exc}"
                )

                if attempt < max_attempts:
                    wait_seconds = 2 ** attempt

                    print(
                        f"Retrying Writer in "
                        f"{wait_seconds} seconds..."
                    )

                    time.sleep(wait_seconds)

            except errors.ClientError as exc:
                print(
                    f"\nWriter Gemini API error: {exc}"
                )
                break

        print(
            "\nGemini unavailable for Writer. "
            "Using deterministic writer fallback."
        )

        return self._fallback_write(
            goal=goal,
            strategy=strategy,
            reviewer_feedback=reviewer_feedback,
        )

    def _fallback_write(
        self,
        goal: str,
        strategy: str,
        reviewer_feedback: str = "",
    ) -> str:
        """Create a structured deliverable without LLM reasoning."""

        self.execution_mode = "deterministic"

        feedback_section = (
            reviewer_feedback
            if reviewer_feedback
            else "No reviewer feedback was supplied."
        )

        return f"""
STARTUP STRATEGY DELIVERABLE
============================

GOAL
----
{goal}

EXECUTIVE SUMMARY
-----------------
This document presents a strategy generated from
research and analysis produced by the multi-agent workflow.

STRATEGY
--------
{strategy}

VALIDATION PLAN
---------------
1. Validate the proposed customer segment.
2. Interview representative users.
3. Test the main customer problem.
4. Build a small MVP.
5. Measure user response and usefulness.
6. Review risks before scaling.
7. Update the strategy using validated evidence.

REVIEW CONTEXT
--------------
{feedback_section}

SYSTEM NOTE
-----------
Gemini generation was unavailable.

This document was assembled using deterministic Python
logic. No additional market statistics or unsupported
facts were invented.
"""