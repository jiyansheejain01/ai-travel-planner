"""
Trip-related exceptions.
"""

from fastapi import status

from app.core.exceptions.base import AppException


class TripNotFoundException(AppException):
    """
    Raised when a trip cannot be found.
    """

    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self) -> None:
        super().__init__("Trip not found.")