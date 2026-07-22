import httpx


class WeatherClient:

    BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"

    async def get_coordinates(
        self,
        city: str,
    ) -> tuple[float, float]:

        async with httpx.AsyncClient() as client:

            response = await client.get(
                self.BASE_URL,
                params={
                    "name": city,
                    "count": 1,
                },
            )

            response.raise_for_status()

            data = response.json()

            if not data.get("results"):
                raise ValueError(f"City '{city}' not found.")

            result = data["results"][0]

            return (
                result["latitude"],
                result["longitude"],
            )
        
    async def get_current_weather(
        self,
        latitude: float,
        longitude: float,
    ) -> dict:

        async with httpx.AsyncClient() as client:

            response = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": "temperature_2m,weather_code",
                },
            )

            response.raise_for_status()

            return response.json()