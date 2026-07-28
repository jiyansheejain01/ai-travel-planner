import requests

BASE_URL = "http://localhost:8000"


def plan_trip(prompt: str):
    response = requests.post(
        f"{BASE_URL}/planner",
        json={
            "prompt": prompt
        },
        timeout=120,
    )

    response.raise_for_status()

    return response.json()