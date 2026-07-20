import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID

from sqlalchemy import (
    Enum as SqlEnum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    Time,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.data.database.models.base_model import BaseModel


class ActivityCategory(str, Enum):
    ATTRACTION = "attraction"
    RESTAURANT = "restaurant"
    HOTEL = "hotel"
    TRANSPORT = "transport"
    SHOPPING = "shopping"
    ENTERTAINMENT = "entertainment"
    OTHER = "other"


class Activity(BaseModel):
    """
    Stores a single activity belonging to an itinerary day.
    """

    __tablename__ = "activities"

    __table_args__ = (
        UniqueConstraint(
            "itinerary_day_id",
            "display_order",
            name="uq_activity_display_order",
        ),
    )

    itinerary_day_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(
            "itinerary_days.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    location_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    place_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    latitude: Mapped[Decimal | None] = mapped_column(
        Numeric(9, 6),
        nullable=True,
    )

    longitude: Mapped[Decimal | None] = mapped_column(
        Numeric(9, 6),
        nullable=True,
    )

    start_time: Mapped[datetime.time | None] = mapped_column(
        Time,
        nullable=True,
    )

    end_time: Mapped[datetime.time | None] = mapped_column(
        Time,
        nullable=True,
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    category: Mapped[ActivityCategory] = mapped_column(
        SqlEnum(
            ActivityCategory,
            name="activity_category",
        ),
        nullable=False,
        default=ActivityCategory.OTHER,
        index=True,
    )

    estimated_cost: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    currency: Mapped[str | None] = mapped_column(
        String(3),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    itinerary_day: Mapped["ItineraryDay"] = relationship(
        back_populates="activities",
    )