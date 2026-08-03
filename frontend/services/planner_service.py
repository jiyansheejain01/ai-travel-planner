import httpx

BASE_URL = "http://localhost:8000"


async def plan_trip(prompt: str) -> dict:
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(
            f"{BASE_URL}/planner/",
            json={
                "message": prompt
            }
        )

    if response.status_code >= 400:
        # The backend's error handlers return {"message": "..."} —
        # surface that instead of a generic "500 Internal Server Error".
        try:
            detail = response.json().get("message", response.text)
        except ValueError:
            detail = response.text
        raise RuntimeError(f"Backend error ({response.status_code}): {detail}")

    return response.json()
