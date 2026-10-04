from app.ingestion.query_builder import LungCancerQueryBuilder


def test_query_builder_creates_queries():

    queries = LungCancerQueryBuilder().build_queries()

    assert len(queries) == 8


def test_queries_have_required_fields():

    queries = LungCancerQueryBuilder().build_queries()

    for query in queries:
        assert query.name
        assert query.query
        assert query.purpose


def test_queries_cover_multiple_evidence_dimensions():

    queries = LungCancerQueryBuilder().build_queries()

    query_text = " ".join(
        query.query.lower()
        for query in queries
    )

    assert "mutation" in query_text
    assert "prognosis" in query_text
    assert "biomarker" in query_text
    assert "survival" in query_text
    assert "therapeutic response" in query_text
    assert "nsclc" in query_text
    assert "lung adenocarcinoma" in query_text
    assert "lung squamous cell carcinoma" in query_text