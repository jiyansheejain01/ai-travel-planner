import asyncio
import httpx

from app.core.config import settings
import json


async def main():
    headers = {
        "Authorization": f"Bearer {settings.DUFFEL_API_TOKEN}",
        "Duffel-Version": "v2",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    payload = {
        "data": {
            "slices": [
                {
                    "origin": "BLR",
                    "destination": "DEL",
                    "departure_date": "2026-08-15",
                }
            ],
            "passengers": [
                {
                    "type": "adult"
                }
            ],
            "cabin_class": "economy",
        }
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            f"{settings.DUFFEL_BASE_URL}/air/offer_requests",
            headers=headers,
            json=payload,
        )

        print("Status Code:", response.status_code)
        print()
        print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())