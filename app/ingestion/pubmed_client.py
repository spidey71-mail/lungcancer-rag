import os

import httpx
from dotenv import load_dotenv


load_dotenv()


PUBMED_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


class PubMedClient:
    def __init__(self):
        self.api_key = os.getenv("NCBI_API_KEY")
        self.email = os.getenv("NCBI_EMAIL")
        self.tool = os.getenv("NCBI_TOOL", "lungcancer-rag")

        self.client = httpx.Client(
            base_url=PUBMED_BASE_URL,
            timeout=30.0,
        )

    def search(
        self,
        query: str,
        retmax: int = 20,
    ) -> list[str]:

        params = {
            "db": "pubmed",
            "term": query,
            "retmax": retmax,
            "retmode": "json",
            "tool": self.tool,
        }

        if self.email:
            params["email"] = self.email

        if self.api_key:
            params["api_key"] = self.api_key

        response = self.client.get(
            "/esearch.fcgi",
            params=params,
        )

        response.raise_for_status()

        data = response.json()

        return data["esearchresult"]["idlist"]

    def close(self):
        self.client.close()