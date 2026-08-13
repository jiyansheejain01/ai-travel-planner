import asyncio
from datetime import date, timedelta

from app.agents.hotel.tools.hotel_tool import HotelTool


async def main():

    tool = HotelTool()

    check_in = date.today() + timedelta(days=30)
    check_out = check_in + timedelta(days=3)

    print()
    print("=" * 60)
    print("HOTEL TOOL TEST")
    print("=" * 60)

    print("City: Salou, Spain")
    print("Check-in:", check_in)
    print("Check-out:", check_out)
    print()

    result = await tool.search_hotels(
        city="Salou, Spain",
        check_in=check_in.isoformat(),
        check_out=check_out.isoformat(),
    )

    print("Hotels returned:", len(result.hotels))
    print()

    for index, hotel in enumerate(
        result.hotels,
        start=1,
    ):

        print(f"{index}. {hotel.name}")
        print("   ID:", hotel.hotel_id)
        print("   Address:", hotel.address)
        print("   Rating:", hotel.rating)
        print(
            "   Price:",
            hotel.price,
            hotel.currency,
        )
        print(
            "   Coordinates:",
            hotel.latitude,
            hotel.longitude,
        )
        print()


if __name__ == "__main__":
    asyncio.run(main())