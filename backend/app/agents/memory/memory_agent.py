from datetime import datetime
from .qdrant_memory_store import QdrantMemoryStore
from .schemas import MemoryRecord


class MemoryAgent:
    def __init__(self):
        self.store = QdrantMemoryStore()

    async def remember_preference(self, user_id: str, text: str):
        memory = MemoryRecord(
            user_id=user_id,
            memory_type="preference",
            text=text,
            created_at=datetime.utcnow(),
            importance=0.8,
        )

        await self.store.add_memory(memory)

    async def remember_feedback(self, user_id: str, text: str):
        memory = MemoryRecord(
            user_id=user_id,
            memory_type="feedback",
            text=text,
            created_at=datetime.utcnow(),
            importance=0.7,
        )

        await self.store.add_memory(memory)

    async def get_relevant_context(
        self,
        user_id: str,
        current_request: str,
    ) -> str:

        memories = await self.store.search_memories(
            user_id=user_id,
            query=current_request,
            limit=5,
        )

        print("\nMEMORY DEBUG:")
        for m in memories:
            print(m.score, m.text)

        # Remove duplicates while preserving order
        unique_texts = list(dict.fromkeys(m.text for m in memories))

        lines = [f"- {text}" for text in unique_texts]

        return "\n".join(lines)