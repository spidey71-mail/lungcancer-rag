from app.knowledge.schema import Publication
from app.knowledge.evidence_score import EvidenceScore
from app.knowledge.knowledge_record import KnowledgeRecordBuilder


def test_knowledge_record_preserves_evidence_and_provenance():

    publication = Publication(
        pmid="TEST001",
        title="EGFR mutations in non-small cell lung cancer",
        abstract=(
            "EGFR mutations are associated with prognosis "
            "in patients with non-small cell lung cancer."
        ),
        keywords=["EGFR", "mutation", "lung cancer"],
    )

    evidence = EvidenceScore(
        disease_score=1.0,
        molecular_score=0.8,
        evidence_score=0.75,
        gene_specificity_score=1.0,
        total_score=0.88,
        disease_hits=[
            "lung cancer",
            "non-small cell lung cancer",
        ],
        molecular_hits=["mutation"],
        evidence_hits=["prognosis", "association"],
        gene_hits=["EGFR"],
        reasons=[
            "lung-cancer disease context detected",
            "molecular/genomic context detected",
            "biomedical evidence context detected",
            "specific lung-cancer gene symbols detected",
        ],
    )

    record = KnowledgeRecordBuilder().build(
        publication=publication,
        evidence=evidence,
        source_query="lung cancer AND gene",
    )

    assert record.pmid == "TEST001"
    assert record.title == publication.title

    assert record.genes == ["EGFR"]
    assert "mutation" in record.molecular_evidence
    assert "prognosis" in record.evidence_types

    assert record.evidence_score == 0.88

    assert record.provenance.source == "PubMed"
    assert record.provenance.pmid == "TEST001"
    assert record.provenance.query == "lung cancer AND gene"