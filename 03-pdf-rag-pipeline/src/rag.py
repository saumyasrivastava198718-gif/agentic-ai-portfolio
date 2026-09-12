from dotenv import load_dotenv
from google import genai

from src.retrieval import Retriever


class RAGPipeline:
    def __init__(self):
        # Load the API key from the .env file
        load_dotenv()

        # Create the Gemini client
        self.client = genai.Client()

        # Create our PDF retriever
        self.retriever = Retriever()

    def answer_question(self, question, top_k=5):
        """
        Retrieve relevant PDF chunks and use Gemini
        to generate a grounded answer.
        """

        # STEP 1: Retrieve relevant chunks from Chroma
        retrieved_chunks = self.retriever.retrieve(
            question,
            top_k=top_k
        )

        # STEP 2: Convert the retrieved chunks into context
        context_parts = []

        for chunk in retrieved_chunks:
            context_parts.append(
                f"Page {chunk['page_number']}:\n"
                f"{chunk['text']}"
            )

        context = "\n\n".join(context_parts)

        # STEP 3: Build the prompt for Gemini
        prompt = f"""
You are answering questions about Microsoft's annual report.

Use ONLY the context supplied below.

If the answer cannot be determined from the context,
say that the retrieved report context does not contain
enough information.

Do not invent facts.

QUESTION:
{question}

CONTEXT:
{context}

Give a clear and concise answer.
Mention relevant page numbers when appropriate.
"""

        # STEP 4: Send the question + retrieved context to Gemini
        interaction = self.client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt
        )

        # STEP 5: Collect the source page numbers
        source_pages = sorted(
            set(
                chunk["page_number"]
                for chunk in retrieved_chunks
            )
        )

        # STEP 6: Return everything
        return {
            "answer": interaction.output_text,
            "sources": source_pages,
            "retrieved_chunks": retrieved_chunks
        }