from typing import Type

import instructor
from groq import AsyncGroq
from pydantic import BaseModel

from app.core.config import settings
from app.observability.tracer import tracer
from app.providers.llm.base_provider import BaseProvider


class GroqProvider(BaseProvider):
    def __init__(self):
        client = AsyncGroq(api_key=settings.GROQ_API_KEY)

        self.client = instructor.from_groq(client)

        self.model = settings.GROQ_MODEL

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        response_model: Type[BaseModel] | None = None,
    ):

        with tracer.start_as_current_span("provider.groq") as span:

            span.set_attribute("provider.name", "groq")
            span.set_attribute("provider.model", self.model)

            try:

                if response_model:

                    response = await self.client.chat.completions.create(
                        model=self.model,
                        response_model=response_model,
                        messages=[
                            {
                                "role": "system",
                                "content": system_prompt,
                            },
                            {
                                "role": "user",
                                "content": user_prompt,
                            },
                        ],
                        temperature=0.7,
                    )

                    return response

                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt,
                        },
                        {
                            "role": "user",
                            "content": user_prompt,
                        },
                    ],
                    temperature=0.7,
                )

                return response.choices[0].message.content.strip()

            except Exception as e:
                span.record_exception(e)
                span.set_attribute("provider.success", False)
                raise