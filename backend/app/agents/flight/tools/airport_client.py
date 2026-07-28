from __future__ import annotations

import httpx


class AirportClient:
    """
    Resolves a city name to an airport IATA code
    using the public API-Ninjas Airport API.

    Example:
        Bangalore -> BLR
        Paris -> CDG
    """

    BASE_URL = "https://api.api-ninjas.com/v1/airports"

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def get_airport_code(self, city: str) -> str | None:

        async with httpx.AsyncClient(timeout=20) as client:

            response = await client.get(
                self.BASE_URL,
                headers={
                    "X-Api-Key": self.api_key
                },
                params={
                    "city": city
                },
            )

            response.raise_for_status()

            data = response.json()

            if not data:
                return None

            return data[0]["iata"]