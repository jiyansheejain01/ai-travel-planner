import json

from app.prompts.planner_prompt import SYSTEM_PROMPT
from app.providers.llm.provider_factory import ProviderFactory
from app.schemas.ai import PlannerResponse


class PlannerAgent:
    def __init__(self):
        self.provider = ProviderFactory.get_provider()

    async def generate(self, user_prompt: str) -> PlannerResponse:
        response = await self.provider.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        data = json.loads(response)

        return PlannerResponse.model_validate(data)