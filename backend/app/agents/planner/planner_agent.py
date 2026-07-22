from app.agents.base.base_agent import BaseAgent
from app.agents.base.agent_state import AgentState
from app.agents.base.agent_result import AgentResult
from app.core.prompt_loader import PromptLoader
from app.agents.planner.schemas.trip_intent import TripIntent
from app.observability.tracer import tracer

class PlannerAgent(BaseAgent):

    name = "planner"
    prompt_name = "system.md"
    response_model = TripIntent

    async def run(
        self,
        state: AgentState,
    ) -> AgentResult:

        with tracer.start_as_current_span("planner.reasoning") as span:

            span.set_attribute("agent.name", self.name)
            span.set_attribute("planner.prompt", self.prompt_name)

            system_prompt = PromptLoader.load(
                agent_name=self.name,
                prompt_name=self.prompt_name,
            )

            response = await self.call_llm(
                system_prompt=system_prompt,
                user_prompt=state.user_input,
            )

            span.set_attribute(
                "planner.response_received",
                True,
            )

            return AgentResult(
                agent=self.name,
                success=True,
                result=response,
                confidence=0.95,
            )