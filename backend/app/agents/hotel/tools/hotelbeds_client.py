from __future__ import annotations

import hashlib
import json
import math
import time
from pathlib import Path

import httpx

from app.core.config import settings
from app.agents.hotel.tools.hotel_client import HotelClient


class HotelbedsClient:
    """
    Client for HBX / Hotelbeds APIs.

    Handles:
    - Authentication
    - Connection testing
    - Destination retrieval
    - Destination lookup by city
    - Hotel content retrieval
    - Hotel lookup by destination
    - Hotel availability and pricing
    """

    HOTEL_CATALOGUE_PATH = (
        Path(__file__).resolve().parents[3]
        / "data"
        / "hotelbeds"
        / "hotels.json"
    )

    # ============================================================
    # Authentication
    # ============================================================

    def _headers(self) -> dict[str, str]:
        """
        Generate HBX authentication headers.
        """

        timestamp = str(int(time.time()))

        signature_string = (
            settings.HOTELBEDS_API_KEY
            + settings.HOTELBEDS_API_SECRET
            + timestamp
        )

        signature = hashlib.sha256(
            signature_string.encode("utf-8")
        ).hexdigest()

        return {
            "Api-key": settings.HOTELBEDS_API_KEY,
            "X-Signature": signature,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    # ============================================================
    # Connection Test
    # ============================================================

    async def test_connection(self) -> dict:
        """
        Test whether HBX authentication is working.
        """

        url = (
            f"{settings.HOTELBEDS_BASE_URL}"
            "/hotel-api/1.0/status"
        )

        async with httpx.AsyncClient(timeout=30) as client:

            response = await client.get(
                url,
                headers=self._headers(),
            )

            response.raise_for_status()

            return response.json()

    # ============================================================
    # Destinations
    # ============================================================

    async def get_destinations(
        self,
        start: int = 1,
        end: int = 1000,
    ) -> dict:
        """
        Retrieve one page of HBX hotel destinations.
        """

        url = (
            f"{settings.HOTELBEDS_BASE_URL}"
            "/hotel-content-api/1.0/locations/destinations"
        )

        params = {
            "fields": "all",
            "language": "ENG",
            "from": start,
            "to": end,
        }

        async with httpx.AsyncClient(timeout=30) as client:

            response = await client.get(
                url,
                headers=self._headers(),
                params=params,
            )

            response.raise_for_status()

            return response.json()

    async def find_destination(
        self,
        city: str,
    ) -> dict | None:
        """
        Find an HBX destination by city name.

        Searches the destination catalogue in smaller pages to avoid
        requesting excessively large ranges.
        """

        city_normalized = city.strip().lower()

        start = 1
        batch_size = 100

        while True:

            end = start + batch_size - 1

            result = await self.get_destinations(
                start=start,
                end=end,
            )

            destinations = result.get("destinations", [])

            if not destinations:
                break

            for destination in destinations:

                name = (
                    destination
                    .get("name", {})
                    .get("content", "")
                    .strip()
                    .lower()
                )

                if name == city_normalized:
                    return destination

            if len(destinations) < batch_size:
                break

            start += batch_size

        return None

    # ============================================================
    # Hotel Content
    # ============================================================

    async def get_hotels(
        self,
        start: int = 1,
        end: int = 1000,
        destination_code: str | None = None,
    ) -> dict:
        """
        Retrieve HBX hotel content.

        Can optionally filter hotels using an HBX destination code.
        """

        url = (
            f"{settings.HOTELBEDS_BASE_URL}"
            "/hotel-content-api/1.0/hotels"
        )

        params = {
            "fields": "all",
            "language": "ENG",
            "from": start,
            "to": end,
        }

        if destination_code:
            params["destinationCode"] = destination_code

        async with httpx.AsyncClient(timeout=30) as client:

            response = await client.get(
                url,
                headers=self._headers(),
                params=params,
            )

            response.raise_for_status()

            return response.json()

    async def get_hotels_by_destination(
        self,
        destination_code: str,
        limit: int = 50,
    ) -> list[dict]:
        """
        Get hotels belonging to an HBX destination.

        Returns hotel content records, not availability.
        """

        result = await self.get_hotels(
            start=1,
            end=limit,
            destination_code=destination_code,
        )

        return result.get("hotels", [])

    # ============================================================
    # City -> Hotels
    # ============================================================

    def _load_hotel_catalogue(self) -> list[dict]:
        """
        Load the locally cached HBX hotel catalogue.
        """

        if not self.HOTEL_CATALOGUE_PATH.exists():
            raise RuntimeError(
                "Hotelbeds local hotel catalogue does not exist."
            )

        try:
            with self.HOTEL_CATALOGUE_PATH.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

        except (json.JSONDecodeError, OSError) as exc:
            raise RuntimeError(
                "Could not read Hotelbeds local hotel catalogue."
            ) from exc

        if not isinstance(data, list):
            raise RuntimeError(
                "Invalid Hotelbeds hotel catalogue format."
            )

        if not data:
            raise RuntimeError(
                "Hotelbeds local hotel catalogue is empty."
            )

        return data


    @staticmethod
    def _distance_km(
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
    ) -> float:
        """
        Calculate distance between two coordinates
        using the Haversine formula.
        """

        earth_radius = 6371.0

        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        delta_lat = lat2 - lat1
        delta_lon = lon2 - lon1

        a = (
            math.sin(delta_lat / 2) ** 2
            + math.cos(lat1)
            * math.cos(lat2)
            * math.sin(delta_lon / 2) ** 2
        )

        c = 2 * math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a),
        )

        return earth_radius * c


    async def find_hotels_by_city(
        self,
        city: str,
        limit: int = 50,
        radius_km: float = 30.0,
    ) -> list[dict]:
        """
        Find nearby HBX hotels without using
        the Hotelbeds Destinations API.

        Flow:

        city
        -> Geoapify coordinates
        -> local HBX catalogue
        -> nearby HBX hotels
        """

        geo_client = HotelClient()

        city_lat, city_lon = await geo_client.get_coordinates(
            city
        )

        catalogue = self._load_hotel_catalogue()

        nearby_hotels = []

        for hotel in catalogue:

            coordinates = hotel.get("coordinates") or {}

            latitude = coordinates.get("latitude")
            longitude = coordinates.get("longitude")

            if latitude is None or longitude is None:
                continue

            try:
                latitude = float(latitude)
                longitude = float(longitude)

            except (TypeError, ValueError):
                continue

            distance = self._distance_km(
                city_lat,
                city_lon,
                latitude,
                longitude,
            )

            if distance <= radius_km:
                nearby_hotels.append(
                    (distance, hotel)
                )

        nearby_hotels.sort(
            key=lambda item: item[0]
        )

        return [
            hotel
            for _, hotel in nearby_hotels[:limit]
        ]

    # ============================================================
    # Availability / Prices
    # ============================================================

    async def check_availability(
        self,
        hotel_codes: list[int],
        check_in: str,
        check_out: str,
        adults: int = 2,
        rooms: int = 1,
        children: int = 0,
    ) -> dict:
        """
        Search availability and prices for HBX hotel codes.

        check_in / check_out format:

            YYYY-MM-DD
        """

        if not hotel_codes:
            return {
                "hotels": {
                    "hotels": []
                }
            }

        url = (
            f"{settings.HOTELBEDS_BASE_URL}"
            "/hotel-api/1.0/hotels"
        )

        payload = {
            "stay": {
                "checkIn": check_in,
                "checkOut": check_out,
            },
            "occupancies": [
                {
                    "rooms": rooms,
                    "adults": adults,
                    "children": children,
                }
            ],
            "hotels": {
                "hotel": hotel_codes,
            },
        }

        async with httpx.AsyncClient(timeout=30) as client:

            response = await client.post(
                url,
                headers=self._headers(),
                json=payload,
            )

            response.raise_for_status()

            return response.json()

    # ============================================================
    # Complete Search
    # ============================================================

    async def search_hotels(
        self,
        city: str,
        check_in: str,
        check_out: str,
        adults: int = 2,
        rooms: int = 1,
        children: int = 0,
        limit: int = 20,
    ) -> dict:
        """
        Complete hotel search.

        Flow:

        City
        -> Geoapify coordinates
        -> local HBX hotel catalogue
        -> nearby HBX hotel codes
        -> Hotelbeds Booking API
        -> live availability and prices
        """

        # --------------------------------------------------------
        # 1. Find nearby hotels from LOCAL catalogue
        # --------------------------------------------------------

        candidate_limit = max(limit * 3, 50)

        hotel_content = await self.find_hotels_by_city(
            city=city,
            limit=candidate_limit,
        )

        if not hotel_content:
            return {
                "content": [],
                "availability": {
                    "hotels": {
                        "hotels": []
                    }
                },
            }

        # --------------------------------------------------------
        # 2. Extract HBX hotel codes
        # --------------------------------------------------------

        hotel_codes: list[int] = []

        for hotel in hotel_content:

            code = hotel.get("code")

            if code is None:
                continue

            try:
                hotel_codes.append(int(code))

            except (TypeError, ValueError):
                continue

        if not hotel_codes:
            return {
                "content": hotel_content,
                "availability": {
                    "hotels": {
                        "hotels": []
                    }
                },
            }

        # --------------------------------------------------------
        # 3. Hotelbeds Booking API
        #    REAL availability + REAL prices
        # --------------------------------------------------------

        availability = await self.check_availability(
            hotel_codes=hotel_codes,
            check_in=check_in,
            check_out=check_out,
            adults=adults,
            rooms=rooms,
            children=children,
        )

        # --------------------------------------------------------
        # 4. Return static content + live availability
        # --------------------------------------------------------

        return {
            "content": hotel_content,
            "availability": availability,
        }