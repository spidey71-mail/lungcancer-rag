from __future__ import annotations

from typing import Any
from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams


class VectorStore:
    def __init__(
        self,
        url: str = "http://localhost:7000",
        collection_name: str = "lung_cancer_knowledge",
        vector_size: int = 3,
    ):
        self.client = QdrantClient(url=url)
        self.collection_name = collection_name
        self.vector_size = vector_size

        self._ensure_collection()

    def _ensure_collection(self) -> None:
        collections = self.client.get_collections()

        exists = any(
            collection.name == self.collection_name
            for collection in collections.collections
        )

        if not exists:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE,
                ),
            )

    def add(
        self,
        vector: list[float],
        text: str,
        metadata: dict[str, Any],
    ) -> None:

        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=str(uuid4()),
                    vector=vector,
                    payload={
                        "text": text,
                        "metadata": metadata,
                    },
                )
            ],
        )

    def search(
        self,
        query_vector: list[float],
        limit: int = 5,
    ) -> list[dict[str, Any]]:

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            with_payload=True,
        ).points

        return [
            {
                "id": result.id,
                "score": result.score,
                "text": result.payload.get("text"),
                "metadata": result.payload.get("metadata", {}),
            }
            for result in results
        ]

    def count(self) -> int:
        collection = self.client.get_collection(
            self.collection_name
        )

        return collection.points_count or 0

    def delete_collection(self) -> None:
        self.client.delete_collection(
            collection_name=self.collection_name
        )