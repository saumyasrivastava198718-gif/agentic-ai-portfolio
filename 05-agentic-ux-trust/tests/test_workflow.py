from src.agent.fallback import (
    build_fallback_proposal,
)
from src.evaluation.evaluator import (
    evaluate_proposal,
)
from src.models.schemas import (
    EvidenceItem,
    HumanDecision,
    TrustRequest,
)
from src.workflow.trust_workflow import (
    apply_human_decision,
)


def create_test_proposal():
    request = TrustRequest(
        question=(
            "What risks should be reviewed "
            "for this portfolio?"
        ),
        scenario=(
            "This hypothetical portfolio "
            "has concentration risk."
        ),
    )

    evidence = [
        EvidenceItem(
            source_id="test",
            title="Test Evidence",
            text=(
                "Diversification can reduce "
                "concentration risk."
            ),
            score=0.9,
        )
    ]

    return build_fallback_proposal(
        request,
        evidence,
    )


def test_proposal_requires_approval():
    proposal = create_test_proposal()

    assert (
        proposal.execution_status
        == "awaiting_approval"
    )

    assert all(
        action.requires_human_approval
        for action
        in proposal.proposed_actions
    )


def test_cancel_stops_action():
    proposal = create_test_proposal()

    decision = HumanDecision(
        decision="cancel"
    )

    updated = (
        apply_human_decision(
            proposal,
            decision,
        )
    )

    assert (
        updated.execution_status
        == "cancelled"
    )


def test_override_changes_action():
    proposal = create_test_proposal()

    decision = HumanDecision(
        decision="override",
        override_instruction=(
            "Only review concentration risk."
        ),
    )

    updated = (
        apply_human_decision(
            proposal,
            decision,
        )
    )

    assert (
        updated.execution_status
        == "overridden"
    )

    assert (
        updated.proposed_actions[
            0
        ].description
        == "Only review concentration risk."
    )


def test_evaluation_passes_safe_proposal():
    proposal = create_test_proposal()

    result = evaluate_proposal(
        proposal
    )

    assert result["passed"] is True