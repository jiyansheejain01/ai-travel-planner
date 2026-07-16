"""
User repository.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.database.models.user import User

from .base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository for User operations.
    """

    def __init__(self, db: Session) -> None:
        super().__init__(
            db=db,
            model=User,
        )

    def get_by_email(
        self,
        email: str,
    ) -> User | None:
        """
        Retrieve a user by email.
        """

        stmt = (
            select(User)
            .where(User.email == email)
        )

        return self.db.scalar(stmt)

    def email_exists(
        self,
        email: str,
    ) -> bool:
        """
        Check whether an email already exists.
        """

        return self.get_by_email(email) is not None