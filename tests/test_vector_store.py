from uuid import uuid4

from app.retrieval.vector_store import VectorStore


def test_vector_store_can_store_and_count():

    collection_name = f"test_{uuid4().hex}"

    store = VectorStore(
        collection_name=collection_name
    )

    vector = [0.1, 0.2, 0.3]

    store.add(
        vector=vector,
        text="EGFR mutations in lung cancer.",
        metadata={
            "pmid": "TEST001",
            "genes": ["EGFR"],
        },
    )

    assert store.count() == 1

    store.delete_collection()


def test_vector_store_can_search():

    collection_name = f"test_{uuid4().hex}"

    store = VectorStore(
        collection_name=collection_name
    )

    store.add(
        vector=[1.0, 0.0, 0.0],
        text="EGFR mutations in lung cancer.",
        metadata={
            "pmid": "TEST001",
            "genes": ["EGFR"],
        },
    )

    store.add(
        vector=[0.0, 1.0, 0.0],
        text="KRAS mutations in lung cancer.",
        metadata={
            "pmid": "TEST002",
            "genes": ["KRAS"],
        },
    )

    results = store.search(
        query_vector=[1.0, 0.0, 0.0],
        limit=1,
    )

    assert len(results) == 1
    assert results[0]["metadata"]["pmid"] == "TEST001"

    store.delete_collection()