import streamlit as st

from src.rag import RAGPipeline


# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="Microsoft Annual Report RAG",
    page_icon="📄",
    layout="centered"
)


# -----------------------------
# TITLE AND DESCRIPTION
# -----------------------------

st.title("📄 Microsoft Annual Report RAG")

st.write(
    "Ask questions about Microsoft's 2025 Annual Report. "
    "The system retrieves relevant report sections and uses Gemini "
    "to generate a grounded answer."
)


# -----------------------------
# LOAD RAG PIPELINE
# -----------------------------

@st.cache_resource
def load_rag():
    return RAGPipeline()


rag = load_rag()


# -----------------------------
# USER QUESTION
# -----------------------------

question = st.text_input(
    "Ask a question about the report:",
    placeholder="Example: What does Microsoft say about artificial intelligence?"
)


# -----------------------------
# ASK BUTTON
# -----------------------------

if st.button("Ask"):

    if not question.strip():
        st.warning("Please enter a question.")

    else:

        with st.spinner(
            "Searching the report and generating an answer..."
        ):

            result = rag.answer_question(
                question,
                top_k=5
            )


        # -----------------------------
        # DISPLAY ANSWER
        # -----------------------------

        st.subheader("Answer")

        st.write(result["answer"])


        # -----------------------------
        # DISPLAY SOURCE PAGES
        # -----------------------------

        st.subheader("Source Pages")

        if result["sources"]:

            source_text = ", ".join(
                str(page)
                for page in result["sources"]
            )

            st.write(source_text)

        else:

            st.write("No source pages retrieved.")


        # -----------------------------
        # DISPLAY RETRIEVED EVIDENCE
        # -----------------------------

        with st.expander("🔎 View Retrieved Evidence"):

            for i, chunk in enumerate(
                result["retrieved_chunks"],
                start=1
            ):

                st.markdown(
                    f"### Result {i} — Page {chunk['page_number']}"
                )

                st.write(chunk["text"])

                st.divider()