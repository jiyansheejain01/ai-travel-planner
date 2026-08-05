from __future__ import annotations

import json
from pathlib import Path

from app.agents.flight.tools.flight_client import FlightClient


class AirportResolver:
    """
    Resolves city names to IATA airport codes.

    Resolution order:
    1. Local airports.json
    2. Duffel Place Suggestions API
    """

    def __init__(self) -> None:

        data_file = (
            Path(__file__).parent.parent
            / "data"
            / "airports.json"
        )

        with open(
            data_file,
            "r",
            encoding="utf-8",
        ) as f:
            self.airports = json.load(f)

        self.client = FlightClient()

    async def resolve(
        self,
        city: str | None,
    ) -> str | None:
        """
        Return an IATA code for a city/airport.
        """

        if not city:
            return None

        query = city.strip()
        normalized_city = query.lower()

        # -----------------------------------------------------
        # 1. Try local airport cache first
        # -----------------------------------------------------

        local_code = self.airports.get(
            normalized_city
        )

        if local_code:
            return local_code

        # -----------------------------------------------------
        # 2. Ask Duffel
        # -----------------------------------------------------

        try:
            response = await self.client.search_places(
                query=query,
            )

            places = response.get(
                "data",
                [],
            )

            if not places:
                return None

            # -------------------------------------------------
            # 3. Find first result containing an IATA code
            # -------------------------------------------------

            for place in places:

                iata_code = place.get(
                    "iata_code"
                )

                if iata_code:
                    return iata_code

        except Exception as exc:
            print(
                f"Airport resolution failed for "
                f"{query}: {exc}"
            )

        return None