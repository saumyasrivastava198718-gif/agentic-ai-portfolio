from sentence_transformers import SentenceTransformer


class Embedder:
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts):
        embeddings = self.model.encode(
            texts,
            show_progress_bar=True
        )

        return embeddings.tolist()

    def embed_query(self, query: str):
        embedding = self.model.encode([query])

        return embedding[0].tolist()