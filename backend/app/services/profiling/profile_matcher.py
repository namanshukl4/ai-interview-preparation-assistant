from typing import Dict, List


def calculate_skill_match(
    candidate_skills: List[str],
    required_skills: List[str],
) -> Dict[str, object]:
    """
    Compare candidate skills against skills required by a job description.
    """

    candidate_set = {
        skill.strip().lower()
        for skill in candidate_skills
        if skill.strip()
    }

    required_set = {
        skill.strip().lower()
        for skill in required_skills
        if skill.strip()
    }

    matched_skills = sorted(candidate_set & required_set)
    missing_skills = sorted(required_set - candidate_set)

    if not required_set:
        match_score = 0.0
    else:
        match_score = round(
            (len(matched_skills) / len(required_set)) * 100,
            2,
        )

    return {
        "candidate_skills": sorted(candidate_set),
        "required_skills": sorted(required_set),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_score": match_score,
    }


def build_profile_match(
    candidate_profile: Dict[str, object],
    jd_profile: Dict[str, object],
) -> Dict[str, object]:
    """Build a candidate-vs-JD skill match."""

    candidate_skills = candidate_profile.get("skills", [])
    required_skills = jd_profile.get("skills", [])

    return calculate_skill_match(
        candidate_skills,
        required_skills,
    )