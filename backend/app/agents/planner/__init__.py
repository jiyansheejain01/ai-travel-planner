from app.agents.base.base_agent import BaseAgent
from app.agents.base.agent_state import AgentState
from app.agents.base.agent_result import AgentResult
from app.core.prompt_loader import PromptLoader
from app.agents.planner.schemas.trip_intent import TripIntent
from app.observability.tracer import tracer
from app.agents.memory.memory_agent import MemoryAgent


class PlannerAgent(BaseAgent):

    name = "planner"
    prompt_name = "system.md"
    response_model = TripIntent

    def __init__(self, llm_provider=None):
        super().__init__(llm_provider=llm_provider)
        self.memory_agent = MemoryAgent()