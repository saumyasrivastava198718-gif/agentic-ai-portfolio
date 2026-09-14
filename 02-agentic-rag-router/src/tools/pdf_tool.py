from src.indexing.embedder import Embedder
from src.indexing.vector_store import VectorStore


class PDFTool:
    def __init__(self):
        self.embedder = Embedder()
        self.vector_store = VectorStore()

    def search(self, question: str, top_k: int = 5):
        query_embedding = self.embedder.embed_query(question)

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k
        )

        evidence = []

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):
            evidence.append(
                {
                    "content": document,
                    "source_type": "pdf",
                    "page_number": metadata.get("page_number"),
                    "distance": distance
                }
            )

        return evidence
    