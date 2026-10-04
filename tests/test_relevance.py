from app.knowledge.relevance import RelevanceFilter
from app.knowledge.schema import Publication


def test_relevant_lung_cancer_gene_paper():

    publication = Publication(
        pmid="TEST001",
        title="EGFR mutations in non-small cell lung cancer",
        abstract=(
            "This study investigates EGFR mutations and "
            "their association with lung cancer prognosis."
        ),
    )

    result = RelevanceFilter().evaluate(publication)

    assert result.relevant is True
    assert "non-small cell lung cancer" in result.lung_cancer_hits
    assert result.molecular_hits
    assert result.evidence_hits


def test_irrelevant_paper():

    publication = Publication(
        pmid="TEST002",
        title="Effects of exercise on cardiovascular health",
        abstract=(
            "This study investigates physical activity "
            "and cardiovascular outcomes."
        ),
    )

    result = RelevanceFilter().evaluate(publication)

    assert result.relevant is False