from app.agents.attraction.schemas.attraction_result import AttractionResult
from app.agents.planner.schemas.trip_intent import TripIntent
from app.agents.weather.schemas.weather_forecast import WeatherForecast


class RecommendationTool:
    """
    Prepares context for the Recommendation Agent.

    Like ItineraryTool, this tool does not call any external APIs. It
    formats the trip intent plus the Attraction and Weather agents'
    results into a prompt-friendly string the LLM can reason over.
    """

    async def build_context(
        self,
        trip: TripIntent,
        attractions: AttractionResult | None,
        weather: WeatherForecast | None,
    ) -> str:

        lines: list[str] = []

        # -------------------------------
        # Trip Information
        # -------------------------------
        lines.append("Trip Information")
        lines.append(f"Destination: {trip.destination}")
        lines.append(f"Duration: {trip.duration_days} days")
        lines.append(f"Travelers: {trip.travelers}")
        lines.append(f"Budget: {trip.budget}")
        lines.append(f"Trip Type: {trip.trip_type}")
        lines.append(f"Interests: {', '.join(trip.interests or []) or 'Not specified'}")

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
        # Candidate Attractions
        # -------------------------------
        if attractions and attractions.attractions:

            lines.append("")
            lines.append("Candidate Places (from local search -- pick and personalize from these, do not invent new ones)")

            for place in attractions.attractions:

                descriptor = place.category

                if place.address:
                    descriptor += f" -- {place.address}"

                lines.append(f"- {place.name} ({descriptor})")

        else:
            lines.append("")
            lines.append("No candidate places were found for this destination.")

        return "\n".join(lines)
