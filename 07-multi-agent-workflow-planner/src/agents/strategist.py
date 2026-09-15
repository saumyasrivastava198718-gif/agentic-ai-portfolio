import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors


class StrategistAgent:
    """Turns research analysis into an actionable startup strategy."""

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
        analysis: str,
    ) -> str:
        """Create strategy from the Analyst Agent's output."""

        prompt = f"""
You are the Strategist Agent in a multi-agent startup accelerator.

OVERALL USER GOAL:
{goal}

ANALYSIS PROVIDED BY THE ANALYST:
{analysis}

Using ONLY the supplied analysis, create an actionable strategy.

Cover:

1. Target customer
2. Core customer problem
3. Value proposition
4. Product positioning
5. Go-to-market approach
6. Recommended actions
7. Key risks
8. Assumptions that require validation

Do not invent market statistics or unsupported facts.

Clearly distinguish recommendations from known evidence.

Produce a concise strategy that can be passed
to the Writer Agent.
"""

        max_attempts = 3

        for attempt in range(1, max_attempts + 1):
            try:
                print(
                    f"\nStrategist: Gemini strategy "
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
                    f"\nStrategist Gemini error "
                    f"{attempt}/{max_attempts}: {exc}"
                )

                if attempt < max_attempts:
                    wait_seconds = 2 ** attempt

                    print(
                        f"Retrying Strategist in "
                        f"{wait_seconds} seconds..."
                    )

                    time.sleep(wait_seconds)

            except errors.ClientError as exc:
                print(
                    f"\nStrategist Gemini API error: {exc}"
                )
                break

        print(
            "\nGemini unavailable for Strategist. "
            "Using deterministic strategy fallback."
        )

        return self._fallback_strategy(
            goal=goal,
            analysis=analysis,
        )

    def _fallback_strategy(
        self,
        goal: str,
        analysis: str,
    ) -> str:
        """Create a conservative strategy without LLM reasoning."""

        self.execution_mode = "deterministic"

        analysis_lower = analysis.lower()

        customer_signals = []
        opportunity_signals = []
        risk_signals = []

        customer_keywords = [
            "student",
            "learner",
            "teacher",
            "school",
            "customer",
            "user",
        ]

        opportunity_keywords = [
            "personalized",
            "growth",
            "adoption",
            "automation",
            "innovation",
            "learning",
        ]

        risk_keywords = [
            "privacy",
            "security",
            "cost",
            "accuracy",
            "compliance",
            "risk",
        ]

        for keyword in customer_keywords:
            if keyword in analysis_lower:
                customer_signals.append(keyword)

        for keyword in opportunity_keywords:
            if keyword in analysis_lower:
                opportunity_signals.append(keyword)

        for keyword in risk_keywords:
            if keyword in analysis_lower:
                risk_signals.append(keyword)

        customers = (
            ", ".join(customer_signals)
            if customer_signals
            else "Requires validation"
        )

        opportunities = (
            ", ".join(opportunity_signals)
            if opportunity_signals
            else "Requires validation"
        )

        risks = (
            ", ".join(risk_signals)
            if risk_signals
            else "Requires validation"
        )

        return f"""
DETERMINISTIC STRATEGIST FALLBACK

Goal
----
{goal}

Target-Customer Signals
-----------------------
{customers}

Opportunity Signals
-------------------
{opportunities}

Risk Signals
------------
{risks}

Conservative Strategy
---------------------
1. Validate the strongest customer segment before scaling.
2. Confirm the highest-priority customer problem through
   direct user research.
3. Build a small MVP around the strongest validated need.
4. Test the value proposition with early users.
5. Measure engagement, usefulness, and retention.
6. Iterate using evidence rather than unsupported assumptions.
7. Review privacy, security, cost, and accuracy risks
   before wider deployment.

Important:
This strategy was generated using deterministic rules because
LLM reasoning was unavailable. It does not introduce new
market facts or statistics.

The original Analyst output remains available to downstream
agents for additional context.

ANALYST INPUT
-------------
{analysis}
"""