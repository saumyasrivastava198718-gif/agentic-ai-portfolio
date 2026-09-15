from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from src.planner.planner import Planner
from src.agents.researcher import ResearcherAgent
from src.agents.analyst import AnalystAgent
from src.agents.strategist import StrategistAgent
from src.agents.writer import WriterAgent
from src.agents.reviewer import ReviewerAgent


# ============================================================
# 1. SHARED WORKFLOW STATE
# ============================================================

class WorkflowState(TypedDict, total=False):
    """
    Shared state passed between all LangGraph nodes.
    """

    goal: str

    plan: str
    research: str
    analysis: str
    strategy: str
    draft: str

    review_score: float
    review_decision: str
    reviewer_feedback: list[str]

    revision_count: int

    planner_mode: str
    researcher_mode: str
    analyst_mode: str
    strategist_mode: str
    writer_mode: str
    reviewer_mode: str


# ============================================================
# 2. CREATE AGENT OBJECTS
# ============================================================

planner = Planner()
researcher = ResearcherAgent()
analyst = AnalystAgent()
strategist = StrategistAgent()
writer = WriterAgent()
reviewer = ReviewerAgent()


# ============================================================
# 3. PLANNER NODE
# ============================================================

def planner_node(state: WorkflowState) -> dict:
    """Create a workflow plan from the user's goal."""

    print("\n" + "=" * 60)
    print("PLANNER NODE")
    print("=" * 60)

    goal = state["goal"]

    plan = planner.create_plan(goal)

    plan_text = plan.model_dump_json(indent=2)

    return {
        "plan": plan_text,
        "planner_mode": planner.planner_mode,
    }


# ============================================================
# 4. RESEARCHER NODE
# ============================================================

def researcher_node(state: WorkflowState) -> dict:
    """Gather evidence relevant to the startup goal."""

    print("\n" + "=" * 60)
    print("RESEARCHER NODE")
    print("=" * 60)

    goal = state["goal"]

    task_description = (
        "Research the market, target users, competitors, "
        "trends, opportunities, and risks relevant to "
        "the startup goal."
    )

    research = researcher.run(
        goal=goal,
        task_description=task_description,
    )

    return {
        "research": research,
        "researcher_mode": researcher.execution_mode,
    }


# ============================================================
# 5. ANALYST NODE
# ============================================================

def analyst_node(state: WorkflowState) -> dict:
    """Analyze evidence produced by the Researcher."""

    print("\n" + "=" * 60)
    print("ANALYST NODE")
    print("=" * 60)

    analysis = analyst.run(
        goal=state["goal"],
        research=state["research"],
    )

    return {
        "analysis": analysis,
        "analyst_mode": analyst.execution_mode,
    }


# ============================================================
# 6. STRATEGIST NODE
# ============================================================

def strategist_node(state: WorkflowState) -> dict:
    """Turn analysis into an actionable strategy."""

    print("\n" + "=" * 60)
    print("STRATEGIST NODE")
    print("=" * 60)

    strategy = strategist.run(
        goal=state["goal"],
        analysis=state["analysis"],
    )

    return {
        "strategy": strategy,
        "strategist_mode": strategist.execution_mode,
    }


# ============================================================
# 7. WRITER NODE
# ============================================================

def writer_node(state: WorkflowState) -> dict:
    """Create or revise the final startup deliverable."""

    print("\n" + "=" * 60)
    print("WRITER NODE")
    print("=" * 60)

    feedback_list = state.get(
        "reviewer_feedback",
        [],
    )
    reviewer_feedback="/n".join(feedback_list)

    draft = writer.run(
        goal=state["goal"],
        strategy=state["strategy"],

    reviewer_feedback=reviewer_feedback
    )

    current_revision_count = state.get(
        "revision_count",
        0,
    )

    return {
        "draft": draft,
        "writer_mode": writer.execution_mode,
        "revision_count": current_revision_count,
    }


# ============================================================
# 8. REVIEWER NODE
# ============================================================

def reviewer_node(state: WorkflowState) -> dict:
    """Evaluate the Writer's draft."""

    print("\n" + "=" * 60)
    print("REVIEWER NODE")
    print("=" * 60)

    review = reviewer.run(
        goal=state["goal"],
        draft=state["draft"],
    )

    return {
        "review_score": review.score,
        "review_decision": review.decision,
        "reviewer_feedback": review.feedback,
        "reviewer_mode": reviewer.execution_mode,
    }


# ============================================================
# 9. CONDITIONAL ROUTING
# ============================================================

def route_after_review(state: WorkflowState) -> str:
    """
    Decide whether to finish or send the draft
    back to the Writer for revision.
    """

    decision = state.get(
        "review_decision",
        "approve",
    )

    revision_count = state.get(
        "revision_count",
        0,
    )

    max_revisions = 2

    if decision == "approve":
        print("\nReviewer approved the deliverable.")

        return "end"

    if revision_count >= max_revisions:
        print(
            "\nMaximum revision count reached. "
            "Ending workflow."
        )

        return "end"

    print(
        "\nReviewer requested revision. "
        "Returning to Writer."
    )

    return "revise"


# ============================================================
# 10. REVISION NODE
# ============================================================

def revision_node(state: WorkflowState) -> dict:
    """Increment the revision counter."""

    revision_count = state.get(
        "revision_count",
        0,
    )

    revision_count += 1

    print(
        f"\nRevision attempt: {revision_count}"
    )

    return {
        "revision_count": revision_count,
    }


# ============================================================
# 11. BUILD LANGGRAPH
# ============================================================

def build_workflow():
    """Build and compile the multi-agent LangGraph."""

    builder = StateGraph(WorkflowState)

    # Add nodes
    builder.add_node(
        "planner",
        planner_node,
    )

    builder.add_node(
        "researcher",
        researcher_node,
    )

    builder.add_node(
        "analyst",
        analyst_node,
    )

    builder.add_node(
        "strategist",
        strategist_node,
    )

    builder.add_node(
        "writer",
        writer_node,
    )

    builder.add_node(
        "reviewer",
        reviewer_node,
    )

    builder.add_node(
        "revision",
        revision_node,
    )

    # Normal workflow edges
    builder.add_edge(
        START,
        "planner",
    )

    builder.add_edge(
        "planner",
        "researcher",
    )

    builder.add_edge(
        "researcher",
        "analyst",
    )

    builder.add_edge(
        "analyst",
        "strategist",
    )

    builder.add_edge(
        "strategist",
        "writer",
    )

    builder.add_edge(
        "writer",
        "reviewer",
    )

    # Conditional reviewer routing
    builder.add_conditional_edges(
        "reviewer",
        route_after_review,
        {
            "revise": "revision",
            "end": END,
        },
    )

    # Revision returns to Writer
    builder.add_edge(
        "revision",
        "writer",
    )

    # Compile graph
    workflow = builder.compile()

    return workflow


# ============================================================
# 12. CREATE COMPILED WORKFLOW
# ============================================================

workflow = build_workflow()