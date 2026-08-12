import httpx

BASE_URL = "http://localhost:8000"


class AuthError(RuntimeError):
    """Raised when the backend rejects the request for lack of (or an
    expired/invalid) authentication -- callers should send the user back
    to /login rather than showing this as a generic planning failure."""


def _extract_message(response: httpx.Response) -> str:
    try:
        body = response.json()
    except ValueError:
        return response.text
    # AppException subclasses (see backend/app/core/exceptions) return
    # {"message": ...}; FastAPI's own HTTPBearer 403 ("no/blank auth
    # header") returns the default {"detail": ...} shape instead.
    return body.get("message") or body.get("detail") or response.text


async def plan_trip(prompt: str, access_token: str | None = None) -> dict:
    headers = {"Authorization": f"Bearer {access_token}"} if access_token else {}

    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(
            f"{BASE_URL}/planner/",
            json={
                "message": prompt
            },
            headers=headers,
        )

    if response.status_code in (401, 403):
        raise AuthError(_extract_message(response))

    if response.status_code >= 400:
        raise RuntimeError(f"Backend error ({response.status_code}): {_extract_message(response)}")

    return response.json()
