from app.ingestion.pubmed_client import PubMedClient


def test_pubmed_search():
    client = PubMedClient()

    try:
        pmids = client.search(
            "lung cancer AND gene",
            retmax=5,
        )

        assert len(pmids) > 0
        assert all(pmid.isdigit() for pmid in pmids)

    finally:
        client.close()