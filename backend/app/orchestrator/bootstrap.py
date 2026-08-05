from app.orchestrator.registry import AgentRegistry

from app.agents.planner.planner_agent import PlannerAgent
from app.agents.weather.weather_agent import WeatherAgent
from app.agents.flight.flight_agent import FlightAgent
from app.agents.hotel.hotel_agent import HotelAgent
from app.agents.itinerary.itinerary_agent import ItineraryAgent
from app.agents.budget.budget_agent import BudgetAgent
from app.agents.attraction.attraction_agent import AttractionAgent

from app.providers.llm.groq_provider import GroqProvider


def create_registry() -> AgentRegistry:
    """
    Create and populate the application's agent registry.
    """

    registry = AgentRegistry()

    llm = GroqProvider()

    registry.register(PlannerAgent(llm))
    registry.register(WeatherAgent())
    registry.register(FlightAgent())
    registry.register(HotelAgent())
    registry.register(ItineraryAgent(llm))
    registry.register(BudgetAgent())
    registry.register(AttractionAgent())

    return registry