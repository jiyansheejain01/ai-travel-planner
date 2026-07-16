"""
User service.

Contains user business logic.
"""

from uuid import UUID

from app.data.database.models.user import User
from app.data.repositories.user_repository import UserRepository


class UserService:
    """
    User business logic.
    """

    def __init__(
        self,
        repository: UserRepository,
    ) -> None:
        self.repository = repository

    def get_by_id(
        self,
        user_id: UUID,
    ) -> User | None:
        """
        Retrieve a user by ID.
        """

        return self.repository.get_by_id(user_id)

    def get_by_email(
        self,
        email: str,
    ) -> User | None:
        """
        Retrieve a user by email.
        """

        return self.repository.get_by_email(email)