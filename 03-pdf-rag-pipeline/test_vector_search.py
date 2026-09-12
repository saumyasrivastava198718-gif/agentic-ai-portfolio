from src.ingestion import extract_text_from_pdf
from src.chunking import chunk_pages
from src.embeddings import EmbeddingModel
from src.vector_store import VectorStore


PDF_PATH = "data/documents/microsoft_2025_annual_report.pdf"


print("1. Reading PDF...")

pages = extract_text_from_pdf(PDF_PATH)

print(f"Pages extracted: {len(pages)}")


print("\n2. Creating chunks...")

chunks = chunk_pages(
    pages,
    chunk_size=1000,
    chunk_overlap=200
)

print(f"Chunks created: {len(chunks)}")


print("\n3. Loading embedding model...")

embedding_model = EmbeddingModel()


print("\n4. Creating embeddings...")

texts = [chunk["text"] for chunk in chunks]

embeddings = embedding_model.embed_documents(texts)

print(f"Embeddings created: {len(embeddings)}")
print(f"Embedding dimensions: {len(embeddings[0])}")


print("\n5. Storing vectors in Chroma...")

vector_store = VectorStore()

vector_store.add_chunks(
    chunks,
    embeddings
)

print("Vectors stored successfully.")


print("\n6. Running semantic search...")

question = "What does Microsoft say about artificial intelligence?"

query_embedding = embedding_model.embed_query(question)

results = vector_store.search(
    query_embedding,
    top_k=5
)


print("\nQUESTION:")
print(question)

print("\nTOP MATCHES:")

for i in range(len(results["documents"][0])):
    print("\n-----------------------------")

    print(
        "Page:",
        results["metadatas"][0][i]["page_number"]
    )

    print(
        results["documents"][0][i][:700]
    )