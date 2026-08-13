import asyncio

from app.agents.planner.planner_agent import PlannerAgent
from app.agents.base.agent_state import AgentState

# IMPORT YOUR REAL PROVIDER
from app.providers.llm.groq_provider import GroqProvider


async def main():

    provider = GroqProvider()

    state = AgentState(
        user_input="Plan a 5-day Bali trip with beaches and temples",
        metadata={
            "user_id": "u1",
        },
    )

    # Inject the provider
    agent = PlannerAgent(llm_provider=provider)

    result = await agent.run(state)

    print("\n=== RETRIEVED MEMORY ===")
    print(state.memory.get("retrieved_context"))

    print("\n=== TRIP INTENT ===")
    print(result.result)


if __name__ == "__main__":
    asyncio.run(main())