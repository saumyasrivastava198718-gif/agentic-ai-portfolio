import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors

from src.models.schemas import ReviewDecision


class ReviewerAgent:
    """Evaluates the Writer Agent's deliverable."""

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
        draft: str,
    ) -> ReviewDecision:
        """Review a draft and decide whether to approve or revise."""

        prompt = f"""
You are the Reviewer Agent in a multi-agent startup accelerator.

OVERALL USER GOAL:
{goal}

DRAFT:
{draft}

Evaluate the draft for:

1. Relevance to the user goal
2. Clarity
3. Internal consistency
4. Actionability
5. Unsupported claims
6. Appropriate risk disclosure
7. Overall usefulness

Return:

- score: number from 0 to 10
- decision: "approve" or "revise"
- feedback: concise actionable feedback

Approve only when the document is sufficiently clear,
grounded, consistent, and useful.
"""

        max_attempts = 3

        for attempt in range(1, max_attempts + 1):
            try:
                print(
                    f"\nReviewer: Gemini review "
                    f"attempt {attempt}/{max_attempts}..."
                )

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config={
                        "response_mime_type": "application/json",
                        "response_json_schema":
                            ReviewDecision.model_json_schema(),
                    },
                )

                decision = ReviewDecision.model_validate_json(
                    response.text
                )

                self.execution_mode = "gemini"

                return decision

            except errors.ServerError as exc:
                print(
                    f"\nReviewer Gemini error "
                    f"{attempt}/{max_attempts}: {exc}"
                )

                if attempt < max_attempts:
                    wait_seconds = 2 ** attempt

                    print(
                        f"Retrying Reviewer in "
                        f"{wait_seconds} seconds..."
                    )

                    time.sleep(wait_seconds)

            except errors.ClientError as exc:
                print(
                    f"\nReviewer Gemini API error: {exc}"
                )
                break

        print(
            "\nGemini unavailable for Reviewer. "
            "Using deterministic review."
        )

        return self._fallback_review(draft)

    def _fallback_review(
        self,
        draft: str,
    ) -> ReviewDecision:
        """Perform basic deterministic quality checks."""

        self.execution_mode = "deterministic"

        score = 5.0
        feedback = []

        draft_lower = draft.lower()

        if len(draft) >= 500:
            score += 1.0
        else:
            feedback.append(
                "The deliverable may need more detail."
            )

        if "goal" in draft_lower:
            score += 0.5
        else:
            feedback.append(
                "Make the overall goal clearer."
            )

        if "strategy" in draft_lower:
            score += 0.5
        else:
            feedback.append(
                "Add a clearer strategy section."
            )

        if "risk" in draft_lower:
            score += 1.0
        else:
            feedback.append(
                "Add explicit risks and assumptions."
            )

        if "validation" in draft_lower:
            score += 1.0
        else:
            feedback.append(
                "Add a validation plan."
            )

        score = min(score, 10.0)

        if score >= 7.0:
            decision = "approve"
        else:
            decision = "revise"

        if not feedback:
            feedback.append(
                "Draft passed the deterministic quality checks."
            )

        return ReviewDecision(
            score=score,
            decision=decision,
            feedback=feedback,
        )