"""
Itinerary Day ORM model.

Represents a single day within an itinerary.
Each itinerary consists of one or more itinerary days.
"""

from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.data.database.database import Base


class ItineraryDay(Base):
    __tablename__ = "itinerary_days"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    itinerary_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("itineraries.id", ondelete="CASCADE"),
        nullable=False,
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

    itinerary = relationship(
        "Itinerary",
        back_populates="days",
    )