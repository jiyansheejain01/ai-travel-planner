import asyncio

from app.agents.planner.planner_agent import PlannerAgent


async def main():
    agent = PlannerAgent()

    response = await agent.generate(
        """
        Plan a 3-day trip to Jaipur.

        Budget: ₹20,000

        Interests:
        - History
        - Food
        - Shopping
        """
    )

    print(response.model_dump_json(indent=4))


if __name__ == "__main__":
    asyncio.run(main())