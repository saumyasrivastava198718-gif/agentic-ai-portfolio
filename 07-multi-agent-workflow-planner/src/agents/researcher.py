import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors

from src.tools.web_search import WebSearchTool


class ResearcherAgent:
    """Research agent that combines web retrieval with LLM synthesis."""

    def __init__(self):
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY was not found in the environment."
            )

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.8-flash"

        self.search_tool = WebSearchTool()

        self.execution_mode = "not_started"

    def run(
        self,
        goal: str,
        task_description: str,
    ) -> str:
        """Search the web and synthesize research."""

        print("\nResearcher: gathering web evidence...")

        search_queries = [
            f"{goal} market trends",
            f"{goal} competitors",
            f"{goal} target customers problems",
        ]

        all_results = []

        for query in search_queries:
            print(f"\nSearching: {query}")

            results = self.search_tool.search(
                query=query,
                max_results=3,
            )

            all_results.extend(results)

        if not all_results:
            self.execution_mode = "no_evidence"

            return (
                "Research could not be completed because "
                "web retrieval returned no evidence."
            )

        evidence_text = self._format_evidence(all_results)

        prompt = f"""
You are the Researcher Agent in a multi-agent startup accelerator.

OVERALL USER GOAL:
{goal}

ASSIGNED TASK:
{task_description}

WEB EVIDENCE:
{evidence_text}

Using ONLY the supplied web evidence:

1. Identify likely target customer segments.
2. Identify customer problems.
3. Identify relevant competitor categories or competitors.
4. Identify important market and technology trends.
5. Identify opportunities.
6. Identify risks and uncertainties.

Do not invent facts or statistics.

Clearly distinguish evidence from inference.

Create concise research notes that can be passed
to an Analyst Agent.
"""

        max_attempts = 3

        for attempt in range(1, max_attempts + 1):
            try:
                print(
                    f"\nResearcher: Gemini synthesis "
                    f"attempt {attempt}/{max_attempts}..."
                )

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )

                self.execution_mode = "web+gemini"

                return response.text

            except errors.ServerError as exc:
                print(
                    f"\nResearcher Gemini error "
                    f"{attempt}/{max_attempts}: {exc}"
                )

                if attempt < max_attempts:
                    wait_seconds = 2 ** attempt

                    print(
                        f"Retrying in {wait_seconds} seconds..."
                    )

                    time.sleep(wait_seconds)

            except errors.ClientError as exc:
                print(f"\nGemini API error: {exc}")
                break

        print(
            "\nGemini unavailable. "
            "Preserving web evidence for downstream agents."
        )

        self.execution_mode = "web-only"

        return self._create_web_fallback(all_results)

    def _format_evidence(
        self,
        results: list[dict],
    ) -> str:
        """Convert web results into text for the LLM."""

        evidence_parts = []

        for number, result in enumerate(results, start=1):
            evidence_parts.append(
                f"""
SOURCE {number}
Title: {result["title"]}
URL: {result["url"]}
Snippet: {result["snippet"]}
"""
            )

        return "\n".join(evidence_parts)

    def _create_web_fallback(
        self,
        results: list[dict],
    ) -> str:
        """Preserve retrieved evidence when Gemini is unavailable."""

        output = [
            "RESEARCHER WEB-ONLY FALLBACK MODE",
            "",
            "Gemini synthesis is temporarily unavailable.",
            "The following web evidence was successfully retrieved:",
            "",
        ]

        for number, result in enumerate(results, start=1):
            output.append(
                f"{number}. {result['title']}\n"
                f"   Source: {result['url']}\n"
                f"   Evidence: {result['snippet']}\n"
            )

        output.append(
            "\nThis evidence is being passed downstream "
            "without LLM synthesis."
        )

        return "\n".join(output)