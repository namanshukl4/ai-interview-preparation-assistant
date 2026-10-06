from app.services.generation.llm_interface import LLMInterface


class MockLLM(LLMInterface):
    """Deterministic LLM implementation for testing."""

    def __init__(self, response: str = "Mock generated response"):
        self.response = response

    def generate(self, prompt: str) -> str:
        return self.response