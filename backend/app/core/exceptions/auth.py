"""
Authentication exceptions.
"""

from app.core.exceptions.base import AppException


class AuthenticationError(AppException):
    """
    Base authentication exception.
    """

    status_code = 401


class EmailAlreadyExistsError(AuthenticationError):
    """
    Raised when a user tries to register with an existing email.
    """

    status_code = 409

    def __init__(self) -> None:
        super().__init__("Email already registered.")


class InvalidCredentialsError(AuthenticationError):
    """
    Raised when login credentials are invalid.
    """

    status_code = 401

    def __init__(self) -> None:
        super().__init__("Invalid email or password.")