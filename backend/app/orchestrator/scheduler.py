from __future__ import annotations

from app.orchestrator.task_graph import TaskGraph


class Scheduler:
    """
    Determines which tasks are ready for execution.
    """

    def __init__(self, graph: TaskGraph):
        self.graph = graph

    def get_ready_tasks(
        self,
        completed: set[str],
    ) -> list[str]:
        """
        Return all tasks whose dependencies have been satisfied.
        """

        return self.graph.get_ready_tasks(completed)