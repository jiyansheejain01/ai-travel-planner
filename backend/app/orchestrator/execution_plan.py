from __future__ import annotations

from pydantic import BaseModel, Field


class ExecutionTask(BaseModel):
    """
    Represents one task that the orchestrator should execute.
    """

    agent: str
    priority: int = 0
    depends_on: list[str] = Field(default_factory=list)
    required: bool = True


class ExecutionPlan(BaseModel):
    """
    Defines which agents should execute for the current request.
    """

    tasks: list[ExecutionTask] = Field(default_factory=list)

    def add_task(
        self,
        agent: str,
        priority: int = 0,
        depends_on: list[str] | None = None,
        required: bool = True,
    ) -> None:

        if any(task.agent == agent for task in self.tasks):
            return

        self.tasks.append(
            ExecutionTask(
                agent=agent,
                priority=priority,
                depends_on=depends_on or [],
                required=required,
            )
        )

    def remove_task(self, agent: str) -> None:

        self.tasks = [
            task
            for task in self.tasks
            if task.agent != agent
        ]

    def has_task(self, agent: str) -> bool:

        return any(task.agent == agent for task in self.tasks)