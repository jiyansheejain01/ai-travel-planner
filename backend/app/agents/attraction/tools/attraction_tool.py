from __future__ import annotations

from app.agents.attraction.schemas.attraction_result import (
    AttractionOption,
    AttractionResult,
)
from app.agents.attraction.tools.attraction_client import AttractionClient

_CATEGORY_LABELS: dict[str, str] = {
    "tourism.sights": "Sights",
    "entertainment.museum": "Museum",
    "entertainment.culture": "Culture",
    "leisure.park": "Park",
}


def _label_for_categories(categories: list[str]) -> str:

    for category in categories:
        for known_prefix, label in _CATEGORY_LABELS.items():
            if category == known_prefix or category.startswith(known_prefix + "."):
                return label

    return "Attraction"


class AttractionTool:

    def __init__(
        self,
        client: AttractionClient | None = None,
    ) -> None:

        self.client = client or AttractionClient()

    async def get_attractions(
        self,
        city: str,
    ) -> AttractionResult:

        data = await self.client.search_attractions(city)

        features = data.get("features") or []

        attractions: list[AttractionOption] = []
        seen_names: set[str] = set()

        for feature in features:

            properties = feature.get("properties") or {}
            geometry = feature.get("geometry") or {}

            name = properties.get("name")

            if not name:
                # Unnamed OSM nodes aren't useful to show a traveler.
                continue

            if name in seen_names:
                # OSM sometimes has multiple nodes for the same place.
                continue

            seen_names.add(name)

            coordinates = geometry.get("coordinates") or [None, None]

            datasource_raw = (properties.get("datasource") or {}).get("raw") or {}

            attractions.append(
                AttractionOption(
                    name=name,
                    category=_label_for_categories(properties.get("categories") or []),
                    address=properties.get("formatted"),
                    latitude=coordinates[1] if len(coordinates) > 1 else None,
                    longitude=coordinates[0] if len(coordinates) > 0 else None,
                    rating=None,
                    price=None,
                    currency=None,
                    distance_meters=properties.get("distance"),
                    wikidata_id=datasource_raw.get("wikidata"),
                )
            )

        return AttractionResult(
            city=city,
            attractions=attractions,
        )
