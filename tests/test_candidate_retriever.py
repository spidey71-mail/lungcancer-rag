from app.ingestion.candidate_retriever import CandidateRetriever
from app.ingestion.query_builder import PubMedQuery


class FakeClient:

    def search(self, query: str, retmax: int = 5):

        results = {
            "query_a": ["100", "200"],
            "query_b": ["200", "300"],
        }

        return results.get(query, [])


class FakeQueryBuilder:

    def build_queries(self):

        return [
            PubMedQuery(
                name="query_a",
                query="query_a",
                purpose="Test query A",
            ),
            PubMedQuery(
                name="query_b",
                query="query_b",
                purpose="Test query B",
            ),
        ]


def test_candidate_retriever_deduplicates():

    retriever = CandidateRetriever(
        client=FakeClient(),
        query_builder=FakeQueryBuilder(),
    )

    candidates = retriever.retrieve(
        retmax_per_query=5,
    )

    pmids = {
        candidate.pmid
        for candidate in candidates
    }

    assert pmids == {
        "100",
        "200",
        "300",
    }


def test_candidate_retriever_tracks_query_sources():

    retriever = CandidateRetriever(
        client=FakeClient(),
        query_builder=FakeQueryBuilder(),
    )

    candidates = retriever.retrieve(
        retmax_per_query=5,
    )

    candidate_200 = next(
        candidate
        for candidate in candidates
        if candidate.pmid == "200"
    )

    assert candidate_200.discovered_by == [
        "query_a",
        "query_b",
    ]