from app.agents.base.agent_state import AgentState
from app.orchestrator.registry import AgentRegistry
from app.observability.tracer import tracer


class Dispatcher:

    def __init__(
        self,
        registry: AgentRegistry,
    ):

        self.registry = registry

    async def dispatch(
        self,
        agent_name: str,
        state: AgentState,
    ):

        with tracer.start_as_current_span("dispatcher.dispatch") as span:

            span.set_attribute("agent.name", agent_name)

            agent = self.registry.get(agent_name)

            result = await agent.execute(state)

            span.set_attribute("agent.success", result.success)

            return result