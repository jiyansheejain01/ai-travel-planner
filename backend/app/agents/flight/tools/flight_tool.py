from __future__ import annotations

from app.agents.flight.schemas.flight_result import (
    FlightOption,
    FlightResult,
)
from app.agents.flight.tools.flight_client import FlightClient


class FlightTool:
    """
    Converts raw Duffel API responses into our internal FlightResult schema.
    """

    def __init__(self) -> None:
        self.client = FlightClient()

    async def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        passengers: int = 1,
    ) -> FlightResult:

        response = await self.client.search_flights(
            origin=origin,
            destination=destination,
            departure_date=departure_date,
            passengers=passengers,
        )

        data = response["data"]

        flights: list[FlightOption] = []

        for offer in data.get("offers", []):

            try:
                first_slice = offer["slices"][0]

                segments = first_slice["segments"]

                first_segment = segments[0]
                last_segment = segments[-1]

                flights.append(
                    FlightOption(
                        airline=first_segment["marketing_carrier"]["iata_code"],
                        flight_number=first_segment["marketing_carrier_flight_number"],
                        departure_airport=first_segment["origin"]["iata_code"],
                        arrival_airport=last_segment["destination"]["iata_code"],
                        departure_time=first_segment["departing_at"],
                        arrival_time=last_segment["arriving_at"],
                        duration=first_slice["duration"],
                        price=float(offer["total_amount"]),
                        currency=offer["total_currency"],
                    )
                )

            except KeyError:
                # Skip malformed offers
                continue

        return FlightResult(
            origin=origin,
            destination=destination,
            departure_date=departure_date,
            flights=flights,
        )