from collections.abc import Generator

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.exceptions.auth import InvalidTokenError
from app.core.security import decode_token
from app.data.database import SessionLocal
from app.data.database.models.user import User
from app.data.repositories.user_repository import UserRepository

security = HTTPBearer()


def get_db() -> Generator[Session, None, None]:
    """
    Database dependency.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    Return the currently authenticated user.
    """

    token = credentials.credentials

    try:
        payload = decode_token(token)
    except JWTError as exc:
        raise InvalidTokenError() from exc

    if payload.get("type") != "access":
        raise InvalidTokenError()

    user = UserRepository(db).get_by_id(payload["sub"])

    if user is None:
        raise InvalidTokenError()

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Return the current active user.
    """

    if not current_user.is_active:
        raise InvalidTokenError()

    return current_user


def get_current_admin(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Return the current administrator.
    """

    if not current_user.is_admin:
        raise InvalidTokenError()

    return current_user