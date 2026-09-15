from typing import Literal
from pydantic import BaseModel, Field


class Task(BaseModel):
    """A single task created by the planner."""

    title: str = Field(
        description="Short name of the task"
    )

    description: str = Field(
        description="Clear instructions for completing the task"
    )

    assigned_agent: Literal[
        "researcher",
        "analyst",
        "strategist",
        "writer",
        "reviewer",
    ] = Field(
        description="Agent responsible for this task"
    )


class WorkflowPlan(BaseModel):
    """Structured plan produced by the planner."""

    goal: str = Field(
        description="The user's overall objective"
    )

    tasks: list[Task] = Field(
        description="Ordered tasks required to achieve the goal"
    )


class ResearchResult(BaseModel):
    """Structured output produced by the researcher."""

    summary: str
    findings: list[str]
    sources: list[str] = Field(default_factory=list)


class AnalysisResult(BaseModel):
    """Structured output produced by the analyst."""

    key_insights: list[str]
    opportunities: list[str]
    risks: list[str]


class StrategyResult(BaseModel):
    """Structured output produced by the strategist."""

    target_customer: str
    value_proposition: str
    recommendations: list[str]


class DraftResult(BaseModel):
    """Structured draft produced by the writer."""

    title: str
    content: str


class ReviewDecision(BaseModel):
    """Quality decision produced by the reviewer."""

    score: float = Field(ge=0.0, le=10.0)
    decision: Literal["approve", "revise"]
    feedback: list[str] = Field(default_factory=list)