import os
import uuid

from qdrant_client.http.models import PayloadSchemaType

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)

from .embedding_service import EmbeddingService
from .schemas import MemoryRecord, RetrievedMemory


# Load environment variables
load_dotenv()

COLLECTION_NAME = "user_memory"
VECTOR_SIZE = 1536  # Cohere embed-v4.0


class QdrantMemoryStore:
    """
    Persistent semantic memory store backed by Qdrant Cloud.

    Stores user-specific memories and retrieves them using semantic
    similarity search with metadata filtering by user_id.
    """

    def __init__(self):
        self.client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
        )

        self.embedder = EmbeddingService()

        # Ensure collection exists
        self._ensure_collection()


    def _ensure_collection(self):
        """
        Create the memory collection and required payload indexes.
        """

        collections = self.client.get_collections().collections
        existing = [c.name for c in collections]

        if COLLECTION_NAME not in existing:
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=VECTOR_SIZE,
                    distance=Distance.COSINE,
                ),
            )

            print(f"Created Qdrant collection: {COLLECTION_NAME}")

        # IMPORTANT: create payload index for filtering by user_id
        self.client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="user_id",
            field_schema=PayloadSchemaType.KEYWORD,
        )

        print("Created payload index for user_id")

    async def add_memory(self, memory: MemoryRecord):
        """
        Add a new semantic memory for a user.
        """

        vector = await self.embedder.embed(memory.text)

        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload={
                        "user_id": memory.user_id,
                        "memory_type": memory.memory_type,
                        "text": memory.text,
                        "created_at": memory.created_at.isoformat(),
                        "importance": memory.importance,
                    },
                )
            ],
        )

    async def search_memories(
        self,
        user_id: str,
        query: str,
        limit: int = 5,
    ) -> list[RetrievedMemory]:
        """
        Retrieve the most relevant memories for a specific user.
        """

        query_vector = await self.embedder.embed(query)

        response = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="user_id",
                        match=MatchValue(value=user_id),
                    )
                ]
            ),
            limit=limit,
        )

        return [
            RetrievedMemory(
                text=p.payload["text"],
                memory_type=p.payload["memory_type"],
                score=p.score,
            )
            for p in response.points
        ]

    async def delete_user_memories(self, user_id: str):
        """
        Delete all memories belonging to a user.
        Useful for account deletion or memory reset.
        """

        self.client.delete(
            collection_name=COLLECTION_NAME,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="user_id",
                        match=MatchValue(value=user_id),
                    )
                ]
            ),
        )

    async def health_check(self) -> bool:
        """
        Simple connectivity check for Qdrant Cloud.
        """

        try:
            self.client.get_collection(COLLECTION_NAME)
            return True
        except Exception:
            return False

    def recreate_collection(self):
        try:
            self.client.delete_collection(COLLECTION_NAME)
            print("Old collection deleted")
        except Exception:
            pass

        self._ensure_collection()
        print("New collection created")