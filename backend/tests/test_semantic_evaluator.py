from app.services.evaluation.semantic_evaluator import SemanticEvaluator


def test_semantic_similarity_high_for_similar_answers():
    evaluator = SemanticEvaluator()

    score = evaluator.calculate_similarity(
        "FastAPI can be used to build REST APIs in Python.",
        "Python FastAPI is commonly used for developing REST APIs.",
    )

    assert 0.7 <= score <= 1.0


def test_semantic_similarity_lower_for_unrelated_answers():
    evaluator = SemanticEvaluator()

    score = evaluator.calculate_similarity(
        "FastAPI is a Python web framework.",
        "The candidate has experience with database normalization.",
    )

    assert 0.0 <= score < 0.7


def test_empty_answer_returns_zero():
    evaluator = SemanticEvaluator()

    score = evaluator.calculate_similarity(
        "",
        "FastAPI is a Python web framework.",
    )

    assert score == 0.0
