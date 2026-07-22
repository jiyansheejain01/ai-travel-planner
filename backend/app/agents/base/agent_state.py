from typing import Any

from pydantic import BaseModel, Field

from app.agents.base.agent_result import AgentResult
from app.agents.planner.schemas.trip_intent import TripIntent
from app.orchestrator.execution_plan import ExecutionPlan


class AgentState(BaseModel):
    """
    Shared state passed through the entire agent workflow.
    """

    # Original user request
    user_input: str

    # Structured planner output
    trip: TripIntent | None = None

    # Workflow execution plan
    execution_plan: ExecutionPlan | None = None

    # Shared context
    context: dict[str, Any] = Field(default_factory=dict)

    # Results from previously executed agents
    previous_results: dict[str, AgentResult] = Field(default_factory=dict)

    # Long-term memory / conversation memory
    memory: dict[str, Any] = Field(default_factory=dict)

    # Extra metadata
    metadata: dict[str, Any] = Field(default_factory=dict)