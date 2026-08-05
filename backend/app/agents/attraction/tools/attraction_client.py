import asyncio

import httpx

from app.core.config import settings


class AttractionClient:
    """
    Client for the Geoapify Places API, used to find tourist
    attractions/points of interest near a destination.
    """

    GEOCODE_URL = "https://api.geoapify.com/v1/geocode/search"
    PLACES_URL = "https://api.geoapify.com/v2/places"

    # https://apidocs.geoapify.com/docs/places/ -- OSM-derived category tags.
    CATEGORIES = "tourism.sights,entertainment.museum,entertainment.culture,leisure.park"

    TIMEOUT = 30.0
    MAX_RETRIES = 2

    async def _get(self, url: str, params: dict) -> dict:

        last_exception = None

        for attempt in range(self.MAX_RETRIES + 1):

            try:
                timeout = httpx.Timeout(self.TIMEOUT, connect=self.TIMEOUT)

                async with httpx.AsyncClient(timeout=timeout) as client:

                    response = await client.get(url, params=params)

                    response.raise_for_status()

                    return response.json()

            except (
                httpx.TimeoutException,
                httpx.ConnectError,
                httpx.NetworkError,
            ) as exc:

                last_exception = exc

                if attempt >= self.MAX_RETRIES:
                    break

                await asyncio.sleep(1)

            except httpx.HTTPStatusError as exc:

                raise RuntimeError(
                    f"Geoapify API returned HTTP {exc.response.status_code}: "
                    f"{exc.response.text}"
                ) from exc

        raise RuntimeError(
            "Geoapify API could not be reached after "
            f"{self.MAX_RETRIES + 1} attempts. "
            f"Last error: {type(last_exception).__name__}"
        ) from last_exception

    async def get_coordinates(
        self,
        city: str,
    ) -> tuple[float, float]:
        """
        Convert a city name into (latitude, longitude).
        """

        data = await self._get(
            self.GEOCODE_URL,
            params={
                "text": city,
                "apiKey": settings.GEOAPIFY_API_KEY,
                "limit": 1,
            },
        )

        features = data.get("features") or []

        if not features:
            raise RuntimeError(f"City '{city}' not found.")

        coordinates = features[0]["geometry"]["coordinates"]

        return coordinates[1], coordinates[0]  # lat, lon

    async def search_attractions(
        self,
        city: str,
        radius: int = 8000,
        limit: int = 20,
    ) -> dict:
        """
        Search tourist attractions/points of interest near a city.
        Returns the raw Geoapify Places API GeoJSON response.
        """

        lat, lon = await self.get_coordinates(city)

        return await self._get(
            self.PLACES_URL,
            params={
                "categories": self.CATEGORIES,
                "filter": f"circle:{lon},{lat},{radius}",
                "bias": f"proximity:{lon},{lat}",
                "limit": limit,
                "apiKey": settings.GEOAPIFY_API_KEY,
            },
        )
