import pytest

from app.services.generation.llm_interface import LLMInterface
from app.services.generation.mock_llm import MockLLM


def test_mock_llm_returns_configured_response():
    llm = MockLLM("Generated interview question")

    response = llm.generate("Generate a question")

    assert response == "Generated interview question"


def test_mock_llm_uses_default_response():
    llm = MockLLM()

    response = llm.generate("Generate a question")

    assert response == "Mock generated response"


def test_llm_interface_is_abstract():
    with pytest.raises(TypeError):
        LLMInterface()