from src.agent.planner import (
    generate_proposal,
)
from src.guardrails.safety import (
    validate_request,
)
from src.models.schemas import (
    AgentProposal,
    HumanDecision,
    TrustRequest,
)
from src.monitoring.telemetry import (
    RunTracker,
)
from src.retrieval.retriever import (
    retrieve_evidence,
)


def create_proposal(
    request: TrustRequest,
) -> tuple[AgentProposal, dict]:
    """Run the complete agent planning workflow."""

    tracker = RunTracker()

    allowed, message = validate_request(
        request
    )

    if not allowed:
        tracker.finish(
            mode="blocked",
            status="blocked",
            evidence_count=0,
            provider_error=message,
        )

        raise ValueError(message)

    query = (
        request.question
        + " "
        + request.scenario
    )

    evidence = retrieve_evidence(
        query=query,
        top_k=3,
    )

    (
        proposal,
        mode,
        provider_error,
    ) = generate_proposal(
        request=request,
        evidence=evidence,
    )

    metrics = tracker.finish(
        mode=mode,
        status="success",
        evidence_count=len(evidence),
        provider_error=provider_error,
    )

    return (
        proposal,
        metrics,
    )


def apply_human_decision(
    proposal: AgentProposal,
    decision: HumanDecision,
) -> AgentProposal:
    """Apply the human-in-the-loop decision."""

    if decision.decision == "approve":
        proposal.execution_status = (
            "approved"
        )

    elif decision.decision == "cancel":
        proposal.execution_status = (
            "cancelled"
        )

    elif decision.decision == "override":
        instruction = (
            decision.override_instruction.strip()
        )

        if not instruction:
            raise ValueError(
                "Override requires an instruction."
            )

        proposal.execution_status = (
            "overridden"
        )

        if proposal.proposed_actions:
            proposal.proposed_actions[
                0
            ].description = instruction

    return proposal