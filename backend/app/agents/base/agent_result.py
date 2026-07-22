from typing import Any

from pydantic import BaseModel, Field


class AgentResult(BaseModel):

    agent: str

    success: bool

    result: Any | None = None

    error: str | None = None

    confidence: float = 1.0

    execution_time: float = 0.0

    metadata: dict[str, Any] = Field(default_factory=dict)