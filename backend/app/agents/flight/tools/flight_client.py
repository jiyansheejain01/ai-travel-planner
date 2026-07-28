import httpx

from app.core.config import settings


class FlightClient:
    """Client for interacting with the Duffel Flights API."""

    def __init__(self):
        self.base_url = settings.DUFFEL_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {settings.DUFFEL_API_TOKEN}",
            "Duffel-Version": "v2",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        passengers: int = 1,
    ):
        """
        Search flight offers using the Duffel API.
        """

        payload = {
            "data": {
                "slices": [
                    {
                        "origin": origin,
                        "destination": destination,
                        "departure_date": departure_date,
                    }
                ],
                "passengers": [
                    {"type": "adult"} for _ in range(passengers)
                ],
                "cabin_class": "economy",
            }
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{self.base_url}/air/offer_requests",
                headers=self.headers,
                json=payload,
            )

            if response.status_code >= 400:
                raise RuntimeError(response.text)

            return response.json()