"""
Itinerary Day ORM model.

Represents a single day within an itinerary.
Each itinerary consists of one or more itinerary days.
"""

from datetime import date
from uuid import UUID

from sqlalchemy import Date, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.data.database.models.base_model import BaseModel


class ItineraryDay(BaseModel):
    """
    Stores a single day belonging to an itinerary.
    """

    __tablename__ = "itinerary_days"

    __table_args__ = (
        UniqueConstraint(
            "itinerary_id",
            "day_number",
            name="uq_itinerary_day_number",
        ),
    )

    itinerary_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(
            "itineraries.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    day_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    summary: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    itinerary: Mapped["Itinerary"] = relationship(
        back_populates="days",
    )

    activities: Mapped[list["Activity"]] = relationship(
        "Activity",
        back_populates="itinerary_day",
        cascade="all, delete-orphan",
    )