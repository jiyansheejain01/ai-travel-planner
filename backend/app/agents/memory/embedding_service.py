import os
import cohere


class EmbeddingService:
    def __init__(self):
        self.client = cohere.Client(os.getenv("COHERE_API_KEY"))

    async def embed(self, text: str) -> list[float]:
        response = self.client.embed(
            texts=[text],
            model="embed-v4.0",
            input_type="search_document"
        )
        return response.embeddings[0]