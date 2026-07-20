"""
Activity-related exceptions.
"""

from fastapi import status

from app.core.exceptions.base import AppException


class ActivityNotFoundException(AppException):
    """
    Raised when an activity cannot be found.
    """

    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self) -> None:
        super().__init__("Activity not found.")