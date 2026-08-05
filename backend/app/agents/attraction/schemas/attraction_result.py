from pydantic import BaseModel, Field


class AttractionOption(BaseModel):
    name: str = Field(..., description="Attraction/place name")

    category: str = Field(
        ...,
        description="Human-readable category, e.g. Sights, Museum, Culture, Park.",
    )

    address: str | None = None

    latitude: float | None = None
    longitude: float | None = None

    rating: float | None = Field(
        default=None,
        description="Not populated by the current Geoapify integration -- reserved for a future data source.",
    )

    price: float | None = Field(
        default=None,
        description="Ticket/entry price, when available. Rarely populated by OpenStreetMap-sourced data.",
    )
    currency: str | None = None

    distance_meters: float | None = Field(
        default=None,
        description="Distance from the city center, as returned by the Places API's proximity bias.",
    )

    wikidata_id: str | None = Field(
        default=None,
        description=(
            "Wikidata QID, when OpenStreetMap has one tagged for this place. Used as a "
            "rough 'well-known landmark' signal -- see AttractionTool's hidden-gem heuristic."
        ),
    )


class AttractionResult(BaseModel):
    city: str

    attractions: list[AttractionOption]
