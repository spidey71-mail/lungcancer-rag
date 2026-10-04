import httpx


PUBMED_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


class PubMedClient:
    def __init__(self):
        self.client = httpx.Client(
            base_url=PUBMED_BASE_URL,
            timeout=30.0,
        )

    def search(
        self,
        query: str,
        retmax: int = 20,
    ) -> list[str]:

        response = self.client.get(
            "/esearch.fcgi",
            params={
                "db": "pubmed",
                "term": query,
                "retmax": retmax,
                "retmode": "json",
            },
        )

        response.raise_for_status()

        data = response.json()

        return data["esearchresult"]["idlist"]

    def close(self):
        self.client.close()