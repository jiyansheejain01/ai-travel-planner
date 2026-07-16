class TravelPlannerException(Exception):
    """Base exception for the application."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ResourceNotFoundException(TravelPlannerException):
    """Raised when a requested resource is not found."""


class ValidationException(TravelPlannerException):
    """Raised when validation fails."""


class UnauthorizedException(TravelPlannerException):
    """Raised when authentication fails."""