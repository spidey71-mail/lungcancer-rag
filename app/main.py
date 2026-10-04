from app.ingestion.pubmed_client import PubMedClient
from app.ingestion.pubmed_parser import PubMedParser


def main():
    query = "lung cancer AND gene"
    retmax = 5

    client = PubMedClient()
    parser = PubMedParser()

    try:
        print("=" * 60)
        print("       LungCancer-RAG | Automated PubMed Ingestion")
        print("=" * 60)

        print()
        print(f"Query: {query}")

        # --------------------------------------------------
        # SEARCH
        # --------------------------------------------------

        print()
        print("-" * 60)
        print("SEARCH")
        print("-" * 60)

        pmids = client.search(
            query=query,
            retmax=retmax,
        )

        print(f"Requested publications : {retmax}")
        print(f"PMIDs retrieved        : {len(pmids)}")

        print()
        print("PMIDs:")

        for index, pmid in enumerate(pmids, start=1):
            print(f"  {index}. {pmid}")

        # --------------------------------------------------
        # ARTICLE RETRIEVAL
        # --------------------------------------------------

        print()
        print("-" * 60)
        print("ARTICLE RETRIEVAL")
        print("-" * 60)

        xml_data = client.fetch(pmids)

        print(f"Raw XML size           : {len(xml_data):,} characters")

        # --------------------------------------------------
        # PARSING
        # --------------------------------------------------

        print()
        print("-" * 60)
        print("STRUCTURED KNOWLEDGE")
        print("-" * 60)

        publications = parser.parse(xml_data)

        for index, publication in enumerate(
            publications,
            start=1,
        ):
            print()
            print(f"[{index}]")
            print(f"PMID       : {publication.pmid}")
            print(f"Title      : {publication.title}")
            print(f"Journal    : {publication.journal}")
            print(f"Year       : {publication.publication_year}")
            print(f"Authors    : {len(publication.authors)}")
            print(
                f"Abstract   : "
                f"{'Available' if publication.abstract else 'Missing'}"
            )
            print(f"DOI        : {publication.doi}")
            print(f"Keywords   : {len(publication.keywords)}")
            print(f"MeSH terms : {len(publication.mesh_terms)}")

        # --------------------------------------------------
        # SUMMARY
        # --------------------------------------------------

        print()
        print("=" * 60)
        print("RESULT")
        print("=" * 60)

        print(
            f"Publications discovered : {len(pmids)}"
        )

        print(
            f"Successfully parsed     : {len(publications)}"
        )

        print(
            f"Failed                   : "
            f"{len(pmids) - len(publications)}"
        )

        print()

        if len(pmids) == len(publications):
            print("Status: SUCCESS")
        else:
            print("Status: PARTIAL SUCCESS")

        print("=" * 60)

    finally:
        client.close()


if __name__ == "__main__":
    main()