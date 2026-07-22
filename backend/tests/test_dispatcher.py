import pytest

from app.agents.base.agent_state import AgentState

from app.orchestrator.bootstrap import create_registry

from app.orchestrator.dispatcher import Dispatcher


@pytest.mark.asyncio
async def test_dispatch():

    registry = create_registry()

    dispatcher = Dispatcher(registry)

    state = AgentState(
        user_input="Plan 5 days in Japan"
    )

    result = await dispatcher.dispatch(
        "planner",
        state,
    )

    assert result.success