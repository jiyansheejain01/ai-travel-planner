from __future__ import annotations

import asyncio

from app.agents.base.agent_state import AgentState
from app.orchestrator.dispatcher import Dispatcher


class Executor:
    """
    Executes agent tasks.
    """

    def __init__(
        self,
        dispatcher: Dispatcher,
    ):
        self.dispatcher = dispatcher

    async def execute_tasks(
        self,
        tasks: list[str],
        state: AgentState,
    ) -> None:

        coroutines = [
            self.execute_task(
                task,
                state,
            )
            for task in tasks
        ]

        await asyncio.gather(*coroutines)

    async def execute_task(
        self,
        task: str,
        state: AgentState,
    ) -> None:

        result = await self.dispatcher.dispatch(
            agent_name=task,
            state=state,
        )

        state.previous_results[result.agent] = result