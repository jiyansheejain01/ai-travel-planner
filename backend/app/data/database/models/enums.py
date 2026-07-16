"""
Database enums.
"""

from enum import Enum


class TripStatus(str, Enum):
    """
    Trip lifecycle status.
    """

    DRAFT = "draft"
    PLANNING = "planning"
    COMPLETED = "completed"
    ARCHIVED = "archived"