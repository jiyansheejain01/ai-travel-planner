from pydantic import BaseModel, Field


class FlightOption(BaseModel):
    airline: str = Field(..., description="Airline operating the flight")
    flight_number: str = Field(..., description="Flight number")

    departure_airport: str
    arrival_airport: str

    departure_time: str
    arrival_time: str

    duration: str

    price: float
    currency: str


class FlightResult(BaseModel):
    origin: str
    destination: str
    departure_date: str

    flights: list[FlightOption]