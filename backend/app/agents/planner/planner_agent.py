from app.agents.base.base_agent import BaseAgent
from app.agents.base.agent_state import AgentState
from app.agents.base.agent_result import AgentResult

from app.core.prompt_loader import PromptLoader

from app.agents.planner.schemas.trip_intent import TripIntent

from app.observability.tracer import tracer

# NEW
from app.agents.memory.memory_agent import MemoryAgent


class PlannerAgent(BaseAgent):

    name = "planner"
    prompt_name = "system.md"
    response_model = TripIntent

    def __init__(self, llm_provider=None):
        super().__init__(llm_provider=llm_provider)
        self.memory_agent = MemoryAgent()

    async def run(
        self,
        state: AgentState,
    ) -> AgentResult:

        with tracer.start_as_current_span("planner.reasoning") as span:

            # -------------------------------------------------
            # TRACE METADATA
            # -------------------------------------------------
            span.set_attribute("agent.name", self.name)
            span.set_attribute("planner.prompt", self.prompt_name)

            # -------------------------------------------------
            # LOAD SYSTEM PROMPT
            # -------------------------------------------------
            system_prompt = PromptLoader.load(
                agent_name=self.name,
                prompt_name=self.prompt_name,
            )

            # -------------------------------------------------
            # RETRIEVE USER MEMORY (RAG STEP)
            # -------------------------------------------------
            user_id = state.metadata.get("user_id")

            memory_context = ""

            if user_id:

                try:
                    memory_context = (
                        await self.memory_agent.get_relevant_context(
                            user_id=user_id,
                            current_request=state.user_input,
                        )
                    )

                    # Save retrieved memory into shared workflow state
                    state.memory["retrieved_context"] = memory_context

                    span.set_attribute(
                        "planner.memory_found",
                        bool(memory_context),
                    )

                    span.set_attribute(
                        "planner.memory_length",
                        len(memory_context),
                    )

                except Exception as exc:

                    # Memory failure should never break planning
                    state.memory["retrieved_context"] = ""

                    span.record_exception(exc)

                    span.set_attribute(
                        "planner.memory_error",
                        True,
                    )

            # -------------------------------------------------
            # BUILD PERSONALIZED USER PROMPT
            # -------------------------------------------------
            if memory_context:

                user_prompt = f"""
Current travel request:
{state.user_input}

Relevant long-term user preferences and travel history:
{memory_context}

Instructions:
- Use these preferences to personalize the trip.
- Prioritize hotels, attractions, food, and pacing that match the user's history.
- Do not explicitly mention that this information came from memory retrieval.
- If the memory conflicts with the current request, follow the current request.
"""

            else:

                user_prompt = state.user_input

            # -------------------------------------------------
            # CALL LLM
            # -------------------------------------------------
            response = await self.call_llm(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
            )

            span.set_attribute(
                "planner.response_received",
                True,
            )

            # -------------------------------------------------
            # STORE PLANNER OUTPUT IN SHARED STATE
            # -------------------------------------------------
            state.trip = response

            # -------------------------------------------------
            # RETURN RESULT
            # -------------------------------------------------
            return AgentResult(
                agent=self.name,
                success=True,
                result=response,
                confidence=0.95,
            )

