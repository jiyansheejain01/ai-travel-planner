from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from app.agents.base.agent_state import AgentState
from app.agents.base.agent_result import AgentResult

from app.observability.tracer import tracer


class BaseAgent(ABC):
    """
    Base class for every AI agent.

    Responsibilities:
    - Build prompts
    - Call the LLM
    - Execute tools
    - Return structured AgentResult
    """

    name: str = "base"

    def __init__(self, llm_provider: Any):
        self.llm = llm_provider

    async def execute(self, state: AgentState) -> AgentResult:
        """
        Public entry point for every agent.
        """

        with tracer.start_as_current_span(f"agent.{self.name}") as span:

            span.set_attribute("agent.name", self.name)
            span.set_attribute("agent.class", self.__class__.__name__)

            try:
                result = await self.run(state)

                span.set_attribute("agent.success", result.success)
                span.set_attribute("agent.confidence", result.confidence)

                return result

            except Exception as e:

                span.record_exception(e)
                span.set_attribute("agent.success", False)

                return AgentResult(
                    agent=self.name,
                    success=False,
                    result=None,
                    error=str(e),
                    confidence=0.0,
                )

    @abstractmethod
    async def run(self, state: AgentState) -> AgentResult:
        """
        Agent-specific reasoning.
        """
        raise NotImplementedError

    async def call_llm(
        self,
        system_prompt: str,
        user_prompt: str,
    ):
        """
        Shared LLM call.
        """

        with tracer.start_as_current_span("llm.call") as span:

            span.set_attribute("agent.name", self.name)

            response = await self.llm.generate(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_model=getattr(
                    self,
                    "response_model",
                    None,
                ),
            )

            return response

    async def execute_tool(
        self,
        tool,
        **kwargs,
    ):
        """
        Shared tool execution.
        """

        with tracer.start_as_current_span(f"tool.{tool.__name__}") as span:

            span.set_attribute("tool.name", tool.__name__)

            result = await tool(**kwargs)

            return result