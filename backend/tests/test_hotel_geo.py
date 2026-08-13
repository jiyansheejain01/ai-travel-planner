import asyncio

from app.agents.hotel.tools.hotel_client import HotelClient


async def main():
    client = HotelClient()

    lat, lon = await client.get_coordinates(
        "Bangalore"
    )

    print("Latitude:", lat)
    print("Longitude:", lon)


if __name__ == "__main__":
    asyncio.run(main())