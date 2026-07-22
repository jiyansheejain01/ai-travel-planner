from app.agents.base.base_agent import BaseAgent
from app.agents.base.agent_state import AgentState
from app.agents.base.agent_result import AgentResult

from app.agents.weather.schemas.weather_forecast import WeatherForecast
from app.agents.weather.tools.weather_tool import WeatherTool

from app.core.prompt_loader import PromptLoader

from app.observability.tracer import tracer


class WeatherAgent(BaseAgent):

    name = "weather"
    prompt_name = "system.md"
    response_model = WeatherForecast

    async def run(
        self,
        state: AgentState,
    ) -> AgentResult:

        with tracer.start_as_current_span("weather.reasoning") as span:

            span.set_attribute("agent.name", self.name)
            span.set_attribute("weather.destination", state.trip.destination)

            system_prompt = PromptLoader.load(
                agent_name=self.name,
                prompt_name=self.prompt_name,
            )

            tool = WeatherTool()

            forecast = await tool.get_weather(
                destination=state.trip.destination,
            )

            span.set_attribute(
                "weather.response_received",
                True,
            )

            return AgentResult(
                agent=self.name,
                success=True,
                result=forecast,
                confidence=0.95,
            )