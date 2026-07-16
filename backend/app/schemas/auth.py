"""
Authentication schemas.
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegisterRequest(BaseModel):
    """
    Request body for user registration.
    """

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
        description="User password",
    )


class UserLoginRequest(BaseModel):
    """
    Request body for login.
    """

    email: EmailStr

    password: str


class TokenResponse(BaseModel):
    """
    JWT tokens returned after successful authentication.
    """

    access_token: str

    refresh_token: str

    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """
    Request body for refreshing an access token.
    """

    refresh_token: str


class TokenPayload(BaseModel):
    """
    Internal decoded JWT payload.
    """

    sub: str

    type: str

    iat: int
    
    exp: int


class MessageResponse(BaseModel):
    """
    Generic success response.
    """

    message: str

    model_config = ConfigDict(
        from_attributes=True,
    )