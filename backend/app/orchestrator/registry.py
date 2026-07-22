from typing import Dict

from app.agents.base.base_agent import BaseAgent


class AgentRegistry:

    def __init__(self):

        self._agents: Dict[str, BaseAgent] = {}

    def register(
        self,
        agent: BaseAgent,
    ):

        self._agents[agent.name] = agent

    def get(
        self,
        name: str,
    ) -> BaseAgent:

        if name not in self._agents:
            raise ValueError(f"Unknown agent: {name}")

        return self._agents[name]

    def list_agents(self):

        return list(self._agents.keys())