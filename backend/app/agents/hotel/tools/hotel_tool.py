from __future__ import annotations

from app.agents.hotel.schemas.hotel_result import (
    HotelOption,
    HotelResult,
)
from app.agents.hotel.tools.hotelbeds_client import HotelbedsClient


class HotelTool:
    """
    Hotel search tool.

    Uses HBX / Hotelbeds for:
    - hotel discovery
    - availability
    - real pricing

    Converts HBX responses into our internal HotelResult schema.
    """

    def __init__(self) -> None:
        self.client = HotelbedsClient()

    async def search_hotels(
        self,
        city: str,
        check_in: str,
        check_out: str,
    ) -> HotelResult:

        # --------------------------------------------------------
        # 1. Search HBX
        # --------------------------------------------------------

        response = await self.client.search_hotels(
            city=city,
            check_in=check_in,
            check_out=check_out,
            adults=2,
            rooms=1,
            children=0,
            limit=20,
        )

        content_hotels = response.get(
            "content",
            [],
        )

        availability_data = response.get(
            "availability",
            {},
        )

        # --------------------------------------------------------
        # 2. Extract available hotels
        # --------------------------------------------------------

        available_hotels = (
            availability_data
            .get("hotels", {})
            .get("hotels", [])
        )

        # --------------------------------------------------------
        # 3. Create lookup table using HBX hotel code
        # --------------------------------------------------------

        content_lookup = {
            str(hotel.get("code")): hotel
            for hotel in content_hotels
            if hotel.get("code") is not None
        }

        # --------------------------------------------------------
        # 4. Convert HBX hotels -> HotelOption
        # --------------------------------------------------------

        hotels: list[HotelOption] = []

        for available_hotel in available_hotels:

            try:

                # ------------------------------------------------
                # Hotel code
                # ------------------------------------------------

                hotel_code = str(
                    available_hotel.get(
                        "code",
                        "",
                    )
                )

                if not hotel_code:
                    continue

                content = content_lookup.get(
                    hotel_code,
                    {},
                )

                # ------------------------------------------------
                # Hotel name
                # ------------------------------------------------

                name_data = content.get(
                    "name",
                    {},
                )

                name = name_data.get(
                    "content"
                )

                if not name:
                    name = (
                        available_hotel.get("name")
                        or "Unknown Hotel"
                    )

                # ------------------------------------------------
                # Address
                # ------------------------------------------------

                address_data = content.get(
                    "address",
                    {},
                )

                address = (
                    address_data.get("content")
                    or "Unknown Address"
                )

                # ------------------------------------------------
                # Coordinates
                # ------------------------------------------------

                coordinates = content.get(
                    "coordinates",
                    {},
                )

                latitude = coordinates.get(
                    "latitude"
                )

                longitude = coordinates.get(
                    "longitude"
                )

                # ------------------------------------------------
                # Rating
                # ------------------------------------------------

                rating = None

                category = content.get(
                    "categoryCode"
                )

                if category:

                    try:
                        rating = float(
                            str(category)[0]
                        )

                    except (
                        ValueError,
                        TypeError,
                        IndexError,
                    ):
                        rating = None

                # ------------------------------------------------
                # Find cheapest available rate
                # ------------------------------------------------

                cheapest_price = None

                rooms = available_hotel.get(
                    "rooms",
                    [],
                )

                for room in rooms:

                    rates = room.get(
                        "rates",
                        [],
                    )

                    for rate in rates:

                        net = rate.get("net")

                        if net is None:
                            continue

                        try:
                            price = float(net)

                        except (
                            ValueError,
                            TypeError,
                        ):
                            continue

                        if (
                            cheapest_price is None
                            or price < cheapest_price
                        ):
                            cheapest_price = price

                # ------------------------------------------------
                # Skip hotels without a valid price
                # ------------------------------------------------

                if cheapest_price is None:
                    continue

                # ------------------------------------------------
                # Currency
                # ------------------------------------------------

                currency = (
                    available_hotel.get(
                        "currency"
                    )
                    or "EUR"
                )

                # ------------------------------------------------
                # Create HotelOption
                # ------------------------------------------------

                hotels.append(
                    HotelOption(
                        hotel_id=hotel_code,
                        name=name,
                        address=address,
                        city=city,
                        latitude=latitude,
                        longitude=longitude,
                        rating=rating,
                        price=cheapest_price,
                        currency=currency,
                    )
                )

            except Exception:
                # One malformed hotel should not destroy
                # the entire search.
                continue

        # --------------------------------------------------------
        # 5. Sort cheapest -> most expensive
        # --------------------------------------------------------

        hotels.sort(
            key=lambda hotel: hotel.price
        )

        # --------------------------------------------------------
        # 6. Keep best 20 options
        # --------------------------------------------------------

        hotels = hotels[:20]

        # --------------------------------------------------------
        # 7. Return internal schema
        # --------------------------------------------------------

        return HotelResult(
            city=city,
            check_in=check_in,
            check_out=check_out,
            hotels=hotels,
        )