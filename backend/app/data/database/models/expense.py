"""
Expense ORM model.
"""

from decimal import Decimal
from enum import Enum
from uuid import UUID

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, Numeric, String, Text, Date
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.data.database.models.base_model import BaseModel


class ExpenseCategory(str, Enum):
    ACCOMMODATION = "accommodation"
    TRANSPORT = "transport"
    FOOD = "food"
    ACTIVITIES = "activities"
    SHOPPING = "shopping"
    MISC = "misc"


class Expense(BaseModel):
    """
    Stores an actual expense incurred during a trip.
    """

    __tablename__ = "expenses"

    trip_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(
            "trips.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
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

    category: Mapped[ExpenseCategory] = mapped_column(
        SqlEnum(
            ExpenseCategory,
            name="expense_category",
        ),
        nullable=False,
        index=True,
    )

    expense_date: Mapped[Date] = mapped_column(
        Date,
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    trip: Mapped["Trip"] = relationship(
        back_populates="expenses",
    )