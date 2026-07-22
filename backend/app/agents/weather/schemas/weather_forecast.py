from pydantic import BaseModel, Field


class WeatherForecast(BaseModel):
    """
    Structured weather information for a travel destination.
    """

    location: str = Field(
        description="Destination for the weather forecast."
    )

    summary: str = Field(
        description="Brief summary of the expected weather."
    )

    temperature_c: float = Field(
        description="Average temperature in Celsius."
    )

    condition: str = Field(
        description="Main weather condition such as Sunny, Rainy or Cloudy."
    )

    travel_advice: str = Field(
        description="Useful travel advice based on the forecast."
    )