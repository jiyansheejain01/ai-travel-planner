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
                error="Destination is required for hotel search.",
                confidence=0.0,
            )

        # --------------------------------------------------------
        # 3. Validate dates
        # --------------------------------------------------------

        if not trip.start_date:
            return AgentResult(
                agent=self.name,
                success=False,
                result=None,
                error="Check-in date is required for hotel search.",
                confidence=0.0,
            )

        if not trip.end_date:
            return AgentResult(
                agent=self.name,
                success=False,
                result=None,
                error="Check-out date is required for hotel search.",
                confidence=0.0,
            )

        # --------------------------------------------------------
        # 4. Search hotels
        # --------------------------------------------------------

        tool = HotelTool()

        try:

            hotels = await tool.search_hotels(
                city=trip.destination,
                check_in=trip.start_date,
                check_out=trip.end_date,
            )

            # ----------------------------------------------------
            # 5. Return result
            # ----------------------------------------------------

            return AgentResult(
                agent=self.name,
                success=True,
                result=hotels,
                confidence=0.95,
            )

        except Exception as exc:

            return AgentResult(
                agent=self.name,
                success=False,
                result=None,
                error=str(exc),
                confidence=0.0,
            )