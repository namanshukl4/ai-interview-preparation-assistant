from app.services.generation.mock_llm import MockLLM
from app.services.generation.question_generator import generate_question


def test_generate_question_returns_llm_response():
    llm = MockLLM(
        "How would you design a scalable FastAPI application?"
    )

    candidate_profile = {
        "skills": ["python", "fastapi"],
    }

    jd_profile = {
        "skills": ["python", "fastapi", "docker"],
        "responsibilities": ["Build REST APIs"],
    }

    result = generate_question(
        llm=llm,
        candidate_profile=candidate_profile,
        jd_profile=jd_profile,
        matched_skills=["python", "fastapi"],
        missing_skills=["docker"],
        interview_type="technical",
        difficulty="medium",
    )

    assert result == "How would you design a scalable FastAPI application?"


def test_generate_question_strips_whitespace():
    llm = MockLLM(
        "  Explain dependency injection in FastAPI.  "
    )

    result = generate_question(
        llm=llm,
        candidate_profile={"skills": ["python"]},
        jd_profile={"skills": ["python"]},
        matched_skills=["python"],
        missing_skills=[],
    )

    assert result == "Explain dependency injection in FastAPI."