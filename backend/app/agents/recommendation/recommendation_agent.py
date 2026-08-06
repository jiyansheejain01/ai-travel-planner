from app.agents.base.base_agent import BaseAgent
from app.agents.base.agent_state import AgentState
from app.agents.base.agent_result import AgentResult

from app.agents.recommendation.schemas.recommendation_result import RecommendationResult
from app.agents.recommendation.tools.recommendation_tool import RecommendationTool

from app.core.prompt_loader import PromptLoader
from app.observability.tracer import tracer


class RecommendationAgent(BaseAgent):
    """
    Synthesizes a short, personalized shortlist of places/experiences for
    the traveler, built on top of the Attraction Agent's candidate list and
    the Weather Agent's forecast -- rather than just dumping raw search
    results, it explains *why* each pick fits this specific trip.
    """

    name = "recommendation"

    prompt_name = "system.md"

    response_model = RecommendationResult

    def __init__(self, llm_provider):
        super().__init__(llm_provider)
        self.tool = RecommendationTool()

    async def run(
        self,
        state: AgentState,
    ) -> AgentResult:

        with tracer.start_as_current_span("recommendation.reasoning") as span:

            span.set_attribute("agent.name", self.name)
            span.set_attribute("recommendation.prompt", self.prompt_name)

            # --------------------------------------------------------
            # 1. Get trip intent
            # --------------------------------------------------------

            trip = state.trip

            if trip is None:
                return AgentResult(
                    agent=self.name,
                    success=False,
                    result=None,
                    error="Trip intent not found.",
                    confidence=0.0,
                )

            # --------------------------------------------------------
            # 2. Validate destination
            # --------------------------------------------------------

            if not trip.destination:
                return AgentResult(
                    agent=self.name,
                    success=False,
                    result=None,
                    error="Destination is required for recommendations.",
                    confidence=0.0,
                )

            # --------------------------------------------------------
            # 3. Pull context from previously executed agents
            # --------------------------------------------------------

            attraction_result = state.previous_results.get("attraction")
            attractions = attraction_result.result if attraction_result else None

            weather_result = state.previous_results.get("weather")
            weather = weather_result.result if weather_result else None

            try:

                # ----------------------------------------------------
                # 4. Build context and call the LLM
                # ----------------------------------------------------

                user_prompt = await self.tool.build_context(
                    trip=trip,
                    attractions=attractions,
                    weather=weather,
                )

                system_prompt = PromptLoader.load(
                    agent_name=self.name,
                    prompt_name=self.prompt_name,
                )

                response = await self.call_llm(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                )

                span.set_attribute("recommendation.response_received", True)

                # ----------------------------------------------------
                # 5. Return result
                # ----------------------------------------------------

                confidence = 0.9 if attractions and attractions.attractions else 0.5

                return AgentResult(
                    agent=self.name,
                    success=True,
                    result=response,
                    confidence=confidence,
                )

            except Exception as exc:

                span.record_exception(exc)
                span.set_attribute("agent.success", False)

                return AgentResult(
                    agent=self.name,
                    success=False,
                    result=None,
                    error=str(exc),
                    confidence=0.0,
                )
