from google import genai
from dotenv import load_dotenv


load_dotenv()


class AnswerGenerator:
    def __init__(self):
        self.client = genai.Client()

    def generate(self, question: str, evidence: list):

        if not evidence:
            return (
                "I could not find enough evidence to answer "
                "this question reliably."
            )

        evidence_text = []

        for index, item in enumerate(evidence, start=1):

            source_type = item.get(
                "source_type",
                "unknown"
            )

            content = item.get(
                "content",
                ""
            )

            if source_type == "pdf":
                source = (
                    f"PDF page "
                    f"{item.get('page_number', 'unknown')}"
                )

            else:
                source = (
                    f"{item.get('source_name', 'Web source')} "
                    f"- {item.get('url', '')}"
                )

            evidence_text.append(
                f"""
SOURCE {index}
Type: {source_type}
Source: {source}
Content:
{content}
"""
            )

        context = "\n".join(evidence_text)

        prompt = f"""
You are a grounded AI research assistant.

Answer the user's question using ONLY the evidence
provided below.

Rules:

1. Do not invent facts that are not supported by the evidence.
2. If the evidence is insufficient, clearly say so.
3. When useful, mention whether information came from
   the PDF or from a web source.
4. Keep the answer clear and professional.
5. Do not make up citations or URLs.

USER QUESTION:
{question}

EVIDENCE:
{context}

Write the final grounded answer.
"""

        try:
            interaction = self.client.interactions.create(
                model="gemini-3.8-flash",
                input=prompt
            )

            return interaction.output_text

        except Exception as error:

            fallback_parts = [
                "The language model is temporarily unavailable, "
                "but retrieval succeeded.\n"
            ]

            for index, item in enumerate(
                evidence[:5],
                start=1
            ):

                content = item.get(
                    "content",
                    ""
                )

                short_content = content[:500]

                if item.get("source_type") == "pdf":

                    source = (
                        f"PDF page "
                        f"{item.get('page_number', 'unknown')}"
                    )

                else:

                    source = (
                        item.get(
                            "source_name",
                            "Web source"
                        )
                    )

                fallback_parts.append(
                    f"\n[{index}] {source}\n"
                    f"{short_content}"
                )

            fallback_parts.append(
                f"\n\nLLM status: "
                f"{type(error).__name__}"
            )

            return "\n".join(
                fallback_parts
            )
           