"""
Budget-related exceptions.
"""

from fastapi import status

from app.core.exceptions.base import AppException


class BudgetNotFoundException(AppException):
    """
    Raised when a budget cannot be found.
    """

    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self) -> None:
        super().__init__("Budget not found.")


class BudgetAlreadyExistsException(AppException):
    """
    Raised when a trip already has a budget.
    """

    status_code = status.HTTP_409_CONFLICT

    def __init__(self) -> None:
        super().__init__(
            "Budget already exists for this trip."
        )