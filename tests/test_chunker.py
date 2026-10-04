from app.knowledge.knowledge_document import KnowledgeDocumentBuilder
from app.knowledge.knowledge_record import (
    KnowledgeRecord,
    Provenance,
)
from app.retrieval.chunker import EvidenceChunker


def build_record():

    return KnowledgeRecord(
        pmid="TEST001",
        title="EGFR mutations in non-small cell lung cancer",
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
        reasons=["gene-specific evidence"],
        provenance=Provenance(
            source="PubMed",
            pmid="TEST001",
            query="lung cancer AND gene",
        ),
    )


def test_chunker_preserves_biomedical_relationships():

    record = build_record()

    document = KnowledgeDocumentBuilder().build(record)

    chunks = EvidenceChunker().chunk(document)

    assert len(chunks) == 2

    molecular = next(
        chunk
        for chunk in chunks
        if chunk.chunk_type == "molecular"
    )

    evidence = next(
        chunk
        for chunk in chunks
        if chunk.chunk_type == "evidence"
    )

    assert "EGFR" in molecular.text
    assert "mutation" in molecular.text
    assert "non-small cell lung cancer" in molecular.text

    assert "prognosis" in evidence.text
    assert "survival" in evidence.text

    assert molecular.metadata["pmid"] == "TEST001"
    assert evidence.metadata["pmid"] == "TEST001"

    assert molecular.metadata["evidence_score"] == 0.88
    assert evidence.metadata["evidence_score"] == 0.88


def test_chunker_preserves_provenance():

    record = build_record()

    document = KnowledgeDocumentBuilder().build(record)

    chunks = EvidenceChunker().chunk(document)

    for chunk in chunks:
        assert chunk.metadata["source"] == "PubMed"
        assert chunk.metadata["query"] == "lung cancer AND gene"