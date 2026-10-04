from app.knowledge.knowledge_record import (
    KnowledgeRecord,
    Provenance,
)
from app.retrieval.document_pipeline import DocumentPipeline


def build_test_record() -> KnowledgeRecord:
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
        reasons=[
            "gene-specific evidence",
        ],
        provenance=Provenance(
            source="PubMed",
            pmid="TEST001",
            query="lung cancer AND gene",
        ),
    )


def test_document_pipeline_transforms_record():

    record = build_test_record()

    document = DocumentPipeline().transform(record)

    assert document.text
    assert "EGFR" in document.text
    assert "mutation" in document.text
    assert "prognosis" in document.text

    assert document.metadata["pmid"] == "TEST001"
    assert document.metadata["source"] == "PubMed"
    assert document.metadata["evidence_score"] == 0.88


def test_document_pipeline_transforms_multiple_records():

    records = [
        build_test_record(),
        KnowledgeRecord(
            pmid="TEST002",
            title="KRAS mutations and lung cancer survival",
            genes=["KRAS"],
            disease_context=["lung cancer"],
            molecular_evidence=["mutation"],
            evidence_types=["survival"],
            evidence_score=0.82,
            reasons=["gene-specific evidence"],
            provenance=Provenance(
                source="PubMed",
                pmid="TEST002",
                query="lung cancer AND gene",
            ),
        ),
    ]

    documents = DocumentPipeline().transform_many(records)

    assert len(documents) == 2
    assert documents[0].metadata["pmid"] == "TEST001"
    assert documents[1].metadata["pmid"] == "TEST002"