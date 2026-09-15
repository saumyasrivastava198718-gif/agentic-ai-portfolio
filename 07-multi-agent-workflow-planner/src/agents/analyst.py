import os
import re
import time
from collections import Counter

from dotenv import load_dotenv
from google import genai
from google.genai import errors


class AnalystAgent:
    """Analyzes research evidence and extracts strategic insights."""

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
        research: str,
    ) -> str:
        """Analyze research produced by the Researcher Agent."""

        prompt = f"""
You are the Analyst Agent in a multi-agent startup accelerator.

OVERALL GOAL:
{goal}

RESEARCH PROVIDED BY THE RESEARCHER:
{research}

Analyze ONLY the supplied research.

Identify:

1. Key insights
2. Customer needs and pain points
3. Market opportunities
4. Competitive patterns
5. Business risks
6. Technical risks
7. Important uncertainties
8. Evidence gaps that require further validation

Do not invent statistics or unsupported facts.

Produce concise analysis that can be passed
to the Strategist Agent.
"""

        max_attempts = 3

        for attempt in range(1, max_attempts + 1):
            try:
                print(
                    f"\nAnalyst: Gemini analysis "
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
                    f"\nAnalyst Gemini error "
                    f"{attempt}/{max_attempts}: {exc}"
                )

                if attempt < max_attempts:
                    wait_seconds = 2 ** attempt

                    print(
                        f"Retrying Analyst in "
                        f"{wait_seconds} seconds..."
                    )

                    time.sleep(wait_seconds)

            except errors.ClientError as exc:
                print(
                    f"\nAnalyst Gemini API error: {exc}"
                )
                break

        print(
            "\nGemini unavailable for Analyst. "
            "Using deterministic Python analysis."
        )

        return self._fallback_analysis(research)

    def _fallback_analysis(
        self,
        research: str,
    ) -> str:
        """Perform lightweight deterministic analysis without an LLM."""

        self.execution_mode = "deterministic"

        text = research.lower()

        words = re.findall(
            r"\b[a-zA-Z]{4,}\b",
            text,
        )

        stop_words = {
            "this",
            "that",
            "with",
            "from",
            "your",
            "have",
            "will",
            "into",
            "about",
            "their",
            "they",
            "been",
            "were",
            "when",
            "what",
            "source",
            "evidence",
            "https",
            "www",
            "researcher",
            "fallback",
            "mode",
        }

        useful_words = [
            word
            for word in words
            if word not in stop_words
        ]

        common_terms = Counter(
            useful_words
        ).most_common(10)

        categories = {
            "customer_signals": [
                "customer",
                "student",
                "learner",
                "teacher",
                "school",
                "user",
            ],
            "competition_signals": [
                "competitor",
                "competition",
                "startup",
                "platform",
                "market",
            ],
            "opportunity_signals": [
                "growth",
                "opportunity",
                "adoption",
                "personalized",
                "automation",
                "innovation",
            ],
            "risk_signals": [
                "risk",
                "cost",
                "privacy",
                "security",
                "compliance",
                "accuracy",
            ],
            "technology_signals": [
                "artificial",
                "intelligence",
                "machine",
                "learning",
                "generative",
                "automation",
            ],
        }

        detected = {}

        for category, keywords in categories.items():
            found = [
                keyword
                for keyword in keywords
                if keyword in text
            ]

            detected[category] = found

        if common_terms:
            term_text = "\n".join(
                f"- {term}: {count}"
                for term, count in common_terms
            )
        else:
            term_text = "- No recurring terms detected"

        category_lines = []

        for category, found in detected.items():
            label = category.replace(
                "_",
                " ",
            ).title()

            values = (
                ", ".join(found)
                if found
                else "None detected"
            )

            category_lines.append(
                f"{label}: {values}"
            )

        category_text = "\n".join(
            category_lines
        )

        return f"""
DETERMINISTIC ANALYST FALLBACK

Gemini reasoning was unavailable.

Python performed lightweight evidence analysis instead.

TOP RECURRING TERMS
-------------------
{term_text}

DETECTED EVIDENCE CATEGORIES
----------------------------
{category_text}

INTERPRETATION
--------------
These signals were extracted directly from the
research evidence.

No new market facts or statistics were invented.

This deterministic analysis is less sophisticated
than LLM semantic reasoning, but it provides
structured signals that can safely continue to
the Strategist Agent.
"""