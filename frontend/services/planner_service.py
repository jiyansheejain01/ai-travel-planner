import httpx

BASE_URL = "http://localhost:8000"


async def plan_trip(prompt: str):
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(
            f"{BASE_URL}/planner/",
            json={
                    "message": prompt
            }
        )

    response.raise_for_status()
    return response.json()