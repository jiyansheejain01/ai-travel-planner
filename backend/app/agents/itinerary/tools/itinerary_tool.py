from app.agents.flight.schemas.flight_result import FlightResult
from app.agents.hotel.schemas.hotel_result import HotelResult
from app.agents.planner.schemas.trip_intent import TripIntent
from app.agents.weather.schemas.weather_forecast import WeatherForecast


class ItineraryTool:
    """
    Prepares context for the Itinerary Agent.

    Unlike WeatherTool or FlightTool, this tool does not call
    any external APIs. It simply formats data from previous
    agents into a prompt-friendly string.
    """

    async def build_context(
        self,
        trip: TripIntent,
        weather: WeatherForecast | None,
        flight: FlightResult | None,
        hotel: HotelResult | None,
    ) -> str:

        lines = []

        # -------------------------------
        # Trip Information
        # -------------------------------
        lines.append("Trip Information")
        lines.append(f"Destination: {trip.destination}")
        lines.append(f"Origin: {trip.origin}")
        lines.append(f"Start Date: {trip.start_date}")
        lines.append(f"End Date: {trip.end_date}")
        lines.append(f"Duration: {trip.duration_days} days")
        lines.append(f"Travelers: {trip.travelers}")
        lines.append(f"Budget: {trip.budget}")
        lines.append(f"Trip Type: {trip.trip_type}")
        lines.append(f"Interests: {', '.join(trip.interests or [])}")

        # -------------------------------
        # Weather
        # -------------------------------
        if weather:
            lines.append("")
            lines.append("Weather")
            lines.append(weather.summary)
            lines.append(f"Temperature: {weather.temperature_c}°C")
            lines.append(f"Condition: {weather.condition}")
            lines.append(f"Advice: {weather.travel_advice}")

        # -------------------------------
        # Flights
        # -------------------------------
        if flight and flight.flights:

            selected = flight.flights[0]

            lines.append("")
            lines.append("Flight")

            lines.append(
                f"{selected.airline} {selected.flight_number}"
            )

            lines.append(
                f"Departure: {selected.departure_time}"
            )

            lines.append(
                f"Arrival: {selected.arrival_time}"
            )

        # -------------------------------
        # Hotel
        # -------------------------------
        if hotel and hotel.hotels:

            selected = hotel.hotels[0]

            lines.append("")
            lines.append("Hotel")

            lines.append(selected.name)
            lines.append(selected.address)

        return "\n".join(lines)