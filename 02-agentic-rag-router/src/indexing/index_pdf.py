from pathlib import Path

from src.indexing.pdf_loader import load_pdf
from src.indexing.chunker import chunk_pages
from src.indexing.embedder import Embedder
from src.indexing.vector_store import VectorStore
from src.indexing.document_registry import DocumentRegistry


def index_pdf(pdf_path: str):

    registry = DocumentRegistry()

    file_hash = registry.compute_hash(pdf_path)
    filename = Path(pdf_path).name

    print("\nDocument fingerprint:")
    print(file_hash[:16])

    if registry.is_indexed(file_hash):
        print("\nThis exact PDF has already been indexed.")
        print("Skipping parsing, chunking and embedding.")
        return

    print("\n1. Loading PDF...")
    pages = load_pdf(pdf_path)
    print(f"Loaded {len(pages)} pages.")

    print("\n2. Chunking PDF...")
    chunks = chunk_pages(
        pages=pages,
        chunk_size=1000,
        overlap=150
    )
    print(f"Created {len(chunks)} chunks.")

    document_id = file_hash[:12]

    for chunk in chunks:
        old_id = chunk["chunk_id"]
        chunk["chunk_id"] = (
            f"{document_id}-{old_id}"
        )

    print("\n3. Creating embeddings...")

    embedder = Embedder()

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = embedder.embed_documents(texts)

    print(
        f"Created {len(embeddings)} embeddings."
    )

    print("\n4. Storing vectors in ChromaDB...")

    vector_store = VectorStore()

    vector_store.add_chunks(
        chunks=chunks,
        embeddings=embeddings
    )

    registry.register(
        file_hash=file_hash,
        filename=filename
    )

    print("\nPDF indexing complete.")
    print("Document fingerprint saved.")


if __name__ == "__main__":

    project_root = (
        Path(__file__)
        .resolve()
        .parent
        .parent
        .parent
    )

    pdf_path = (
        project_root
        / "data"
        / "microsoft_2025_annual_report.pdf"
    )

    index_pdf(str(pdf_path))