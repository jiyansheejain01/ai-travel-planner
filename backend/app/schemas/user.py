"""
User schemas.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponse(BaseModel):
    """
    Public user information.
    """

    id: UUID

    email: EmailStr

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserPublic(UserResponse):
    """
    Public user schema.

    Reserved for future extension.
    """

    pass