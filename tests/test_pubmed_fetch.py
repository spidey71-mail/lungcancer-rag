from app.ingestion.pubmed_client import PubMedClient


def test_pubmed_fetch():
    client = PubMedClient()

    try:
        pmids = client.search(
            "lung cancer AND gene",
            retmax=2,
        )

        xml = client.fetch(pmids)

        assert xml
        assert "<PubmedArticle>" in xml

    finally:
        client.close()