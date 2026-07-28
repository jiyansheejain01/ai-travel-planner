import httpx

from app.core.config import settings


class HotelClient:
    """
    Client for interacting with the Geoapify Places API.
    """

    GEOCODE_URL = "https://api.geoapify.com/v1/geocode/search"
    PLACES_URL = "https://api.geoapify.com/v2/places"

    async def _get_coordinates(self, city: str):
        """
        Convert a city name into latitude and longitude.
        """

        params = {
            "text": city,
            "apiKey": settings.GEOAPIFY_API_KEY,
            "limit": 1,
        }

        async with httpx.AsyncClient(timeout=30) as client:

            response = await client.get(
                self.GEOCODE_URL,
                params=params,
            )

            response.raise_for_status()

            data = response.json()["features"]

            if not data:
                raise RuntimeError(f"City '{city}' not found.")

            coordinates = data[0]["geometry"]["coordinates"]

            return coordinates[1], coordinates[0]   # lat, lon

    async def search_hotels(
        self,
        city: str,
        radius: int = 5000,
    ):
        """
        Search hotels in a city.
        """

        lat, lon = await self._get_coordinates(city)

        params = {
            "categories": "accommodation.hotel",
            "filter": f"circle:{lon},{lat},{radius}",
            "limit": 20,
            "apiKey": settings.GEOAPIFY_API_KEY,
        }

        async with httpx.AsyncClient(timeout=30) as client:

            response = await client.get(
                self.PLACES_URL,
                params=params,
            )

            response.raise_for_status()

            return response.json()