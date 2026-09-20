from typing import Literal

from pydantic import BaseModel, Field


class TrustRequest(BaseModel):
    """Validated user request."""

    question: str = Field(
        ...,
        min_length=10,
        max_length=1000,
    )

    scenario: str = Field(
        ...,
        min_length=10,
        max_length=3000,
    )


class EvidenceItem(BaseModel):
    """One piece of retrieved evidence."""

    source_id: str
    title: str
    text: str

    score: float = Field(
        ge=0.0,
        le=1.0,
    )


class ActionPreview(BaseModel):
    """Action proposed by the agent."""

    action: str
    description: str

    reversible: bool = True

    requires_human_approval: bool = True


class AgentProposal(BaseModel):
    """Structured output produced by the planning agent."""

    summary: str

    reasoning_summary: list[str]

    evidence: list[EvidenceItem]

    assumptions: list[str]

    risks: list[str]

    proposed_actions: list[ActionPreview]

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    execution_status: Literal[
        "awaiting_approval",
        "approved",
        "cancelled",
        "overridden",
    ] = "awaiting_approval"


class HumanDecision(BaseModel):
    """Human response to the agent proposal."""

    decision: Literal[
        "approve",
        "cancel",
        "override",
    ]

    override_instruction: str = ""