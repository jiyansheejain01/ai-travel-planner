from app.core.config import settings
from app.providers.llm.groq_provider import GroqProvider


class ProviderFactory:
    @staticmethod
    def get_provider():
        if settings.AI_PROVIDER.lower() == "groq":
            return GroqProvider()

        raise ValueError(
            f"Unsupported AI provider: {settings.AI_PROVIDER}"
        )