from typing import Literal

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field


load_dotenv()


class RouteDecision(BaseModel):
    route: Literal["pdf", "web", "hybrid"]
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str


class Router:
    def __init__(self):
        self.client = genai.Client()

    def _deterministic_route(
        self,
        question: str
    ) -> RouteDecision | None:

        q = question.lower()

        hybrid_words = [
            "changed since",
            "compare with current",
            "compared with current",
            "since the report",
            "after the report",
            "report vs today",
            "report versus today"
        ]

        web_words = [
            "latest",
            "today",
            "current",
            "recent",
            "this week",
            "this month",
            "new announcement",
            "breaking"
        ]

        pdf_words = [
            "annual report",
            "according to the report",
            "in the report",
            "what does the report say"
        ]

        if any(word in q for word in hybrid_words):
            return RouteDecision(
                route="hybrid",
                confidence=0.95,
                reason=(
                    "Deterministic routing detected a question "
                    "requiring both document and current information."
                )
            )

        if any(word in q for word in web_words):
            return RouteDecision(
                route="web",
                confidence=0.95,
                reason=(
                    "Deterministic routing detected a request "
                    "for current or recent information."
                )
            )

        if any(word in q for word in pdf_words):
            return RouteDecision(
                route="pdf",
                confidence=0.95,
                reason=(
                    "Deterministic routing detected a question "
                    "about the indexed annual report."
                )
            )

        return None

    def _fallback_route(
        self,
        question: str
    ) -> RouteDecision:

        return RouteDecision(
            route="pdf",
            confidence=0.70,
            reason=(
                "Gemini routing was unavailable, so the "
                "fallback selected the indexed PDF knowledge base."
            )
        )

    def route(
        self,
        question: str
    ) -> RouteDecision:

        deterministic = self._deterministic_route(
            question
        )

        if deterministic is not None:
            return deterministic

        prompt = f"""
You are the routing agent for an AI research assistant.

Choose exactly one route:

pdf:
Use when the question can be answered from the indexed document.

web:
Use when the question requires recent, current, or external information.

hybrid:
Use when BOTH document information and current web information
are required.

Return:
- route
- confidence between 0 and 1
- short reason

Question:
{question}
"""

        try:

            interaction = self.client.interactions.create(
                model="gemini-3.8-flash",
                input=prompt,
                response_format={
                    "type": "text",
                    "mime_type": "application/json",
                    "schema": RouteDecision.model_json_schema()
                }
            )

            return RouteDecision.model_validate_json(
                interaction.output_text
            )

        except Exception as error:

            print(
                f"\nGemini router unavailable. "
                f"Using fallback router.\n"
                f"Reason: {type(error).__name__}\n"
            )

            return self._fallback_route(
                question
            )