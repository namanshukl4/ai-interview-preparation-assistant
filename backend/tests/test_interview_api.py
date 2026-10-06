from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_start_interview_returns_first_question():
    response = client.post(
        "/api/interview/start",
        json={
            "candidate_profile": {
                "name": "Test Candidate",
                "target_role": "Backend Developer",
                "skills": [
                    "Python",
                    "FastAPI",
                    "SQL",
                ],
            },
            "job_profile": {
                "skills": [
                    "Python",
                    "FastAPI",
                    "Docker",
                    "SQL",
                ],
                "responsibilities": [
                    "Build REST APIs",
                    "Develop backend services",
                    "Design scalable applications",
                ],
            },
            "interview_type": "technical",
            "difficulty": "medium",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "active"
    assert data["question_number"] == 1
    assert isinstance(data["question"], str)
    assert data["question"].strip() != ""
    assert data["history"] == []


def test_start_interview_requires_candidate_profile():
    response = client.post(
        "/api/interview/start",
        json={
            "job_profile": {
                "skills": ["Python"],
                "responsibilities": ["Build APIs"],
            },
            "interview_type": "technical",
            "difficulty": "medium",
        },
    )

    assert response.status_code == 422
