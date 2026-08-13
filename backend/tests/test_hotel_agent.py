import asyncio
from datetime import date, timedelta

from app.agents.base.agent_state import AgentState
from app.agents.hotel.hotel_agent import HotelAgent
from app.agents.planner.schemas.trip_intent import TripIntent


async def main():

    # --------------------------------------------------------
    # 1. Test dates
    # --------------------------------------------------------

    check_in = date.today() + timedelta(days=30)
    check_out = check_in + timedelta(days=3)

    # --------------------------------------------------------
    # 2. Create TripIntent
    # --------------------------------------------------------

    trip = TripIntent(
        destination="Salou, Spain",
        start_date=check_in.isoformat(),
        end_date=check_out.isoformat(),
        travelers=2,
        trip_type="hotels",
    )

    # --------------------------------------------------------
    # 3. Create AgentState
    # --------------------------------------------------------

    state = AgentState(
        user_input=(
            f"Find hotels in Salou, Spain from "
            f"{check_in.isoformat()} to "
            f"{check_out.isoformat()} for 2 travelers."
        ),
        trip=trip,
    )

    # --------------------------------------------------------
    # 4. Run HotelAgent
    # --------------------------------------------------------

    agent = HotelAgent()

    result = await agent.run(state)

    # --------------------------------------------------------
    # 5. Print AgentResult
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("HOTEL AGENT TEST")
    print("=" * 60)

    print("Agent:", result.agent)
    print("Success:", result.success)
    print("Confidence:", result.confidence)
    print("Error:", result.error)
    print()

    # --------------------------------------------------------
    # 6. Stop if agent failed
    # --------------------------------------------------------

    if not result.success:
        print("HotelAgent failed.")
        return

    hotel_result = result.result

    if hotel_result is None:
        print("HotelAgent returned no result.")
        return

    # --------------------------------------------------------
    # 7. Print hotels
    # --------------------------------------------------------

    print("City:", hotel_result.city)
    print("Check-in:", hotel_result.check_in)
    print("Check-out:", hotel_result.check_out)
    print()

    print(
        "Hotels returned:",
        len(hotel_result.hotels),
    )

    print()

    for index, hotel in enumerate(
        hotel_result.hotels,
        start=1,
    ):

        print(
            f"{index}. {hotel.name}"
        )

        print(
            "   ID:",
            hotel.hotel_id,
        )

        print(
            "   Address:",
            hotel.address,
        )

        print(
            "   Rating:",
            hotel.rating,
        )

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