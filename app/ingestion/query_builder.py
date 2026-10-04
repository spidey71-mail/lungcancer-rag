from dataclasses import dataclass


@dataclass(frozen=True)
class PubMedQuery:
    name: str
    query: str
    purpose: str


class LungCancerQueryBuilder:
    """
    Builds controlled PubMed queries for lung-cancer
    molecular and gene-related evidence discovery.
    """

    def build_queries(self) -> list[PubMedQuery]:

        return [
            PubMedQuery(
                name="gene_mutation",
                query="lung cancer AND gene AND mutation",
                purpose="Discover gene mutation evidence in lung cancer.",
            ),
            PubMedQuery(
                name="gene_prognosis",
                query="lung cancer AND gene AND prognosis",
                purpose="Discover genes associated with prognosis.",
            ),
            PubMedQuery(
                name="gene_biomarker",
                query="lung cancer AND gene AND biomarker",
                purpose="Discover gene-based biomarker evidence.",
            ),
            PubMedQuery(
                name="gene_survival",
                query="lung cancer AND gene AND survival",
                purpose="Discover gene associations with survival.",
            ),
            PubMedQuery(
                name="gene_therapy",
                query="lung cancer AND gene AND therapeutic response",
                purpose="Discover genes associated with treatment response.",
            ),
            PubMedQuery(
                name="nsclc_gene",
                query="NSCLC AND gene",
                purpose="Discover molecular evidence specific to NSCLC.",
            ),
            PubMedQuery(
                name="luad_gene",
                query="lung adenocarcinoma AND gene",
                purpose="Discover molecular evidence specific to LUAD.",
            ),
            PubMedQuery(
                name="lusc_gene",
                query="lung squamous cell carcinoma AND gene",
                purpose="Discover molecular evidence specific to LUSC.",
            ),
        ]