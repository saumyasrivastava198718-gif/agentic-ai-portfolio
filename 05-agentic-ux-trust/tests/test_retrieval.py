from src.retrieval.retriever import (
    retrieve_evidence,
)


def test_retriever_returns_evidence():
    evidence = retrieve_evidence(
        "portfolio concentration risk"
    )

    assert len(evidence) > 0
    assert evidence[0].source_id
    assert evidence[0].title