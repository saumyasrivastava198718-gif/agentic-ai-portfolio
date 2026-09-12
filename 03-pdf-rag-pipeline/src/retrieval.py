from src.embeddings import EmbeddingModel
from src.vector_store import VectorStore


class Retriever:
    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.vector_store = VectorStore()

    def retrieve(self, question, top_k=5):
        query_embedding = self.embedding_model.embed_query(question)

        results = self.vector_store.search(
            query_embedding,
            top_k=top_k
        )

        retrieved_chunks = []

        for i in range(len(results["documents"][0])):
            retrieved_chunks.append({
                "text": results["documents"][0][i],
                "page_number": results["metadatas"][0][i]["page_number"]
            })

        return retrieved_chunks