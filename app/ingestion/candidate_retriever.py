from dataclasses import dataclass

from app.ingestion.pubmed_client import PubMedClient
from app.ingestion.query_builder import LungCancerQueryBuilder


@dataclass
class CandidatePaper:
    pmid: str
    discovered_by: list[str]


class CandidateRetriever:
    """
    Executes controlled PubMed queries and creates a
    deduplicated candidate publication set.
    """

    def __init__(
        self,
        client: PubMedClient,
        query_builder: LungCancerQueryBuilder,
    ):
        self.client = client
        self.query_builder = query_builder

    def retrieve(
        self,
        retmax_per_query: int = 5,
    ) -> list[CandidatePaper]:

        candidates: dict[str, CandidatePaper] = {}

        queries = self.query_builder.build_queries()

        for query in queries:

            pmids = self.client.search(
                query.query,
                retmax=retmax_per_query,
            )

            for pmid in pmids:

                if pmid not in candidates:

                    candidates[pmid] = CandidatePaper(
                        pmid=pmid,
                        discovered_by=[query.name],
                    )

                else:

                    if query.name not in candidates[pmid].discovered_by:
                        candidates[pmid].discovered_by.append(
                            query.name
                        )

        return list(candidates.values())