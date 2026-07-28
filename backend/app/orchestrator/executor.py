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

    async def execute_task(
        self,
        agent_name: str,
        state: AgentState,
    ) -> None:
        """
        Execute a single agent.
        """

        result = await self.dispatcher.dispatch(
            agent_name=agent_name,
            state=state,
        )

        state.previous_results[agent_name] = result

    async def execute_tasks(
        self,
        tasks: list[str],
        state: AgentState,
    ) -> None:
        """
        Execute all ready tasks concurrently.
        """

        coroutines = [
            self.execute_task(
                agent_name=task,
                state=state,
            )
            for task in tasks
        ]

        await asyncio.gather(*coroutines)