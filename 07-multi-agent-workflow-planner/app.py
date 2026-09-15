import streamlit as st

from src.orchestration.workflow import workflow


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Multi-Agent Startup Accelerator",
    page_icon="🤖",
    layout="wide",
)


# ============================================================
# HEADER
# ============================================================

st.title("🤖 Multi-Agent Startup Accelerator")

st.markdown(
    """
    Enter a startup goal and let a LangGraph-powered
    multi-agent workflow research, analyze, strategize,
    write, and review a launch plan.
    """
)

st.info(
    "The system uses Gemini when available and automatically "
    "falls back to deterministic processing when the model "
    "is unavailable or quota-limited."
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.header("🧠 Agent Workflow")

    st.markdown(
        """
        **1. Planner**  
        Breaks the goal into tasks.

        **2. Researcher**  
        Searches the web and gathers evidence.

        **3. Analyst**  
        Extracts insights and signals.

        **4. Strategist**  
        Converts analysis into recommendations.

        **5. Writer**  
        Creates the final deliverable.

        **6. Reviewer**  
        Scores and reviews the output.

        **Orchestrator:** LangGraph
        """
    )

    st.divider()

    st.caption(
        "Built as an Agentic AI portfolio project."
    )


# ============================================================
# USER INPUT
# ============================================================

default_goal = (
    "Create a launch and pitch strategy for an "
    "AI-powered personalized learning startup."
)

goal = st.text_area(
    "🎯 Startup Goal",
    value=default_goal,
    height=120,
    help="Describe the startup problem or goal.",
)


# ============================================================
# RUN WORKFLOW
# ============================================================

if st.button(
    "🚀 Run Multi-Agent Workflow",
    type="primary",
    use_container_width=True,
):

    if not goal.strip():
        st.warning(
            "Please enter a startup goal before running."
        )

    else:
        try:
            with st.spinner(
                "Agents are collaborating..."
            ):
                initial_state = {
                    "goal": goal.strip(),
                    "revision_count": 0,
                }

                result = workflow.invoke(
                    initial_state
                )

            st.success(
                "✅ Multi-agent workflow completed!"
            )

            # =================================================
            # EXECUTION MODES
            # =================================================

            st.subheader("⚙️ Agent Execution Modes")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Planner",
                    result.get(
                        "planner_mode",
                        "unknown",
                    ),
                )

                st.metric(
                    "Researcher",
                    result.get(
                        "researcher_mode",
                        "unknown",
                    ),
                )

            with col2:
                st.metric(
                    "Analyst",
                    result.get(
                        "analyst_mode",
                        "unknown",
                    ),
                )

                st.metric(
                    "Strategist",
                    result.get(
                        "strategist_mode",
                        "unknown",
                    ),
                )

            with col3:
                st.metric(
                    "Writer",
                    result.get(
                        "writer_mode",
                        "unknown",
                    ),
                )

                st.metric(
                    "Reviewer",
                    result.get(
                        "reviewer_mode",
                        "unknown",
                    ),
                )

            st.divider()

            # =================================================
            # REVIEW
            # =================================================

            st.subheader("✅ Review Result")

            review_col1, review_col2, review_col3 = (
                st.columns(3)
            )

            with review_col1:
                st.metric(
                    "Score",
                    result.get(
                        "review_score",
                        "N/A",
                    ),
                )

            with review_col2:
                decision = result.get(
                    "review_decision",
                    "N/A",
                )

                st.metric(
                    "Decision",
                    str(decision).upper(),
                )

            with review_col3:
                st.metric(
                    "Revisions",
                    result.get(
                        "revision_count",
                        0,
                    ),
                )

            feedback = result.get(
                "reviewer_feedback",
                [],
            )

            if feedback:
                st.markdown(
                    "**Reviewer Feedback**"
                )

                if isinstance(feedback, list):
                    for item in feedback:
                        st.write(f"• {item}")
                else:
                    st.write(feedback)

            st.divider()

            # =================================================
            # FINAL DELIVERABLE
            # =================================================

            st.subheader("📄 Final Deliverable")

            final_draft = result.get(
                "draft",
                "No final deliverable was produced.",
            )

            st.markdown(final_draft)

            st.divider()

            # =================================================
            # AGENT OUTPUTS
            # =================================================

            st.subheader(
                "🔍 Inspect Agent Outputs"
            )

            with st.expander(
                "🧠 Planner Output"
            ):
                st.code(
                    result.get(
                        "plan",
                        "No plan available.",
                    ),
                    language="json",
                )

            with st.expander(
                "🔎 Researcher Output"
            ):
                st.write(
                    result.get(
                        "research",
                        "No research available.",
                    )
                )

            with st.expander(
                "📊 Analyst Output"
            ):
                st.write(
                    result.get(
                        "analysis",
                        "No analysis available.",
                    )
                )

            with st.expander(
                "🎯 Strategist Output"
            ):
                st.write(
                    result.get(
                        "strategy",
                        "No strategy available.",
                    )
                )

            with st.expander(
                "✍️ Writer Output"
            ):
                st.write(
                    result.get(
                        "draft",
                        "No draft available.",
                    )
                )

            with st.expander(
                "✅ Reviewer Output"
            ):
                st.write(
                    {
                        "score": result.get(
                            "review_score"
                        ),
                        "decision": result.get(
                            "review_decision"
                        ),
                        "feedback": result.get(
                            "reviewer_feedback"
                        ),
                    }
                )

        except Exception as exc:
            st.error(
                "The workflow encountered an error."
            )

            st.exception(exc)


# ============================================================
# ARCHITECTURE
# ============================================================

st.divider()

st.subheader("🏗️ Architecture")

st.code(
    """
User Goal
   |
   v
Planner
   |
   v
Researcher + Web Search
   |
   v
Analyst
   |
   v
Strategist
   |
   v
Writer
   |
   v
Reviewer
   |
   +---- Approve ----> END
   |
   +---- Revise -----> Writer
""",
    language="text",
)

st.caption(
    "LangGraph manages shared state, node execution, "
    "conditional routing, and the bounded revision loop."
)