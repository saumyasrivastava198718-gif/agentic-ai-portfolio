from pathlib import Path

import chromadb


class VectorStore:
    def __init__(
        self,
        collection_name="microsoft_annual_report"
    ):
        # Find the project root:
        # src/vector_store.py -> src -> project root
        project_root = Path(__file__).resolve().parent.parent

        # Always use the chroma_db folder inside this project
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
            metadatas.append({
                "page_number": chunk["page_number"]
            })

        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings
        )

    def search(self, query_embedding, top_k=5):
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results