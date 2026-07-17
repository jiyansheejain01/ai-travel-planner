"""
Trip ORM model.
"""

from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import Date, Enum, ForeignKey, Numeric, String
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.data.database.models.base_model import BaseModel
from app.data.database.models.enums import TripStatus


class Trip(BaseModel):
    """
    Trip database model.
    """

    __tablename__ = "trips"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    primary_destination: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    end_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    budget: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=12,
            scale=2,
        ),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    status: Mapped[TripStatus] = mapped_column(
        Enum(
            TripStatus,
            name="trip_status",
        ),
        default=TripStatus.DRAFT,
        nullable=False,
    )

    planning_context: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )

    itinerary: Mapped["Itinerary"] = relationship(
        back_populates="trip",
        cascade="all, delete-orphan",
        uselist=False,
    )