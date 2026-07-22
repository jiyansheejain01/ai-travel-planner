from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel


class BaseProvider(ABC):

    @abstractmethod
    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        response_model: Type[BaseModel] | None = None,
    ):
        raise NotImplementedError