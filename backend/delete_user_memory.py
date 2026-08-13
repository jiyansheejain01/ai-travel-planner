import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

load_dotenv()

USER_ID = "26b55bbb-0976-49af-a7ae-abfdcb2a1244"
COLLECTION = "user_memory"  # actual name from qdrant_memory_store.py

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

client.delete(
    collection_name=COLLECTION,
    points_selector=Filter(
        must=[
            FieldCondition(
                key="user_id",
                match=MatchValue(value=USER_ID),
            )
        ]
    ),
)

print(f"Deleted memories for user: {USER_ID}")