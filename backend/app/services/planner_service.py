from app.agents.base.agent_state import AgentState
from app.orchestrator.bootstrap import create_registry
from app.orchestrator.dispatcher import Dispatcher
from app.orchestrator.executor import Executor
from app.orchestrator.orchestrator import Orchestrator


class PlannerService:
    """
    Executes the AI travel planning workflow.
    """

    def __init__(self):
        registry = create_registry()

        self.dispatcher = Dispatcher(registry)
        self.executor = Executor(self.dispatcher)
        self.orchestrator = Orchestrator(self.executor)

    async def plan_trip(
        self,
        message: str,
    ) -> AgentState:

        state = AgentState(user_input=message)

        planner = self.dispatcher.registry.get("planner")

        planner_result = await planner.execute(state)

        if not planner_result.success:
            raise RuntimeError(planner_result.error or "Planner agent failed.")

        state.trip = planner_result.result

        state = await self.orchestrator.run(state)

        return state