import asyncio
import json
from datetime import date, timedelta

from app.agents.hotel.tools.hotelbeds_client import HotelbedsClient


async def main():

    client = HotelbedsClient()

    # Use future dates so HBX can search availability.
    check_in = date.today() + timedelta(days=30)
    check_out = check_in + timedelta(days=3)

    print("Searching Salou...")
    print("Check-in:", check_in)
    print("Check-out:", check_out)
    print()

    result = await client.search_hotels(
        city="Salou, Spain",
        check_in=check_in.isoformat(),
        check_out=check_out.isoformat(),
        adults=2,
        rooms=1,
        children=0,
        limit=10,
    )

    print("LOCAL HOTEL CANDIDATES")
    print("=" * 60)

    for hotel in result.get("content", []):

        name = (
            (hotel.get("name") or {})
            .get("content")
        )

        print(
            hotel.get("code"),
            "-",
            name,
        )

    print()
    print("LIVE HBX AVAILABILITY")
    print("=" * 60)

    available_hotels = (
        result
        .get("availability", {})
        .get("hotels", {})
        .get("hotels", [])
    )

    print(
        "Available hotels:",
        len(available_hotels),
    )

    print()

    for hotel in available_hotels:

        print(
            "Code:",
            hotel.get("code"),
            "| Name:",
            hotel.get("name"),
            "| Currency:",
            hotel.get("currency"),
        )

        for room in hotel.get("rooms", []):

            for rate in room.get("rates", []):

                print(
                    "   Price:",
                    rate.get("net"),
                )

        print("-" * 60)


if __name__ == "__main__":
    asyncio.run(main())