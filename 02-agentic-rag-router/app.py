import streamlit as st

from src.orchestrator import Orchestrator


st.set_page_config(
    page_title="Agentic RAG Router",
    page_icon="🤖",
    layout="wide"
)


@st.cache_resource
def load_orchestrator():
    return Orchestrator()


orchestrator = load_orchestrator()


st.title("🤖 Agentic RAG Router")
st.subheader("Multi-Source Grounded AI Assistant")

st.write(
    "Ask questions about the indexed Microsoft Annual Report "
    "or ask for current information from the web."
)

question = st.text_input(
    "💬 Ask a question:",
    placeholder="What does Microsoft say about artificial intelligence?"
)


if st.button("🚀 Ask AI", type="primary"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner(
            "Routing, retrieving evidence and generating answer..."
        ):

            result = orchestrator.answer(question)


        st.divider()

        st.subheader("🤖 Answer")

        st.write(result["answer"])


        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "🚦 Route",
                result["route"].upper()
            )

        with col2:
            st.metric(
                "🎯 Router Confidence",
                f"{result['confidence']:.0%}"
            )


        st.info(
            f"**Why this route?** {result['reason']}"
        )


        st.subheader("📚 Retrieved Evidence")

        for index, item in enumerate(
            result["evidence"],
            start=1
        ):

            if item["source_type"] == "pdf":

                title = (
                    f"📄 Source {index} — "
                    f"PDF Page {item.get('page_number')}"
                )

            else:

                title = (
                    f"🌐 Source {index} — "
                    f"{item.get('source_name', 'Web Source')}"
                )

            with st.expander(title):

                st.write(item.get("content", ""))

                if item["source_type"] == "web":

                    url = item.get("url")

                    if url:
                        st.write(
                            f"Source URL: {url}"
                        )