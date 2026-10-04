from app.knowledge.knowledge_record import KnowledgeRecord
from app.storage.knowledge_store import KnowledgeStore


def test_knowledge_record_can_be_persisted_and_loaded(tmp_path):
    store = KnowledgeStore(tmp_path / "knowledge.jsonl")

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

    loaded = store.load_all()

    assert len(loaded) == 1

    assert loaded[0].pmid == "TEST001"
    assert loaded[0].genes == ["EGFR"]
    assert loaded[0].evidence_score == 0.88

    assert loaded[0].provenance.source == "PubMed"
    assert loaded[0].provenance.pmid == "TEST001"
    assert loaded[0].provenance.query == "lung cancer AND gene"