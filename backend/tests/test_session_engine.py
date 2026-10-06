from app.services.interview.session_engine import InterviewSessionEngine


def mock_question_generator(
    candidate_profile,
    job_profile,
    interview_type,
    difficulty,
):
    return "Explain how you would design a REST API."


def mock_answer_evaluator(answer, reference_answer):
    return {
        "semantic_score": 80.0,
        "coverage_score": 75.0,
        "final_score": 78.0,
        "covered_concepts": ["api", "http"],
        "missing_concepts": ["authentication"],
    }


def mock_adaptive_engine(evaluation, question_number, max_questions):
    return {
        "action": "follow_up",
        "reason": "Answer contains a knowledge gap.",
        "focus_concepts": ["authentication"],
    }


def test_start_session():
    engine = InterviewSessionEngine(
        question_generator=mock_question_generator,
        answer_evaluator=mock_answer_evaluator,
        adaptive_engine=mock_adaptive_engine,
    )

    session = engine.start_session(
        candidate_profile={"skills": ["python", "fastapi"]},
        job_profile={"skills": ["python", "fastapi"]},
    )

    assert session["status"] == "active"
    assert session["question_number"] == 1
    assert session["question"] == "Explain how you would design a REST API."
    assert session["history"] == []


def test_process_answer():
    engine = InterviewSessionEngine(
        question_generator=mock_question_generator,
        answer_evaluator=mock_answer_evaluator,
        adaptive_engine=mock_adaptive_engine,
    )

    session = engine.start_session(
        candidate_profile={"skills": ["python"]},
        job_profile={"skills": ["python"]},
    )

    result = engine.process_answer(
        session=session,
        answer="I would use FastAPI with HTTP endpoints.",
        reference_answer="A REST API uses HTTP methods and authentication.",
    )

    assert result["evaluation"]["final_score"] == 78.0
    assert result["decision"]["action"] == "follow_up"
    assert len(result["history"]) == 1