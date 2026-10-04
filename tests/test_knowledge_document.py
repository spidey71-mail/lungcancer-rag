from app.knowledge.knowledge_document import KnowledgeDocumentBuilder
from app.knowledge.knowledge_record import (
    KnowledgeRecord,
    Provenance,
)


def test_knowledge_document_preserves_evidence_and_provenance():

    record = KnowledgeRecord(
        pmid="TEST001",
        title="EGFR mutations in non-small cell lung cancer",
        journal="Journal of Cancer Research",
        publication_year=2026,
        doi="10.1234/example",
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
            "lung-cancer disease context detected",
            "molecular/genomic context detected",
            "specific lung-cancer gene symbols detected",
        ],
        provenance=Provenance(
            source="PubMed",
            pmid="TEST001",
            query="lung cancer AND gene",
        ),
    )

    document = KnowledgeDocumentBuilder().build(record)

    assert document.text

    assert "EGFR" in document.text
    assert "non-small cell lung cancer" in document.text
    assert "mutation" in document.text
    assert "prognosis" in document.text

    assert document.metadata["pmid"] == "TEST001"
    assert document.metadata["source"] == "PubMed"
    assert document.metadata["evidence_score"] == 0.88

    assert "EGFR" in document.metadata["genes"]