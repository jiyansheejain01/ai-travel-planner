"""
Base repository.

Provides common CRUD operations.
"""

from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy.orm import Session

from app.data.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic repository providing common CRUD operations.
    """

    def __init__(
        self,
        db: Session,
        model: type[ModelType],
    ) -> None:
        self.db = db
        self.model = model

    def get_by_id(
        self,
        object_id: UUID,
    ) -> ModelType | None:
        """
        Retrieve an object by its primary key.
        """

        return self.db.get(
            self.model,
            object_id,
        )

    def create(
        self,
        obj: ModelType,
    ) -> ModelType:
        """
        Persist a new object.
        """

        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return obj

    def update(
        self,
        obj: ModelType,
    ) -> ModelType:
        """
        Persist changes to an existing object.
        """

        self.db.commit()
        self.db.refresh(obj)

        return obj

    def delete(
        self,
        obj: ModelType,
    ) -> None:
        """
        Delete an object.
        """

        self.db.delete(obj)
        self.db.commit()