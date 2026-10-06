from app.services.evaluation.answer_evaluator import (
    AnswerEvaluator,
    evaluate_answer,
)


def test_normalize_concepts():
    concepts = [" FastAPI ", "Python", " REST APIs "]

    result = AnswerEvaluator.normalize_concepts(concepts)

    assert result == [
        "fastapi",
        "python",
        "rest apis",
    ]


def test_concept_coverage():
    result = AnswerEvaluator.calculate_concept_coverage(
        candidate_answer=(
            "FastAPI is a Python framework used to build REST APIs."
        ),
        required_concepts=[
            "FastAPI",
            "Python",
            "REST APIs",
            "Docker",
        ],
    )

    assert result["covered_concepts"] == [
        "fastapi",
        "python",
        "rest apis",
    ]

    assert result["missing_concepts"] == [
        "docker",
    ]

    assert result["coverage_score"] == 0.75


def test_empty_answer():
    result = evaluate_answer(
        candidate_answer="",
        reference_answer="FastAPI is a Python framework.",
        required_concepts=["FastAPI", "Python"],
    )

    assert result["semantic_score"] == 0.0
    assert result["coverage_score"] == 0.0
    assert result["final_score"] == 0.0


def test_answer_evaluation():
    result = evaluate_answer(
        candidate_answer=(
            "FastAPI is a Python framework used to build REST APIs."
        ),
        reference_answer=(
            "FastAPI is a Python framework for building REST APIs."
        ),
        required_concepts=[
            "FastAPI",
            "Python",
            "REST APIs",
        ],
    )

    assert result["semantic_score"] > 70
    assert result["coverage_score"] == 100.0
    assert result["final_score"] > 70
    assert result["missing_concepts"] == []