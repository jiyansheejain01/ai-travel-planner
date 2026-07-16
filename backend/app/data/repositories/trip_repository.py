"""
Trip repository.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.database.models.trip import Trip

from .base_repository import BaseRepository


class TripRepository(BaseRepository[Trip]):
    """
    Repository for Trip operations.
    """

    def __init__(self, db: Session) -> None:
        super().__init__(
            db=db,
            model=Trip,
        )

    def get_by_id(
        self,
        trip_id: UUID,
    ) -> Trip | None:
        """
        Retrieve a trip by ID.
        """

        stmt = (
            select(Trip)
            .where(Trip.id == trip_id)
        )

        return self.db.scalar(stmt)

    def get_by_user(
        self,
        user_id: UUID,
    ) -> list[Trip]:
        """
        Retrieve all trips for a user.
        """

        stmt = (
            select(Trip)
            .where(Trip.user_id == user_id)
            .order_by(Trip.created_at.desc())
        )

        return list(
            self.db.scalars(stmt).all()
        )