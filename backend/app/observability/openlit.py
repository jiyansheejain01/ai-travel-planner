"""
OpenLIT initialization for the AI Travel Planner.

All observability starts here.
"""

import openlit

from app.core.config import settings


def initialize_observability() -> None:
    """Initialize OpenLIT instrumentation."""

    openlit.init(
        application_name="ai-travel-planner",
        environment=settings.ENVIRONMENT,
    )