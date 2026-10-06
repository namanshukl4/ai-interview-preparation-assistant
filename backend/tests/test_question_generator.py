from app.services.generation.question_generator import generate_question


def test_generate_question_targets_missing_skill():
    candidate_profile = {
        "skills": ["python", "fastapi"],
    }

    jd_profile = {
        "skills": ["python", "fastapi", "docker"],
        "responsibilities": ["Build REST APIs"],
    }

    result = generate_question(
        candidate_profile=candidate_profile,
        jd_profile=jd_profile,
        interview_type="technical",
        difficulty="medium",
    )

    assert isinstance(result, str)
    assert result.strip()
    assert "Docker" in result


def test_generate_question_uses_matched_skill_when_no_gap_exists():
    candidate_profile = {
        "skills": ["python", "fastapi"],
    }

    jd_profile = {
        "skills": ["python", "fastapi"],
        "responsibilities": ["Build REST APIs"],
    }

    result = generate_question(
        candidate_profile=candidate_profile,
        jd_profile=jd_profile,
        interview_type="technical",
        difficulty="medium",
    )

    assert isinstance(result, str)
    assert result.strip()


def test_generate_question_supports_behavioral_interview():
    candidate_profile = {
        "skills": ["python"],
    }

    jd_profile = {
        "skills": ["python"],
        "responsibilities": ["Build backend services"],
    }

    result = generate_question(
        candidate_profile=candidate_profile,
        jd_profile=jd_profile,
        interview_type="behavioral",
        difficulty="medium",
    )

    assert isinstance(result, str)
    assert result.strip()
    assert "Python" in result


def test_generate_question_falls_back_for_unknown_options():
    candidate_profile = {
        "skills": ["python"],
    }

    jd_profile = {
        "skills": ["python"],
        "responsibilities": [],
    }

    result = generate_question(
        candidate_profile=candidate_profile,
        jd_profile=jd_profile,
        interview_type="unknown",
        difficulty="unknown",
    )

    assert isinstance(result, str)
    assert result.strip()
