import json

from app.knowledge.knowledge_record import KnowledgeRecord
from app.storage.knowledge_store import KnowledgeStore


def test_storage_contains_structured_knowledge(tmp_path):
    path = tmp_path / "knowledge.jsonl"

    store = KnowledgeStore(path)

    record = KnowledgeRecord(
        title="EGFR mutations in non-small cell lung cancer",
        pmid="TEST001",
        genes=["EGFR"],
        disease_context=[
            "lung cancer",
            "non-small cell lung cancer",
        ],
        molecular_evidence=["mutation"],
        evidence_types=[
            "prognosis",
            "survival",
        ],
        evidence_score=0.88,
        reasons=[
            "gene-specific evidence",
        ],
        provenance={
            "source": "PubMed",
            "pmid": "TEST001",
            "query": "lung cancer AND gene",
        },
    )

    store.save(record)

    # Read the actual persisted JSONL record.
    with path.open("r", encoding="utf-8") as file:
        stored = json.loads(file.readline())

    # Structured knowledge is persisted.
    assert stored["pmid"] == "TEST001"
    assert stored["genes"] == ["EGFR"]
    assert stored["disease_context"] == [
        "lung cancer",
        "non-small cell lung cancer",
    ]
    assert stored["molecular_evidence"] == ["mutation"]
    assert stored["evidence_types"] == [
        "prognosis",
        "survival",
    ]

    # Evidence scoring is preserved.
    assert stored["evidence_score"] == 0.88

    # Provenance is preserved.
    assert stored["provenance"]["source"] == "PubMed"
    assert stored["provenance"]["query"] == "lung cancer AND gene"

    # The knowledge base does not contain raw PubMed XML.
    assert "<PubmedArticle" not in json.dumps(stored)