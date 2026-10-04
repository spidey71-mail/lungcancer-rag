from app.knowledge.evidence_scorer import EvidenceScorer
from app.knowledge.schema import Publication


def test_gene_specific_paper_scores_high():
    publication = Publication(
        pmid="TEST001",
        title="EGFR mutations in non-small cell lung cancer",
        abstract=(
            "This study evaluates EGFR mutations and their "
            "association with prognosis and survival in "
            "patients with non-small cell lung cancer."
        ),
        keywords=["EGFR", "mutation", "lung cancer"],
    )

    result = EvidenceScorer().evaluate(publication)

    assert result.total_score > 0.7
    assert "EGFR" in result.gene_hits
    assert "mutation" in result.molecular_hits
    assert "prognosis" in result.evidence_hits


def test_irrelevant_paper_scores_low():
    publication = Publication(
        pmid="TEST002",
        title="Agricultural soil microbiome analysis",
        abstract=(
            "This study investigates microbial diversity "
            "in agricultural soil."
        ),
    )

    result = EvidenceScorer().evaluate(publication)

    assert result.total_score < 0.3
    assert result.disease_score == 0.0
    assert result.gene_specificity_score == 0.0


def test_provenance_is_explainable():
    publication = Publication(
        pmid="TEST003",
        title="KRAS mutation and lung cancer survival",
        abstract="Clinical study of KRAS mutations.",
    )

    result = EvidenceScorer().evaluate(publication)

    assert result.reasons
    assert "KRAS" in result.gene_hits
    assert "mutation" in result.molecular_hits
    assert "survival" in result.evidence_hits