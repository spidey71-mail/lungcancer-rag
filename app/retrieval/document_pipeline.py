from app.knowledge.knowledge_document import (
    KnowledgeDocument,
    KnowledgeDocumentBuilder,
)
from app.knowledge.knowledge_record import KnowledgeRecord


class DocumentPipeline:
    """
    Converts structured KnowledgeRecords into RAG-ready documents.

    The pipeline intentionally operates on validated KnowledgeRecords
    rather than raw PubMed responses.
    """

    def __init__(
        self,
        document_builder: KnowledgeDocumentBuilder | None = None,
    ):
        self.document_builder = (
            document_builder or KnowledgeDocumentBuilder()
        )

    def transform(
        self,
        record: KnowledgeRecord,
    ) -> KnowledgeDocument:

        return self.document_builder.build(record)

    def transform_many(
        self,
        records: list[KnowledgeRecord],
    ) -> list[KnowledgeDocument]:

        return [
            self.transform(record)
            for record in records
        ]