from pydantic import BaseModel, Field


class EvidenceScore(BaseModel):
    disease_score: float = Field(ge=0.0, le=1.0)
    molecular_score: float = Field(ge=0.0, le=1.0)
    evidence_score: float = Field(ge=0.0, le=1.0)
    gene_specificity_score: float = Field(ge=0.0, le=1.0)

    total_score: float = Field(ge=0.0, le=1.0)

    disease_hits: list[str] = Field(default_factory=list)
    molecular_hits: list[str] = Field(default_factory=list)
    evidence_hits: list[str] = Field(default_factory=list)
    gene_hits: list[str] = Field(default_factory=list)

    reasons: list[str] = Field(default_factory=list)