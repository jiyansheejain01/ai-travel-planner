from app.agents.memory.qdrant_memory_store import QdrantMemoryStore

store = QdrantMemoryStore()
store.recreate_collection()