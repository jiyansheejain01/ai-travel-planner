"""
Budget routes.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_current_user,
    get_db,
)
from app.data.database.models.user import User
from app.data.repositories.budget_repository import (
    BudgetRepository,
)
from app.data.repositories.trip_repository import (
    TripRepository,
)
from app.schemas.budget import (
    BudgetCreate,
    BudgetUpdate,
    BudgetResponse,
)
from app.services.budget_service import BudgetService

router = APIRouter(
    prefix="/budgets",
    tags=["Budgets"],
)


@router.post(
    "/trips/{trip_id}",
    response_model=BudgetResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_budget(
    trip_id: UUID,
    request: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> BudgetResponse:
    """
    Create a budget for a trip.
    """

    budget_repository = BudgetRepository(db)
    trip_repository = TripRepository(db)

    service = BudgetService(
        budget_repository,
        trip_repository,
    )

    budget = service.create_budget(
        trip_id=trip_id,
        user_id=current_user.id,
        request=request,
    )

    return BudgetResponse.model_validate(
        budget,
    )


@router.get(
    "/trips/{trip_id}",
    response_model=BudgetResponse,
)
def get_budget(
    trip_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> BudgetResponse:
    """
    Retrieve a trip budget.
    """

    budget_repository = BudgetRepository(db)
    trip_repository = TripRepository(db)

    service = BudgetService(
        budget_repository,
        trip_repository,
    )

    budget = service.get_budget(
        trip_id=trip_id,
        user_id=current_user.id,
    )

    return BudgetResponse.model_validate(
        budget,
    )


@router.put(
    "/{budget_id}",
    response_model=BudgetResponse,
)
def update_budget(
    budget_id: UUID,
    request: BudgetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> BudgetResponse:
    """
    Update an existing budget.
    """

    budget_repository = BudgetRepository(db)
    trip_repository = TripRepository(db)

    service = BudgetService(
        budget_repository,
        trip_repository,
    )

    budget = service.update_budget(
        budget_id=budget_id,
        user_id=current_user.id,
        request=request,
    )

    return BudgetResponse.model_validate(
        budget,
    )


@router.delete(
    "/{budget_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_budget(
    budget_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """
    Delete a budget.
    """

    budget_repository = BudgetRepository(db)
    trip_repository = TripRepository(db)

    service = BudgetService(
        budget_repository,
        trip_repository,
    )

    service.delete_budget(
        budget_id=budget_id,
        user_id=current_user.id,
    )