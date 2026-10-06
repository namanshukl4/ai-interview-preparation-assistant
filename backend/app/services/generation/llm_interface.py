from abc import ABC, abstractmethod


class LLMInterface(ABC):
    """Provider-independent interface for generative AI models."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a response from a prompt.

        Implementations can connect to Gemini, OpenAI,
        or another language model provider.
        """
        raise NotImplementedError