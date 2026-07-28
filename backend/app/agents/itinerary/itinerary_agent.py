from app.agents.base.base_agent import BaseAgent
from app.agents.base.agent_result import AgentResult
from app.agents.base.agent_state import AgentState

from app.agents.itinerary.schemas.itinerary_result import ItineraryResult
from app.agents.itinerary.tools.itinerary_tool import ItineraryTool

from app.core.prompt_loader import PromptLoader
from app.observability.tracer import tracer


class ItineraryAgent(BaseAgent):

    name = "itinerary"

    prompt_name = "system.md"

    response_model = ItineraryResult

    def __init__(self, llm_provider):
        super().__init__(llm_provider)
        self.tool = ItineraryTool()

    async def run(
        self,
        state: AgentState,
    ) -> AgentResult:

        with tracer.start_as_current_span("itinerary.reasoning") as span:

            span.set_attribute("agent.name", self.name)
            span.set_attribute(
                "itinerary.prompt",
                self.prompt_name,
            )

            if state.trip is None:
                raise ValueError(
                    "TripIntent is required before itinerary generation."
                )

            weather = (
                state.previous_results.get("weather").result
                if state.previous_results.get("weather")
                else None
            )

            flight = (
                state.previous_results.get("flight").result
                if state.previous_results.get("flight")
                else None
            )

            hotel = (
                state.previous_results.get("hotel").result
                if state.previous_results.get("hotel")
                else None
            )

            user_prompt = await self.tool.build_context(
                trip=state.trip,
                weather=weather,
                flight=flight,
                hotel=hotel,
            )

            system_prompt = PromptLoader.load(
                agent_name=self.name,
                prompt_name=self.prompt_name,
            )

            response = await self.call_llm(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
            )

            span.set_attribute(
                "itinerary.response_received",
                True,
            )

            return AgentResult(
                agent=self.name,
                success=True,
                result=response,
                confidence=0.95,
            )