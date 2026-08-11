from qdrant_client import QdrantClient
from qdrant_client.http.models import PayloadSchemaType
from dotenv import load_dotenv
import os

load_dotenv()

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

client.create_payload_index(
    collection_name="user_memory",
    field_name="user_id",
    field_schema=PayloadSchemaType.KEYWORD,
)

print("user_id payload index created successfully")