from pathlib import Path

import chromadb


class VectorStore:
    def __init__(
        self,
        collection_name: str = "agentic_rag_documents"
    ):
        project_root = Path(__file__).resolve().parent.parent.parent

        db_path = project_root / "chroma_db"

        self.client = chromadb.PersistentClient(
            path=str(db_path)
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add_chunks(self, chunks, embeddings):
        ids = []
        documents = []
        metadatas = []

        for chunk in chunks:
            ids.append(chunk["chunk_id"])
            documents.append(chunk["text"])

            metadatas.append(
                {
                    "page_number": chunk["page_number"]
                }
            )

        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings
        )

    def search(self, query_embedding, top_k: int = 5):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )