"""
Itinerary ORM model.
"""

from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.data.database.models.base_model import BaseModel


class Itinerary(BaseModel):
    """
    Stores the itinerary for a trip.
    Each trip has exactly one itinerary.
    """

    __tablename__ = "itineraries"

    trip_id: Mapped[UUID] = mapped_column(
        ForeignKey("trips.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    generated_by_ai: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    version: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    last_generated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    trip: Mapped["Trip"] = relationship(
        back_populates="itinerary",
    )

    days: Mapped[list["ItineraryDay"]] = relationship(
        "ItineraryDay",
        back_populates="itinerary",
        cascade="all, delete-orphan",
        order_by="ItineraryDay.day_number",
    )