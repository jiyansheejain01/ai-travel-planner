"""
Itinerary Day-related exceptions.
"""

from fastapi import status

from app.core.exceptions.base import AppException


class ItineraryDayNotFoundException(AppException):
    """
    Raised when an itinerary day cannot be found.
    """

    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self) -> None:
        super().__init__("Itinerary day not found.")