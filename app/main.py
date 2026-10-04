from app.ingestion.pubmed_client import PubMedClient
from app.ingestion.pubmed_parser import PubMedParser
from app.knowledge.relevance import RelevanceFilter


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
        # --------------------------------------------------
        # RELEVANCE FILTER
        # --------------------------------------------------

        relevance_filter = RelevanceFilter()

        print()
        print("-" * 60)
        print("RELEVANCE FILTER")
        print("-" * 60)

        relevant_count = 0
        rejected_count = 0

        for index, publication in enumerate(
            publications,
            start=1,
        ):
            result = relevance_filter.evaluate(publication)

            status = "KEEP" if result.relevant else "REJECT"

            if result.relevant:
                relevant_count += 1
            else:
                rejected_count += 1

            print()
            print(f"[{index}] {status}")
            print(f"PMID       : {publication.pmid}")
            print(f"Title      : {publication.title}")

            print(
                f"Lung terms : "
                f"{', '.join(result.lung_cancer_hits) or 'None'}"
            )

            print(
                f"Molecular  : "
                f"{', '.join(result.molecular_hits) or 'None'}"
            )

            print(
                f"Evidence   : "
                f"{', '.join(result.evidence_hits) or 'None'}"
            )

            print(
                f"Reasons    : "
                f"{'; '.join(result.reasons) or 'None'}"
            )

        print()
        print("-" * 60)
        print("FILTER SUMMARY")
        print("-" * 60)

        print(
            f"Candidate publications : {len(publications)}"
        )

        print(
            f"Relevant (KEEP)        : {relevant_count}"
        )

        print(
            f"Rejected                : {rejected_count}"
        )

        print(
            f"Relevance rate         : "
            f"{(relevant_count / len(publications) * 100):.1f}%"
            if publications
            else "Relevance rate         : 0.0%"
        )

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