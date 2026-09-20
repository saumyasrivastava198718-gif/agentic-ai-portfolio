from src.models.schemas import (
    ActionPreview,
    AgentProposal,
    EvidenceItem,
    TrustRequest,
)


def build_fallback_proposal(
    request: TrustRequest,
    evidence: list[EvidenceItem],
) -> AgentProposal:
    """Build a safe proposal when the LLM is unavailable."""

    return AgentProposal(
        summary=(
            "Review diversification, concentration, liquidity "
            "and time-horizon considerations before making "
            "any portfolio decision."
        ),

        reasoning_summary=[
            (
                "Relevant financial principles were retrieved "
                "from the controlled knowledge base."
            ),
            (
                "Potential risks should be reviewed before "
                "any action is considered."
            ),
            (
                "This prototype requires explicit human "
                "authorization."
            ),
        ],

        evidence=evidence,

        assumptions=[
            "The scenario is hypothetical.",
            (
                "No complete investor suitability assessment "
                "has been performed."
            ),
            (
                "Information supplied to the prototype may "
                "be incomplete."
            ),
        ],

        risks=[
            "Investment values can rise or fall.",
            (
                "Portfolio changes can involve taxes, fees "
                "or other consequences."
            ),
            (
                "Incomplete information can lead to "
                "inappropriate conclusions."
            ),
        ],

        proposed_actions=[
            ActionPreview(
                action="review_portfolio_risk",
                description=(
                    "Review concentration, diversification, "
                    "liquidity and time-horizon factors. "
                    "No transaction will be executed."
                ),
                reversible=True,
                requires_human_approval=True,
            )
        ],

        confidence=0.60,

        execution_status="awaiting_approval",
    )