from __future__ import annotations

from app.agents.base.agent_state import AgentState
from app.orchestrator.execution_plan import ExecutionPlan
from app.orchestrator.executor import Executor
from app.orchestrator.scheduler import Scheduler
from app.orchestrator.task_graph import TaskGraph


class Orchestrator:
    """
    Coordinates the execution of all agents.
    """

    def __init__(
        self,
        executor: Executor,
    ):
        self.executor = executor

    async def run(
        self,
        state: AgentState,
    ) -> AgentState:

        #
        # Build execution plan
        #
        state.execution_plan = self.build_execution_plan(state)

        #
        # Build dependency graph
        #
        graph = self.build_task_graph(state.execution_plan)

        scheduler = Scheduler(graph)

        completed: set[str] = set()

        while True:

            ready_tasks = scheduler.get_ready_tasks(completed)

            if not ready_tasks:
                break

            await self.executor.execute_tasks(
                ready_tasks,
                state,
            )

            completed.update(ready_tasks)

        return state

    def build_execution_plan(
        self,
        state: AgentState,
    ) -> ExecutionPlan:

        plan = ExecutionPlan()

        trip = state.trip

        if trip is None:
            return plan

        #
        # Only WeatherAgent exists right now
        #
        if trip.destination:
            plan.add_task("weather")

        return plan
    
    def build_task_graph(
        self,
        plan: ExecutionPlan,
    ) -> TaskGraph:
        """
        Convert the execution plan into a dependency graph.
        """

        graph = TaskGraph()

        #
        # Independent tasks
        #
        for task in [
            "weather",
            "flight",
            "hotel",
            "budget",
            "events",
        ]:
            if task in plan.tasks:
                graph.add_task(task)

        #
        # Itinerary depends on everything else
        #
        if "itinerary" in plan.tasks:

            dependencies = [
                task
                for task in plan.tasks
                if task != "itinerary"
            ]

            graph.add_task(
                "itinerary",
                depends_on=dependencies,
            )

        return graph