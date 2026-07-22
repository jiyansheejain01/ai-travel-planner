from app.agents.weather.schemas.weather_forecast import WeatherForecast
from app.agents.weather.tools.weather_client import WeatherClient


WEATHER_CODES = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing Rime Fog",
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Dense Drizzle",
    61: "Slight Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    71: "Slight Snow",
    73: "Moderate Snow",
    75: "Heavy Snow",
    80: "Rain Showers",
    81: "Heavy Rain Showers",
    82: "Violent Rain Showers",
    95: "Thunderstorm",
}


def build_travel_advice(condition: str) -> str:
    if "Rain" in condition:
        return "Carry an umbrella and waterproof clothing."

    if "Snow" in condition:
        return "Wear warm clothing and winter boots."

    if "Fog" in condition:
        return "Drive carefully due to reduced visibility."

    if "Thunderstorm" in condition:
        return "Avoid outdoor activities if possible."

    return "Weather looks suitable for sightseeing."


class WeatherTool:

    def __init__(self):
        self.client = WeatherClient()

    async def get_weather(
        self,
        destination: str,
    ) -> WeatherForecast:

        latitude, longitude = await self.client.get_coordinates(
            destination
        )

        weather = await self.client.get_current_weather(
            latitude,
            longitude,
        )

        current = weather["current"]

        condition = WEATHER_CODES.get(
            current["weather_code"],
            "Unknown",
        )

        return WeatherForecast(
            location=destination,
            summary=f"The current weather in {destination} is {condition.lower()}.",
            temperature_c=current["temperature_2m"],
            condition=condition,
            travel_advice=build_travel_advice(condition),
        )