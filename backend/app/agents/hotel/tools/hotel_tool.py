from __future__ import annotations

from app.agents.hotel.schemas.hotel_result import (
    HotelOption,
    HotelResult,
)
from app.agents.hotel.tools.hotel_client import HotelClient


class HotelTool:
    """
    Converts raw Geoapify Places API responses into our internal
    HotelResult schema.
    """

    def __init__(self) -> None:
        self.client = HotelClient()

    async def search_hotels(
        self,
        city: str,
        check_in: str,
        check_out: str,
    ) -> HotelResult:

        response = await self.client.search_hotels(
            city=city,
        )

        hotels: list[HotelOption] = []

        for hotel in response.get("features", []):

            try:

                properties = hotel.get("properties", {})

                hotels.append(
                    HotelOption(
                        hotel_id=properties.get(
                            "place_id",
                            properties.get("datasource", {}).get("raw", {}).get("osm_id", ""),
                        ),
                        name=properties.get(
                            "name",
                            "Unknown Hotel",
                        ),
                        address=properties.get(
                            "formatted",
                            "Unknown Address",
                        ),
                        city=properties.get(
                            "city",
                            city,
                        ),
                        latitude=hotel.get("geometry", {})
                        .get("coordinates", [None, None])[1],
                        longitude=hotel.get("geometry", {})
                        .get("coordinates", [None, None])[0],
                        rating=None,
                        price=None,
                        currency=None,
                    )
                )

            except Exception:
                # Skip malformed hotel records
                continue

        return HotelResult(
            city=city,
            check_in=check_in,
            check_out=check_out,
            hotels=hotels,
        )