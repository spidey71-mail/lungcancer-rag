from pydantic import BaseModel, Field

from app.knowledge.knowledge_record import KnowledgeRecord


class KnowledgeDocument(BaseModel):
    text: str
    metadata: dict = Field(default_factory=dict)


class KnowledgeDocumentBuilder:

    def build(self, record: KnowledgeRecord) -> KnowledgeDocument:

        text = self._build_text(record)
        metadata = self._build_metadata(record)

        return KnowledgeDocument(
            text=text,
            metadata=metadata,
        )

    @staticmethod
    def _build_text(record: KnowledgeRecord) -> str:

        sections = [
            f"Title: {record.title}",
            f"PMID: {record.pmid}",
        ]

        if record.journal:
            sections.append(f"Journal: {record.journal}")

        if record.publication_year:
            sections.append(
                f"Publication Year: {record.publication_year}"
            )

        if record.doi:
            sections.append(f"DOI: {record.doi}")

        if record.genes:
            sections.append(
                f"Genes: {', '.join(record.genes)}"
            )

        if record.disease_context:
            sections.append(
                "Disease Context: "
                + ", ".join(record.disease_context)
            )

        if record.molecular_evidence:
            sections.append(
                "Molecular Evidence: "
                + ", ".join(record.molecular_evidence)
            )

        if record.evidence_types:
            sections.append(
                "Evidence Types: "
                + ", ".join(record.evidence_types)
            )

        sections.append(
            f"Evidence Score: {record.evidence_score:.4f}"
        )

        if record.reasons:
            sections.append(
                "Evidence Reasons: "
                + "; ".join(record.reasons)
            )

        return "\n".join(sections)

    @staticmethod
    def _build_metadata(record: KnowledgeRecord) -> dict:

        return {
            "pmid": record.pmid,
            "source": record.provenance.source,
            "query": record.provenance.query,
            "journal": record.journal,
            "publication_year": record.publication_year,
            "doi": record.doi,
            "genes": record.genes,
            "disease_context": record.disease_context,
            "molecular_evidence": record.molecular_evidence,
            "evidence_types": record.evidence_types,
            "evidence_score": record.evidence_score,
        }