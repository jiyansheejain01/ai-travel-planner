import asyncio
import hashlib
import time

import httpx

from app.core.config import settings


def get_headers():
    timestamp = str(int(time.time()))

    signature = hashlib.sha256(
        (
            settings.HOTELBEDS_API_KEY
            + settings.HOTELBEDS_API_SECRET
            + timestamp
        ).encode("utf-8")
    ).hexdigest()

    return {
        "Api-key": settings.HOTELBEDS_API_KEY,
        "X-Signature": signature,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


async def test_get(name: str, url: str, params=None):
    print("\n" + "=" * 70)
    print(f"TEST: {name}")
    print("=" * 70)
    print("URL:", url)
    print("PARAMS:", params)

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                url,
                headers=get_headers(),
                params=params,
            )

        print("STATUS:", response.status_code)

        if response.status_code == 200:
            print("SUCCESS")

            try:
                data = response.json()

                if "destinations" in data:
                    print(
                        "Destinations returned:",
                        len(data["destinations"]),
                    )

                elif "hotels" in data:
                    print(
                        "Hotels returned:",
                        len(data["hotels"]),
                    )

                else:
                    print("RESPONSE:", data)

            except Exception:
                print("RESPONSE:", response.text[:1000])

        else:
            print("FAILED")
            print("RESPONSE:")
            print(response.text[:2000])

    except Exception as e:
        print("EXCEPTION:", repr(e))


async def main():

    base_url = settings.HOTELBEDS_BASE_URL

    print("\nHBX DIAGNOSTIC TEST")
    print("=" * 70)

    # Don't print secrets.
    print(
        "API KEY PRESENT:",
        bool(settings.HOTELBEDS_API_KEY)
    )

    print(
        "API SECRET PRESENT:",
        bool(settings.HOTELBEDS_API_SECRET)
    )

    print("BASE URL:", base_url)

    # ---------------------------------------------------------
    # TEST 1: Booking API authentication
    # ---------------------------------------------------------

    await test_get(
        name="1. BOOKING API STATUS",
        url=f"{base_url}/hotel-api/1.0/status",
    )

    # ---------------------------------------------------------
    # TEST 2: Content API - first 100 destinations
    # ---------------------------------------------------------

    await test_get(
        name="2. CONTENT API - DESTINATIONS 1-100",
        url=(
            f"{base_url}"
            "/hotel-content-api/1.0/locations/destinations"
        ),
        params={
            "fields": "all",
            "language": "ENG",
            "from": 1,
            "to": 100,
        },
    )

    # ---------------------------------------------------------
    # TEST 3: Same endpoint using 1-1000
    # ---------------------------------------------------------

    await test_get(
        name="3. CONTENT API - DESTINATIONS 1-1000",
        url=(
            f"{base_url}"
            "/hotel-content-api/1.0/locations/destinations"
        ),
        params={
            "fields": "all",
            "language": "ENG",
            "from": 1,
            "to": 1000,
        },
    )

    # ---------------------------------------------------------
    # TEST 4: Hotel Content API
    # ---------------------------------------------------------

    await test_get(
        name="4. HOTEL CONTENT API",
        url=(
            f"{base_url}"
            "/hotel-content-api/1.0/hotels"
        ),
        params={
            "fields": "all",
            "language": "ENG",
            "from": 1,
            "to": 10,
        },
    )

    print("\n" + "=" * 70)
    print("DIAGNOSTIC FINISHED")
    print("=" * 70)


asyncio.run(main())