from app.services.interview.adaptive_engine import (
    AdaptiveInterviewEngine,
    decide_next_action,
)


def test_low_score_with_missing_concepts_returns_follow_up():
    result = decide_next_action(
        evaluation={
            "final_score": 52.0,
            "missing_concepts": [
                "authentication",
                "docker",
            ],
        },
        question_number=1,
    )

    assert result["action"] == "follow_up"
    assert result["focus_concepts"] == [
        "authentication",
        "docker",
    ]


def test_low_score_without_missing_concepts_returns_follow_up():
    result = decide_next_action(
        evaluation={
            "final_score": 60.0,
            "missing_concepts": [],
        },
        question_number=2,
    )

    assert result["action"] == "follow_up"
    assert result["focus_concepts"] == []


def test_good_answer_moves_to_next_topic():
    result = decide_next_action(
        evaluation={
            "final_score": 88.0,
            "missing_concepts": [],
        },
        question_number=1,
    )

    assert result["action"] == "next_topic"
    assert result["focus_concepts"] == []


def test_max_questions_finishes_interview():
    result = decide_next_action(
        evaluation={
            "final_score": 88.0,
            "missing_concepts": [],
        },
        question_number=5,
    )

    assert result["action"] == "finish"


def test_custom_threshold():
    engine = AdaptiveInterviewEngine(
        max_questions=10,
        follow_up_threshold=80.0,
    )

    result = engine.decide_next_action(
        evaluation={
            "final_score": 75.0,
            "missing_concepts": ["Docker"],
        },
        question_number=3,
    )

    assert result["action"] == "follow_up"
    assert result["focus_concepts"] == ["Docker"]