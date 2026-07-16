"""
Authentication routes.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.data.repositories.user_repository import UserRepository
from app.schemas.user import UserResponse
from app.schemas.auth import (
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
)
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    request: UserRegisterRequest,
    db: Session = Depends(get_db),
) -> UserResponse:
    """
    Register a new user.
    """

    repository = UserRepository(db)
    service = AuthService(repository)

    user = service.register(request)

    return UserResponse.model_validate(user)

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: UserLoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """
    Authenticate a user.
    """

    repository = UserRepository(db)
    service = AuthService(repository)

    return service.login(request)