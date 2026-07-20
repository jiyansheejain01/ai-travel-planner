"""
Activity routes.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.v1.routes.auth import get_current_user
from app.data.database.models.user import User
from app.data.database.session import get_db
from app.data.repositories.activity_repository import ActivityRepository
from app.schemas.activity import (
    ActivityCreate,
    ActivityResponse,
    ActivityUpdate,
)
from app.services.activity_service import ActivityService

router = APIRouter(
    prefix="/activities",
    tags=["Activities"],
)


@router.post(
    "/days/{itinerary_day_id}",
    response_model=ActivityResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_activity(
    itinerary_day_id: UUID,
    activity: ActivityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = ActivityRepository(db)
    service = ActivityService(repository)

    return service.create_activity(
        itinerary_day_id=itinerary_day_id,
        user_id=current_user.id,
        activity=activity,
    )


@router.get(
    "/days/{itinerary_day_id}",
    response_model=list[ActivityResponse],
)
def list_activities(
    itinerary_day_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = ActivityRepository(db)
    service = ActivityService(repository)

    return service.list_activities(
        itinerary_day_id=itinerary_day_id,
        user_id=current_user.id,
    )


@router.get(
    "/{activity_id}",
    response_model=ActivityResponse,
)
def get_activity(
    activity_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = ActivityRepository(db)
    service = ActivityService(repository)

    return service.get_activity(
        activity_id=activity_id,
        user_id=current_user.id,
    )


@router.patch(
    "/{activity_id}",
    response_model=ActivityResponse,
)
def update_activity(
    activity_id: UUID,
    activity: ActivityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = ActivityRepository(db)
    service = ActivityService(repository)

    return service.update_activity(
        activity_id=activity_id,
        user_id=current_user.id,
        activity_update=activity,
    )


@router.delete(
    "/{activity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_activity(
    activity_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = ActivityRepository(db)
    service = ActivityService(repository)

    service.delete_activity(
        activity_id=activity_id,
        user_id=current_user.id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )