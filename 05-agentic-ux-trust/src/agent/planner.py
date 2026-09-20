import os

from dotenv import load_dotenv
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
)

from src.agent.fallback import (
    build_fallback_proposal,
)
from src.models.schemas import (
    AgentProposal,
    EvidenceItem,
    TrustRequest,
)


load_dotenv()


def _format_evidence(
    evidence: list[EvidenceItem],
) -> str:
    """Convert evidence objects into prompt context."""

    return "\n\n".join(
        (
            f"[{item.source_id}] {item.title}\n"
            f"{item.text}"
        )
        for item in evidence
    )


def generate_proposal(
    request: TrustRequest,
    evidence: list[EvidenceItem],
) -> tuple[AgentProposal, str, str | None]:
    """
    Generate a structured proposal.

    Returns:
        proposal,
        execution mode,
        provider error if fallback was required.
    """

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key:
        proposal = build_fallback_proposal(
            request,
            evidence,
        )

        return (
            proposal,
            "deterministic_fallback",
            "GEMINI_API_KEY not configured.",
        )

    try:
        model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.6-flash",
        )

        llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            max_retries=2,
        )

        structured_llm = (
            llm.with_structured_output(
                AgentProposal
            )
        )

        prompt = f"""
You are a trust-focused financial decision-support
planning agent.

You do NOT execute financial transactions.

Your purpose is to create a transparent ACTION PREVIEW
that a human can inspect before deciding whether to
approve, override, or cancel it.

USER QUESTION:
{request.question}

SCENARIO:
{request.scenario}

RETRIEVED EVIDENCE:
{_format_evidence(evidence)}

REQUIREMENTS:

1. Ground the proposal in the supplied evidence.
2. Never fabricate sources.
3. Keep reasoning_summary concise and user-facing.
4. Do not reveal hidden chain-of-thought.
5. State assumptions explicitly.
6. State material risks explicitly.
7. Proposed actions are previews only.
8. Every action requires human approval.
9. Do not claim guaranteed financial outcomes.
10. Do not claim to have executed a transaction.
11. execution_status must be "awaiting_approval".
12. confidence is an interface indicator, not a
    guaranteed probability of correctness.

Return a valid AgentProposal.
"""

        proposal = structured_llm.invoke(
            prompt
        )

        # Evidence comes from our retriever rather than
        # allowing the LLM to invent source objects.
        proposal.evidence = evidence

        proposal.execution_status = (
            "awaiting_approval"
        )

        for action in proposal.proposed_actions:
            action.requires_human_approval = True

        return (
            proposal,
            "llm",
            None,
        )

    except Exception as error:
        proposal = build_fallback_proposal(
            request,
            evidence,
        )

        return (
            proposal,
            "deterministic_fallback",
            f"{type(error).__name__}: {error}",
        )