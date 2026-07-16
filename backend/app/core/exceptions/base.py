"""
Base application exception.
"""



class AppException(Exception):
    """
    Base exception for all application-specific exceptions.
    """

    status_code = 500

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)