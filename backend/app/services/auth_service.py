"""
Authentication service.

Contains authentication business logic.
"""

from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.core.exceptions.auth import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
)
from app.data.database.models.user import User
from app.data.repositories.user_repository import UserRepository
from app.schemas.auth import (
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
)


class AuthService:
    """
    Authentication business logic.
    """

    def __init__(
        self,
        repository: UserRepository,
    ) -> None:
        self.repository = repository

    def register(
        self,
        request: UserRegisterRequest,
    ) -> User:
        """
        Register a new user.
        """

        if self.repository.email_exists(request.email):
            raise EmailAlreadyExistsError()

        user = User(
            email=request.email,
            hashed_password=hash_password(
                request.password
            ),
        )

        return self.repository.create(user)

    def login(
        self,
        request: UserLoginRequest,
    ) -> TokenResponse:
        """
        Authenticate a user.
        """

        user = self.repository.get_by_email(
            request.email
        )

        if user is None:
            raise InvalidCredentialsError()

        if not verify_password(
            request.password,
            user.hashed_password,
        ):
            raise InvalidCredentialsError()

        return TokenResponse(
            access_token=create_access_token(
                str(user.id)
            ),
            refresh_token=create_refresh_token(
                str(user.id)
            ),
        )