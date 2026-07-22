from pathlib import Path


class PromptLoader:

    BASE_PATH = Path(__file__).parent.parent / "agents"

    @classmethod
    def load(
        cls,
        agent_name: str,
        prompt_name: str,
    ) -> str:

        path = (
            cls.BASE_PATH
            / agent_name
            / "prompts"
            / prompt_name
        )

        return path.read_text(encoding="utf-8")