from __future__ import annotations

from pydantic import BaseModel, Field


class ExecutionPlan(BaseModel):
    """
    Defines which agents should execute for the current request.
    """

    tasks: list[str] = Field(default_factory=list)

    def add_task(self, task: str) -> None:
        """Add a task if it doesn't already exist."""

        if task not in self.tasks:
            self.tasks.append(task)

    def remove_task(self, task: str) -> None:
        """Remove a task."""

        if task in self.tasks:
            self.tasks.remove(task)

    def has_task(self, task: str) -> bool:
        """Check whether a task exists."""

        return task in self.tasks