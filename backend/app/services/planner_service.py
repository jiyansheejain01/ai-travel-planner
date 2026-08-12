import time

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
        user_id: str,
    ) -> tuple[AgentState, float]:
        """
        Runs the full planning workflow.

        Returns the final state plus total wall-clock time in seconds,
        so the dashboard's "AI Planner Summary" can show a real number
        instead of a guess.
        """

        started_at = time.perf_counter()

        # -------------------------------------------------
        # CREATE AGENT STATE WITH USER METADATA
        # -------------------------------------------------
        state = AgentState(
            user_input=message,
            metadata={
                "user_id": user_id,
            },
        )

        # -------------------------------------------------
        # RUN PLANNER AGENT
        # -------------------------------------------------
        planner = self.dispatcher.registry.get("planner")

        planner_result = await planner.execute(state)

        # Keep planner result for frontend visualization
        state.previous_results["planner"] = planner_result

        if not planner_result.success:
            raise RuntimeError(planner_result.error or "Planner agent failed.")

        state.trip = planner_result.result

        # -------------------------------------------------
        # DEBUG: VERIFY USER ID REACHES THE PLANNER
        # -------------------------------------------------
        with open("planner_test.txt", "a", encoding="utf-8") as f:
            f.write("\n" + "=" * 60 + "\n")
            f.write(f"INPUT: {state.user_input}\n")
            f.write(f"METADATA: {state.metadata}\n")
            f.write("=" * 60 + "\n")

        print("\n" + "=" * 80)
        print("TRIP INTENT")
        print(state.trip.model_dump())
        print("METADATA:", state.metadata)
        print("=" * 80 + "\n")

        # -------------------------------------------------
        # RUN SPECIALIST AGENTS
        # -------------------------------------------------
        state = await self.orchestrator.run(state)

        total_time = round(time.perf_counter() - started_at, 3)

        return state, total_time

