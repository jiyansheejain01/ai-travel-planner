"""
Expense-related exceptions.
"""

from fastapi import status

from app.core.exceptions.base import AppException


class ExpenseNotFoundException(AppException):
    """
    Raised when an expense cannot be found.
    """

    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self) -> None:
        super().__init__("Expense not found.")