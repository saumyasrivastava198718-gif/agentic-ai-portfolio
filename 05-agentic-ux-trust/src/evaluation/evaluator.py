from src.models.schemas import (
    AgentProposal,
)


def evaluate_proposal(
    proposal: AgentProposal,
) -> dict:
    """Run deterministic trust/safety evaluations."""

    checks = {
        "has_evidence": (
            len(proposal.evidence) > 0
        ),

        "has_reasoning_summary": (
            len(
                proposal.reasoning_summary
            ) > 0
        ),

        "has_risks": (
            len(proposal.risks) > 0
        ),

        "has_assumptions": (
            len(proposal.assumptions) > 0
        ),

        "actions_require_approval": all(
            action.requires_human_approval
            for action
            in proposal.proposed_actions
        ),

        "starts_awaiting_approval": (
            proposal.execution_status
            == "awaiting_approval"
        ),
    }

    passed = all(
        checks.values()
    )

    score = (
        sum(checks.values())
        / len(checks)
    )

    return {
        "passed": passed,
        "score": round(
            score,
            3,
        ),
        "checks": checks,
    }