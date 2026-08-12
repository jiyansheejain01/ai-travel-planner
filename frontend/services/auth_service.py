import httpx

BASE_URL = "http://localhost:8000"


def _raise_for_error(response: httpx.Response) -> None:
    if response.status_code >= 400:
        # The backend's error handlers return {"message": "..."} for
        # AppException subclasses (e.g. EmailAlreadyExistsError,
        # InvalidCredentialsError) -- fall back to FastAPI's default
        # {"detail": ...} shape just in case, then raw text.
        try:
            body = response.json()
            detail = body.get("message") or body.get("detail") or response.text
        except ValueError:
            detail = response.text
        raise RuntimeError(detail)


async def register(email: str, password: str) -> dict:
    """
    Calls POST /auth/register. Returns the created user
    (id, email, created_at, updated_at) — no tokens yet, matching the
    backend contract (register() only creates the account).
    """
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            f"{BASE_URL}/auth/register",
            json={"email": email, "password": password},
        )

    _raise_for_error(response)
    return response.json()


async def login(email: str, password: str) -> dict:
    """
    Calls POST /auth/login. Returns {"access_token", "refresh_token", "token_type"}.
    """
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            f"{BASE_URL}/auth/login",
            json={"email": email, "password": password},
        )

    _raise_for_error(response)
    return response.json()


async def get_me(access_token: str) -> dict:
    """
    Calls GET /auth/me with the given bearer token. Returns the current
    user (id, email, created_at, updated_at).
    """
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(
            f"{BASE_URL}/auth/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    _raise_for_error(response)
    return response.json()
