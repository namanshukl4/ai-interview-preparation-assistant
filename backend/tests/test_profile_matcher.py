from app.services.profiling.profile_matcher import (
    build_profile_match,
    calculate_skill_match,
)


def test_calculate_skill_match():
    result = calculate_skill_match(
        ["Python", "FastAPI", "SQL"],
        ["Python", "SQL", "Docker", "AWS"],
    )

    assert result["matched_skills"] == ["python", "sql"]
    assert result["missing_skills"] == ["aws", "docker"]
    assert result["match_score"] == 50.0


def test_calculate_skill_match_with_no_required_skills():
    result = calculate_skill_match(
        ["Python", "SQL"],
        [],
    )

    assert result["matched_skills"] == []
    assert result["missing_skills"] == []
    assert result["match_score"] == 0.0


def test_build_profile_match():
    candidate_profile = {
        "skills": ["Python", "FastAPI", "SQL"],
    }

    jd_profile = {
        "skills": ["Python", "SQL", "Docker"],
    }

    result = build_profile_match(
        candidate_profile,
        jd_profile,
    )

    assert result["matched_skills"] == ["python", "sql"]
    assert result["missing_skills"] == ["docker"]
    assert result["match_score"] == 66.67