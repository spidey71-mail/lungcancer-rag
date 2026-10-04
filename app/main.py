from app.ingestion.pubmed_client import PubMedClient
from app.ingestion.pubmed_parser import PubMedParser
from app.ingestion.candidate_retriever import CandidateRetriever
from app.ingestion.query_builder import LungCancerQueryBuilder
from app.knowledge.relevance import RelevanceFilter


def run_baseline_experiment() -> None:
    """
    Original single-query PubMed ingestion experiment.
    Kept as the baseline for comparison.
    """

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

        # --------------------------------------------------
        # FILTER SUMMARY
        # --------------------------------------------------

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
            f"Rejected               : {rejected_count}"
        )

        relevance_rate = (
            relevant_count / len(publications) * 100
            if publications
            else 0.0
        )

        print(
            f"Relevance rate         : "
            f"{relevance_rate:.1f}%"
        )

        # --------------------------------------------------
        # STRUCTURED PUBLICATION SUMMARY
        # --------------------------------------------------

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
        # RESULT
        # --------------------------------------------------

        print()
        print("=" * 60)
        print("BASELINE RESULT")
        print("=" * 60)

        print(
            f"Publications discovered : {len(pmids)}"
        )

        print(
            f"Successfully parsed     : {len(publications)}"
        )

        print(
            f"Failed                  : "
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


def run_candidate_retrieval_experiment() -> None:
    """
    Controlled multi-query candidate retrieval experiment.
    """

    print()
    print()
    print("=" * 60)
    print("       CONTROLLED CANDIDATE RETRIEVAL")
    print("=" * 60)

    client = PubMedClient()
    query_builder = LungCancerQueryBuilder()

    try:
        queries = query_builder.build_queries()

        retriever = CandidateRetriever(
            client=client,
            query_builder=query_builder,
        )

        candidates = retriever.retrieve(
            retmax_per_query=5,
        )

        print()
        print("-" * 60)
        print("RETRIEVAL SUMMARY")
        print("-" * 60)

        print(
            f"Query families       : {len(queries)}"
        )

        print(
            "Results per query    : 5"
        )

        raw_results = len(queries) * 5

        print(
            f"Maximum candidates   : {raw_results}"
        )

        print(
            f"Unique candidates    : {len(candidates)}"
        )

        duplicates = raw_results - len(candidates)

        print(
            f"Duplicates removed   : {duplicates}"
        )

        # --------------------------------------------------
        # QUERY COVERAGE
        # --------------------------------------------------

        print()
        print("-" * 60)
        print("QUERY COVERAGE")
        print("-" * 60)

        for query in queries:
            count = sum(
                query.name in candidate.discovered_by
                for candidate in candidates
            )

            print(
                f"{query.name:<25} "
                f"{count} unique papers"
            )

        # --------------------------------------------------
        # PROVENANCE
        # --------------------------------------------------

        print()
        print("-" * 60)
        print("CANDIDATE PROVENANCE")
        print("-" * 60)

        for candidate in candidates:
            sources = ", ".join(
                candidate.discovered_by
            )

            print(
                f"{candidate.pmid:<12} "
                f"{sources}"
            )

        print()
        print("=" * 60)
        print("CONTROLLED RETRIEVAL COMPLETE")
        print("=" * 60)

    finally:
        client.close()


def main() -> None:
    """
    Run the complete automated knowledge-construction demonstration.
    """

    run_baseline_experiment()

    run_candidate_retrieval_experiment()


if __name__ == "__main__":
    main()