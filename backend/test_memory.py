import asyncio
from datetime import datetime

from app.agents.memory.qdrant_memory_store import QdrantMemoryStore
from app.agents.memory.schemas import MemoryRecord


async def main():
    store = QdrantMemoryStore()

    # Add a real memory
    await store.add_memory(
        MemoryRecord(
            user_id="u1",
            memory_type="preference",
            text="User prefers vegetarian food and quiet beaches",
            created_at=datetime.utcnow(),
        )
    )

    # Semantic search
    results = await store.search_memories(
        user_id="u1",
        query="Plan a relaxing Bali beach vacation with good vegetarian food",
        limit=5,
    )

    print("\n=== SEMANTIC SEARCH RESULTS ===")

    for r in results:
        print(f"Score: {r.score:.3f}")
        print(f"Type : {r.memory_type}")
        print(f"Text : {r.text}")
        print()


if __name__ == "__main__":
    asyncio.run(main())