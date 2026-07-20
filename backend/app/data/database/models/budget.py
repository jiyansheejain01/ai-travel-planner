"""
Budget ORM model.
"""

from decimal import Decimal
from uuid import UUID

from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.data.database.models.base_model import BaseModel
from app.data.database.models.trip import Trip


class Budget(BaseModel):
    """
    Stores the budget breakdown for a trip.
    """

    __tablename__ = "budgets"

    trip_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(
            "trips.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
        index=True,
    )

    total_budget: Mapped[Decimal] = mapped_column(
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

    accommodation_budget: Mapped[Decimal | None] = mapped_column(
        Numeric(
            precision=12,
            scale=2,
        ),
        nullable=True,
    )

    transport_budget: Mapped[Decimal | None] = mapped_column(
        Numeric(
            precision=12,
            scale=2,
        ),
        nullable=True,
    )

    food_budget: Mapped[Decimal | None] = mapped_column(
        Numeric(
            precision=12,
            scale=2,
        ),
        nullable=True,
    )

    activities_budget: Mapped[Decimal | None] = mapped_column(
        Numeric(
            precision=12,
            scale=2,
        ),
        nullable=True,
    )

    shopping_budget: Mapped[Decimal | None] = mapped_column(
        Numeric(
            precision=12,
            scale=2,
        ),
        nullable=True,
    )

    misc_budget: Mapped[Decimal | None] = mapped_column(
        Numeric(
            precision=12,
            scale=2,
        ),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    trip: Mapped["Trip"] = relationship(
        back_populates="budget_details",
    )