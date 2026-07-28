from pydantic import BaseModel, Field


class HotelOption(BaseModel):
    hotel_id: str = Field(..., description="Hotel identifier")

    name: str = Field(..., description="Hotel name")

    address: str
    city: str

    latitude: float | None = None
    longitude: float | None = None

    rating: float | None = None

    price: float | None = None
    currency: str | None = None


class HotelResult(BaseModel):
    city: str

    check_in: str | None = None
    check_out: str | None = None

    hotels: list[HotelOption]