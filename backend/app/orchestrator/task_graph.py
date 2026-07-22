from __future__ import annotations

from pydantic import BaseModel, Field


class TaskNode(BaseModel):
    """
    Represents one task in the execution graph.
    """

    name: str

    depends_on: list[str] = Field(default_factory=list)


class TaskGraph(BaseModel):
    """
    Directed Acyclic Graph (DAG) of tasks.
    """

    nodes: dict[str, TaskNode] = Field(default_factory=dict)

    def add_task(
        self,
        task: str,
        depends_on: list[str] | None = None,
    ) -> None:

        self.nodes[task] = TaskNode(
            name=task,
            depends_on=depends_on or [],
        )

    def get_dependencies(
        self,
        task: str,
    ) -> list[str]:

        node = self.nodes.get(task)

        if not node:
            return []

        return node.depends_on

    def get_ready_tasks(
        self,
        completed: set[str],
    ) -> list[str]:
        """
        Return tasks whose dependencies are satisfied.
        """

        ready = []

        for node in self.nodes.values():

            if node.name in completed:
                continue

            if all(dep in completed for dep in node.depends_on):
                ready.append(node.name)

        return ready