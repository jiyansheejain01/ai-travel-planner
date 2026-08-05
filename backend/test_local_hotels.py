import asyncio

from app.agents.hotel.tools.hotelbeds_client import HotelbedsClient


async def main():

    client = HotelbedsClient()

    hotels = await client.find_hotels_by_city(
        city="Salou, Spain",
        limit=10,
        radius_km=30,
    )

    print()
    print("Hotels found:", len(hotels))
    print()

    for hotel in hotels:

        print(
            hotel.get("code"),
            "-",
            hotel.get("name", {}).get("content"),
            "-",
            hotel.get("coordinates"),
        )


if __name__ == "__main__":
    asyncio.run(main())