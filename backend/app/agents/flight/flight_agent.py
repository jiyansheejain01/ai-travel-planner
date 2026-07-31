from app.agents.base.base_agent import BaseAgent
from app.agents.base.agent_state import AgentState
from app.agents.base.agent_result import AgentResult
from app.agents.flight.tools.airport_resolver import AirportResolver
from app.agents.flight.tools.flight_tool import FlightTool


class FlightAgent(BaseAgent):

    name = "flight"

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
        print("Origin:", trip.origin)
        print("Destination:", trip.destination)
        if not trip.origin or not trip.destination:
            return AgentResult(
                agent=self.name,
                success=False,
                result=None,
                error="Origin and destination are required.",
                confidence=0.0,
            )

        resolver = AirportResolver()

       

        origin = (
            trip.origin_airport
            or resolver.resolve(trip.origin)
        )

        destination = (
            trip.destination_airport
            or resolver.resolve(trip.destination)
        )

        print("Origin Airport:", origin)
        print("Destination Airport:", destination)

        if not origin or not destination:
            return AgentResult(
                agent=self.name,
                success=False,
                result=None,
                error="Unable to resolve airport codes.",
                confidence=0.0,
            )

        tool = FlightTool()

        flights = await tool.search_flights(
            origin=origin,
            destination=destination,
            departure_date=trip.start_date,
            passengers=trip.travelers or 1,
        )

        return AgentResult(
            agent=self.name,
            success=True,
            result=flights,
            confidence=0.95,
        )