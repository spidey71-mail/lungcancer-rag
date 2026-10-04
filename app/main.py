from app.ingestion.pubmed_client import PubMedClient


def main():
    client = PubMedClient()

    try:
        query = "lung cancer AND gene"

        print("=" * 60)
        print("LungCancer-RAG | PubMed Search")
        print("=" * 60)

        print(f"Query: {query}")
        print()

        pmids = client.search(query, retmax=10)

        print(f"Retrieved {len(pmids)} publications")
        print()

        for index, pmid in enumerate(pmids, start=1):
            print(f"{index:02d}. PMID: {pmid}")

    finally:
        client.close()


if __name__ == "__main__":
    main()