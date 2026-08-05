from app.agents.base.base_agent import BaseAgent
from app.agents.base.agent_state import AgentState
from app.agents.base.agent_result import AgentResult

from app.agents.attraction.tools.attraction_tool import AttractionTool


class AttractionAgent(BaseAgent):

    name = "attraction"

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
                error="Destination is required for attraction search.",
                confidence=0.0,
            )

        # --------------------------------------------------------
        # 3. Search attractions
        # --------------------------------------------------------

        tool = AttractionTool()

        try:

            attractions = await tool.get_attractions(
                city=trip.destination,
            )

            # ----------------------------------------------------
            # 4. Return result
            # ----------------------------------------------------

            confidence = 0.9 if attractions.attractions else 0.5

            return AgentResult(
                agent=self.name,
                success=True,
                result=attractions,
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
