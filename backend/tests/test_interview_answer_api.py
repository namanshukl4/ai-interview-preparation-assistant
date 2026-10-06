from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_submit_answer_returns_evaluation_and_decision():
    session = {
        "status": "active",
        "question_number": 1,
        "question": "What is FastAPI and why would you use it?",
        "history": [],
    }

    answer = (
        "FastAPI is a Python web framework for building "
        "REST APIs with request validation and automatic documentation."
    )

    response = client.post(
        "/api/interview/answer",
        json={
            "session": session,
            "answer": answer,
            "reference_answer": (
                "FastAPI is a Python framework for building REST APIs. "
                "It provides request validation, type hints, and automatic documentation."
            ),
            "missing_concepts": [],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "evaluation" in data
    assert "decision" in data
    assert "history" in data

    assert "final_score" in data["evaluation"]
    assert "action" in data["decision"]

    assert len(data["history"]) == 1
    assert data["history"][0]["question"] == session["question"]
    assert data["history"][0]["answer"] == answer


def test_submit_answer_requires_session():
    response = client.post(
        "/api/interview/answer",
        json={
            "session": {},
            "answer": "FastAPI is a Python web framework.",
            "reference_answer": "FastAPI is a Python framework.",
            "missing_concepts": [],
        },
    )

    assert response.status_code == 400
