import asyncio

import httpx


class WeatherClient:

    GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
    FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

    TIMEOUT = 10.0
    MAX_RETRIES = 2

    async def _get(
        self,
        url: str,
        params: dict,
    ) -> dict:
        """
        Make a GET request with timeout and retry handling.
        """

        last_exception = None

        for attempt in range(self.MAX_RETRIES + 1):

            try:
                timeout = httpx.Timeout(
                    self.TIMEOUT,
                    connect=self.TIMEOUT,
                )

                async with httpx.AsyncClient(
                    timeout=timeout,
                ) as client:

                    response = await client.get(
                        url,
                        params=params,
                    )

                    response.raise_for_status()

                    return response.json()

            except (
                httpx.TimeoutException,
                httpx.ConnectError,
                httpx.NetworkError,
            ) as exc:

                last_exception = exc

                # No more retries left
                if attempt >= self.MAX_RETRIES:
                    break

                # Small delay before retrying
                await asyncio.sleep(1)

            except httpx.HTTPStatusError as exc:

                status_code = exc.response.status_code

                raise RuntimeError(
                    f"Weather API returned HTTP "
                    f"{status_code}: "
                    f"{exc.response.text}"
                ) from exc

        # If all retry attempts failed
        raise RuntimeError(
            "Weather service could not be reached "
            f"after {self.MAX_RETRIES + 1} attempts. "
            f"Last error: "
            f"{type(last_exception).__name__}"
        ) from last_exception

    async def get_coordinates(
        self,
        city: str,
    ) -> tuple[float, float]:
        """
        Convert a city name into latitude and longitude.
        """

        data = await self._get(
            self.GEOCODING_URL,
            params={
                "name": city,
                "count": 1,
            },
        )

        results = data.get("results")

        if not results:
            raise ValueError(
                f"City '{city}' not found."
            )

        result = results[0]

        return (
            result["latitude"],
            result["longitude"],
        )

    async def get_current_weather(
        self,
        latitude: float,
        longitude: float,
    ) -> dict:
        """
        Get current weather from Open-Meteo.
        """

        return await self._get(
            self.FORECAST_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,weather_code"
                ),
            },
        )