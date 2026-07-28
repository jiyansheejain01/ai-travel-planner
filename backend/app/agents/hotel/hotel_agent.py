from app.agents.base.base_agent import BaseAgent
from app.agents.base.agent_state import AgentState
from app.agents.base.agent_result import AgentResult

from app.agents.hotel.tools.hotel_tool import HotelTool


class HotelAgent(BaseAgent):

    name = "hotel"

    async def run(
        self,
        state: AgentState,
    ) -> AgentResult:

        trip = state.trip

        if trip is None:
            return AgentResult(
                agent=self.name,
                success=False,
                result=None,
                error="Trip intent not found.",
                confidence=0.0,
            )

        if not trip.destination:
            return AgentResult(
                agent=self.name,
                success=False,
                result=None,
                error="Destination is required.",
                confidence=0.0,
            )

        tool = HotelTool()

        try:
            hotels = await tool.search_hotels(
                city=trip.destination,
                check_in=trip.start_date or "",
                check_out=trip.end_date or "",
            )

            return AgentResult(
                agent=self.name,
                success=True,
                result=hotels,
                confidence=0.95,
            )

        except Exception as e:
            return AgentResult(
                agent=self.name,
                success=False,
                result=None,
                error=str(e),
                confidence=0.0,
            )