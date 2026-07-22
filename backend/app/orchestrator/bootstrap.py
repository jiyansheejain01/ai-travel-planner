from app.orchestrator.registry import AgentRegistry

from app.agents.planner.planner_agent import PlannerAgent
from app.agents.weather.weather_agent import WeatherAgent

from app.providers.llm.groq_provider import GroqProvider


def create_registry() -> AgentRegistry:
    """
    Create and populate the application's agent registry.
    """

    registry = AgentRegistry()

    llm = GroqProvider()

    agents = [
        PlannerAgent,
        WeatherAgent,
    ]

    for agent_cls in agents:
        registry.register(agent_cls(llm))

    return registry