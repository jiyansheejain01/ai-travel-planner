"""
Expense routes.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_current_user,
    get_db,
)
from app.data.database.models.user import User
from app.data.repositories.expense_repository import (
    ExpenseRepository,
)
from app.data.repositories.trip_repository import (
    TripRepository,
)
from app.schemas.expense import (
    ExpenseCreate,
    ExpenseResponse,
    ExpenseUpdate,
)
from app.services.expense_service import ExpenseService

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"],
)


@router.post(
    "/trips/{trip_id}",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_expense(
    trip_id: UUID,
    request: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ExpenseResponse:
    """
    Create an expense for a trip.
    """

    expense_repository = ExpenseRepository(db)
    trip_repository = TripRepository(db)

    service = ExpenseService(
        expense_repository,
        trip_repository,
    )

    expense = service.create_expense(
        trip_id=trip_id,
        user_id=current_user.id,
        request=request,
    )

    return ExpenseResponse.model_validate(
        expense,
    )


@router.get(
    "/trips/{trip_id}",
    response_model=list[ExpenseResponse],
)
def get_expenses(
    trip_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ExpenseResponse]:
    """
    Retrieve all expenses for a trip.
    """

    expense_repository = ExpenseRepository(db)
    trip_repository = TripRepository(db)

    service = ExpenseService(
        expense_repository,
        trip_repository,
    )

    expenses = service.get_expenses(
        trip_id=trip_id,
        user_id=current_user.id,
    )

    return [
        ExpenseResponse.model_validate(expense)
        for expense in expenses
    ]


@router.get(
    "/{expense_id}",
    response_model=ExpenseResponse,
)
def get_expense(
    expense_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ExpenseResponse:
    """
    Retrieve an expense.
    """

    expense_repository = ExpenseRepository(db)
    trip_repository = TripRepository(db)

    service = ExpenseService(
        expense_repository,
        trip_repository,
    )

    expense = service.get_expense(
        expense_id=expense_id,
        user_id=current_user.id,
    )

    return ExpenseResponse.model_validate(
        expense,
    )


@router.put(
    "/{expense_id}",
    response_model=ExpenseResponse,
)
def update_expense(
    expense_id: UUID,
    request: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ExpenseResponse:
    """
    Update an existing expense.
    """

    expense_repository = ExpenseRepository(db)
    trip_repository = TripRepository(db)

    service = ExpenseService(
        expense_repository,
        trip_repository,
    )

    expense = service.update_expense(
        expense_id=expense_id,
        user_id=current_user.id,
        request=request,
    )

    return ExpenseResponse.model_validate(
        expense,
    )


@router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_expense(
    expense_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """
    Delete an expense.
    """

    expense_repository = ExpenseRepository(db)
    trip_repository = TripRepository(db)

    service = ExpenseService(
        expense_repository,
        trip_repository,
    )

    service.delete_expense(
        expense_id=expense_id,
        user_id=current_user.id,
    )