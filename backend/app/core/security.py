"""
Security utilities.

Responsibilities:
- Password hashing
- Password verification
- JWT creation
- JWT validation
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings


# Configure password hashing algorithm
_pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """
    Hash a plain-text password.

    Args:
        password: User's plain-text password.

    Returns:
        Secure bcrypt hash.
    """
    return _pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a password against its stored hash.

    Args:
        plain_password: Password entered by the user.
        hashed_password: Password stored in the database.

    Returns:
        True if the password matches, otherwise False.
    """
    return _pwd_context.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(subject: str) -> str:
    """
    Create a JWT access token.

    Args:
        subject: Usually the user's UUID.

    Returns:
        Encoded JWT access token.
    """

    issued_at = datetime.now(timezone.utc)

    expire = issued_at + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": subject,
        "type": "access",
        "iat": issued_at,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def create_refresh_token(subject: str) -> str:
    """
    Create a JWT refresh token.

    Args:
        subject: Usually the user's UUID.

    Returns:
        Encoded JWT refresh token.
    """

    issued_at = datetime.now(timezone.utc)

    expire = issued_at + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    payload = {
        "sub": subject,
        "type": "refresh",
        "iat": issued_at,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_token(token: str) -> dict[str, Any]:
    """
    Decode and validate a JWT.

    Args:
        token: JWT access or refresh token.

    Returns:
        Decoded payload.

    Raises:
        JWTError: If the token is invalid or expired.
    """

    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )