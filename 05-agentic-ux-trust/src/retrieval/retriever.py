from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from src.models.schemas import EvidenceItem


DATA_FILE = Path("data/financial_knowledge.txt")

_model = None
_collection = None


def _load_documents() -> list[dict]:
    """Read and parse the local financial knowledge base."""

    raw_text = DATA_FILE.read_text(
        encoding="utf-8"
    )

    blocks = [
        block.strip()
        for block in raw_text.split("\n\n")
        if block.strip()
    ]

    documents = []

    for block in blocks:
        lines = block.splitlines()

        if len(lines) < 3:
            continue

        source_id = (
            lines[0]
            .replace("SOURCE_ID:", "")
            .strip()
        )

        title = (
            lines[1]
            .replace("TITLE:", "")
            .strip()
        )

        text = " ".join(lines[2:]).strip()

        documents.append(
            {
                "source_id": source_id,
                "title": title,
                "text": text,
            }
        )

    return documents


def initialize_retriever() -> None:
    """Initialize the embedding model and Chroma collection once."""

    global _model
    global _collection

    if (
        _model is not None
        and _collection is not None
    ):
        return

    _model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    client = chromadb.Client()

    _collection = client.get_or_create_collection(
        name="financial_trust_knowledge"
    )

    documents = _load_documents()

    texts = [
        item["text"]
        for item in documents
    ]

    embeddings = _model.encode(
        texts,
        normalize_embeddings=True,
    ).tolist()

    ids = [
        item["source_id"]
        for item in documents
    ]

    metadatas = [
        {
            "source_id": item["source_id"],
            "title": item["title"],
        }
        for item in documents
    ]

    # upsert makes initialization safe if the code is rerun.
    _collection.upsert(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings,
    )


def retrieve_evidence(
    query: str,
    top_k: int = 3,
) -> list[EvidenceItem]:
    """Retrieve the most semantically relevant evidence."""

    initialize_retriever()

    query_embedding = _model.encode(
        [query],
        normalize_embeddings=True,
    ).tolist()[0]

    results = _collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    evidence = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for index, document in enumerate(documents):
        metadata = metadatas[index]

        distance = float(
            distances[index]
        )

        # Display-friendly similarity indicator.
        score = max(
            0.0,
            min(
                1.0,
                1.0 / (1.0 + distance),
            ),
        )

        evidence.append(
            EvidenceItem(
                source_id=metadata["source_id"],
                title=metadata["title"],
                text=document,
                score=score,
            )
        )

    return evidence