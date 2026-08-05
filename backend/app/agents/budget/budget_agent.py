from app.agents.base.base_agent import BaseAgent
from app.agents.base.agent_state import AgentState
from app.agents.base.agent_result import AgentResult

from app.agents.budget.tools.budget_tool import BudgetTool


class BudgetAgent(BaseAgent):
    """
    Computes a currency-normalized budget breakdown for the trip and
    checks it against the user's stated budget.

    Deliberately does not use an LLM -- like FlightAgent/HotelAgent/
    WeatherAgent, this is a deterministic, tool-driven agent, so every
    number it returns is traceable back to either a real price from
    another agent or one of the documented estimate_cost.py heuristics.
    """

    name = "budget"

    async def run(
        self,
        state: AgentState,
    ) -> AgentResult:

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
        # 2. Pull in whatever upstream agents produced
        # --------------------------------------------------------

        flight_result = state.previous_results.get("flight")
        hotel_result = state.previous_results.get("hotel")
        itinerary_result = state.previous_results.get("itinerary")

        flight = (
            flight_result.result
            if flight_result and flight_result.success
            else None
        )

        hotel = (
            hotel_result.result
            if hotel_result and hotel_result.success
            else None
        )

        itinerary = (
            itinerary_result.result
            if itinerary_result and itinerary_result.success
            else None
        )

        # --------------------------------------------------------
        # 3. Build the budget breakdown
        # --------------------------------------------------------

        tool = BudgetTool()

        try:

            budget = await tool.build_budget(
                trip=trip,
                flight=flight,
                hotel=hotel,
                itinerary=itinerary,
            )

            # ----------------------------------------------------
            # 4. Return result
            # ----------------------------------------------------

            confidence = 0.6 if budget.incomplete else 0.9

            return AgentResult(
                agent=self.name,
                success=True,
                result=budget,
                confidence=confidence,
            )

        except Exception as exc:

            return AgentResult(
                agent=self.name,
                success=False,
                result=None,
                error=str(exc),
                confidence=0.0,
            )
