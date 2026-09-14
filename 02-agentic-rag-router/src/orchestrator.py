from src.router import Router
from src.tools.pdf_tool import PDFTool
from src.tools.web_tool import WebTool
from src.answer_generator import AnswerGenerator


class Orchestrator:
    def __init__(self):
        self.router = Router()
        self.pdf_tool = PDFTool()
        self.web_tool = WebTool()
        self.answer_generator = AnswerGenerator()

    def retrieve(self, question: str):
        decision = self.router.route(question)

        if decision.route == "pdf":

            evidence = self.pdf_tool.search(
                question
            )

        elif decision.route == "web":

            evidence = self.web_tool.search(
                question
            )

        else:

            pdf_evidence = self.pdf_tool.search(
                question
            )

            web_evidence = self.web_tool.search(
                question
            )

            evidence = (
                pdf_evidence
                +
                web_evidence
            )

        return {
            "route": decision.route,
            "confidence": decision.confidence,
            "reason": decision.reason,
            "evidence": evidence
        }

    def answer(self, question: str):

        retrieval_result = self.retrieve(
            question
        )

        final_answer = (
            self.answer_generator.generate(
                question=question,
                evidence=retrieval_result["evidence"]
            )
        )

        return {
            "route": retrieval_result["route"],
            "confidence": retrieval_result["confidence"],
            "reason": retrieval_result["reason"],
            "answer": final_answer,
            "evidence": retrieval_result["evidence"]
        }