from pydantic import BaseModel, Field

from app.knowledge.knowledge_document import KnowledgeDocument


class EvidenceChunk(BaseModel):
    text: str
    chunk_type: str

    metadata: dict = Field(default_factory=dict)


class EvidenceChunker:

    def chunk(
        self,
        document: KnowledgeDocument,
    ) -> list[EvidenceChunk]:

        metadata = document.metadata

        chunks: list[EvidenceChunk] = []

        if metadata.get("genes") or metadata.get("molecular_evidence"):
            chunks.append(
                EvidenceChunk(
                    text=self._build_molecular_chunk(document),
                    chunk_type="molecular",
                    metadata={
                        **metadata,
                        "chunk_type": "molecular",
                    },
                )
            )

        if (
            metadata.get("disease_context")
            or metadata.get("evidence_types")
        ):
            chunks.append(
                EvidenceChunk(
                    text=self._build_evidence_chunk(document),
                    chunk_type="evidence",
                    metadata={
                        **metadata,
                        "chunk_type": "evidence",
                    },
                )
            )

        return chunks

    @staticmethod
    def _build_molecular_chunk(
        document: KnowledgeDocument,
    ) -> str:

        metadata = document.metadata

        sections = [
            f"Title: {document.metadata.get('title', '')}",
        ]

        if metadata.get("genes"):
            sections.append(
                f"Genes: {', '.join(metadata['genes'])}"
            )

        if metadata.get("disease_context"):
            sections.append(
                "Disease Context: "
                + ", ".join(metadata["disease_context"])
            )

        if metadata.get("molecular_evidence"):
            sections.append(
                "Molecular Evidence: "
                + ", ".join(metadata["molecular_evidence"])
            )

        return "\n".join(sections)

    @staticmethod
    def _build_evidence_chunk(
        document: KnowledgeDocument,
    ) -> str:

        metadata = document.metadata

        sections = [
            f"Title: {metadata.get('title', '')}",
        ]

        if metadata.get("disease_context"):
            sections.append(
                "Disease Context: "
                + ", ".join(metadata["disease_context"])
            )

        if metadata.get("evidence_types"):
            sections.append(
                "Evidence Types: "
                + ", ".join(metadata["evidence_types"])
            )

        if metadata.get("evidence_score") is not None:
            sections.append(
                f"Evidence Score: "
                f"{metadata['evidence_score']:.4f}"
            )

        return "\n".join(sections)