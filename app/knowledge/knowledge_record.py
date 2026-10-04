from pydantic import BaseModel, Field

from app.knowledge.evidence_score import EvidenceScore
from app.knowledge.schema import Publication


class Provenance(BaseModel):
    source: str
    pmid: str
    query: str


class KnowledgeRecord(BaseModel):
    pmid: str

    title: str
    journal: str | None = None
    publication_year: int | None = None
    doi: str | None = None

    genes: list[str] = Field(default_factory=list)

    disease_context: list[str] = Field(default_factory=list)

    molecular_evidence: list[str] = Field(default_factory=list)

    evidence_types: list[str] = Field(default_factory=list)

    evidence_score: float

    reasons: list[str] = Field(default_factory=list)

    provenance: Provenance


class KnowledgeRecordBuilder:

    def build(
        self,
        publication: Publication,
        evidence: EvidenceScore,
        source_query: str,
    ) -> KnowledgeRecord:

        provenance = Provenance(
            source="PubMed",
            pmid=publication.pmid,
            query=source_query,
        )

        return KnowledgeRecord(
            pmid=publication.pmid,
            title=publication.title,
            journal=publication.journal,
            publication_year=publication.publication_year,
            doi=publication.doi,
            genes=evidence.gene_hits,
            disease_context=evidence.disease_hits,
            molecular_evidence=evidence.molecular_hits,
            evidence_types=evidence.evidence_hits,
            evidence_score=evidence.total_score,
            reasons=evidence.reasons,
            provenance=provenance,
        )