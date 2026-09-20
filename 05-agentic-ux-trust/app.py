import streamlit as st

from src.evaluation.evaluator import (
    evaluate_proposal,
)
from src.guardrails.safety import (
    validate_request,
)
from src.models.schemas import (
    HumanDecision,
    TrustRequest,
)
from src.workflow.trust_workflow import (
    apply_human_decision,
    create_proposal,
)


st.set_page_config(
    page_title="Agentic UX Trust Lab",
    page_icon="🛡️",
    layout="wide",
)


st.title(
    "🛡️ Agentic UX Trust Prototype"
)

st.caption(
    "Transparent financial decision-support "
    "with evidence, action previews and human control."
)

st.warning(
    "Educational prototype only. "
    "No financial transaction is executed and "
    "the system does not provide personalized "
    "financial advice."
)


question = st.text_area(
    "💬 Financial question",
    placeholder=(
        "What factors should be reviewed if "
        "this hypothetical portfolio has "
        "high concentration risk?"
    ),
)


scenario = st.text_area(
    "📋 Scenario",
    placeholder=(
        "The hypothetical portfolio is heavily "
        "concentrated in one technology sector "
        "and liquidity may be needed within "
        "three years."
    ),
)


if st.button(
    "🧠 Generate Action Preview",
    type="primary",
):
    try:
        request = TrustRequest(
            question=question,
            scenario=scenario,
        )

        # Deterministic safety guardrail runs
        # BEFORE the agent creates a proposal.
        allowed, reason = validate_request(
            request
        )

        if not allowed:
            # Remove any old proposal so that a
            # previous result is not shown below
            # the blocked request.
            st.session_state.pop(
                "proposal",
                None,
            )
            st.session_state.pop(
                "metrics",
                None,
            )

            st.error(
                f"🛑 Request blocked: {reason}"
            )
            st.stop()

        proposal, metrics = (
            create_proposal(request)
        )

        st.session_state[
            "proposal"
        ] = proposal

        st.session_state[
            "metrics"
        ] = metrics

    except Exception as error:
        st.error(
            str(error)
        )


if "proposal" in st.session_state:
    proposal = (
        st.session_state[
            "proposal"
        ]
    )

    st.divider()

    st.header(
        "🤖 Agent Proposal"
    )

    st.subheader(
        "Summary"
    )

    st.write(
        proposal.summary
    )

    st.subheader(
        "🧠 Reasoning Summary"
    )

    for item in (
        proposal.reasoning_summary
    ):
        st.write(
            "•",
            item,
        )

    st.subheader(
        "📚 Evidence / Citations"
    )

    for evidence in (
        proposal.evidence
    ):
        with st.expander(
            (
                f"{evidence.title} "
                f"[{evidence.source_id}]"
            )
        ):
            st.write(
                evidence.text
            )

            st.caption(
                (
                    "Retrieval relevance "
                    f"indicator: "
                    f"{evidence.score:.3f}"
                )
            )

    col1, col2 = (
        st.columns(2)
    )

    with col1:
        st.subheader(
            "⚠️ Assumptions"
        )

        for item in (
            proposal.assumptions
        ):
            st.write(
                "•",
                item,
            )

    with col2:
        st.subheader(
            "🚨 Risks"
        )

        for item in (
            proposal.risks
        ):
            st.write(
                "•",
                item,
            )

    st.subheader(
        "👁️ Action Preview"
    )

    for action in (
        proposal.proposed_actions
    ):
        st.info(
            (
                f"{action.action}\n\n"
                f"{action.description}"
            )
        )

        st.write(
            "Human approval required:",
            action.requires_human_approval,
        )

    st.subheader(
        "📊 Confidence Indicator"
    )

    st.progress(
        proposal.confidence
    )

    st.write(
        (
            f"{proposal.confidence * 100:.0f}%"
        )
    )

    st.caption(
        "This is an application confidence "
        "indicator, not a calibrated probability "
        "or guarantee of correctness."
    )

    evaluation = (
        evaluate_proposal(
            proposal
        )
    )

    with st.expander(
        "🧪 Trust & Safety Evaluation"
    ):
        st.json(
            evaluation
        )

    with st.expander(
        "📈 Run Telemetry"
    ):
        st.json(
            st.session_state[
                "metrics"
            ]
        )

    st.divider()

    st.header(
        "🧑 Human-in-the-Loop Control"
    )

    st.write(
        (
            "**Current status:** "
            f"{proposal.execution_status}"
        )
    )

    if (
        proposal.execution_status
        == "awaiting_approval"
    ):
        override_text = (
            st.text_area(
                "Override instruction",
                placeholder=(
                    "Example: Only review "
                    "concentration risk. Do not "
                    "suggest allocation changes."
                ),
            )
        )

        col1, col2, col3 = (
            st.columns(3)
        )

        decision = None

        with col1:
            if st.button(
                "✅ Approve"
            ):
                decision = "approve"

        with col2:
            if st.button(
                "✏️ Override"
            ):
                decision = "override"

        with col3:
            if st.button(
                "🛑 Cancel"
            ):
                decision = "cancel"

        if decision:
            try:
                human_decision = (
                    HumanDecision(
                        decision=decision,
                        override_instruction=(
                            override_text
                        ),
                    )
                )

                updated = (
                    apply_human_decision(
                        proposal,
                        human_decision,
                    )
                )

                st.session_state[
                    "proposal"
                ] = updated

                if (
                    updated.execution_status
                    == "cancelled"
                ):
                    st.error(
                        "Action cancelled. "
                        "Nothing was executed."
                    )

                elif (
                    updated.execution_status
                    == "overridden"
                ):
                    st.warning(
                        "Human override applied."
                    )

                else:
                    st.success(
                        "Action preview approved. "
                        "No real financial "
                        "transaction was executed."
                    )

                st.rerun()

            except Exception as error:
                st.error(
                    str(error)
                )

    elif (
        proposal.execution_status
        == "approved"
    ):
        st.success(
            "✅ Proposal approved by the human reviewer."
        )

    elif (
        proposal.execution_status
        == "overridden"
    ):
        st.warning(
            "✏️ Human override applied."
        )

    elif (
        proposal.execution_status
        == "cancelled"
    ):
        st.error(
            "🛑 Proposal cancelled. No action executed."
        )