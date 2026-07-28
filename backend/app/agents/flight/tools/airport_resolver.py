from __future__ import annotations

import json
from pathlib import Path


class AirportResolver:
    """
    Resolves city names to IATA airport codes
    using a local JSON dataset.
    """

    def __init__(self) -> None:
        data_file = (
            Path(__file__).parent.parent
            / "data"
            / "airports.json"
        )

        with open(data_file, "r", encoding="utf-8") as f:
            self.airports = json.load(f)

    def resolve(self, city: str | None) -> str | None:
        """
        Returns the IATA airport code for a city.
        """

        if not city:
            return None

        return self.airports.get(city.strip().lower())