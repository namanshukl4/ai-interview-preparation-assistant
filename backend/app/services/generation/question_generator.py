from typing import Dict, List

from app.services.profiling.profile_matcher import calculate_skill_match


QUESTION_TEMPLATES = {
    "technical": {
        "easy": [
            "What is {skill}, and how would you use it in a backend application?",
            "Explain the basic purpose of {skill} and where you would use it.",
        ],
        "medium": [
            "How would you use {skill} when building a backend application?",
            "How would you implement a practical solution using {skill} in a backend project?",
        ],
        "hard": [
            "You are designing a production backend system. How would you use {skill}, and what design decisions would you consider?",
            "How would you apply {skill} to build a scalable backend system, and what trade-offs would you consider?",
        ],
    },
    "behavioral": {
        "easy": [
            "Tell me about a project where you used {skill}.",
            "Describe your experience working with {skill}.",
        ],
        "medium": [
            "Tell me about a time you used {skill} to solve a challenging problem.",
            "Describe a project where your experience with {skill} made an important difference.",
        ],
        "hard": [
            "Describe a challenging situation involving {skill}, the decision you made, and the outcome.",
            "Tell me about a situation where you had to make an important technical decision involving {skill}. What was your reasoning?",
        ],
    },
}


def _normalize(value: object) -> str:
    return str(value).strip().lower()


def _clean_skill(skill: str) -> str:
    """Format a normalized skill for presentation."""
    known_names = {
        "python": "Python",
        "fastapi": "FastAPI",
        "sql": "SQL",
        "docker": "Docker",
        "javascript": "JavaScript",
        "typescript": "TypeScript",
        "java": "Java",
        "c++": "C++",
        "c": "C",
        "react": "React",
        "node.js": "Node.js",
        "node": "Node.js",
        "mongodb": "MongoDB",
        "postgresql": "PostgreSQL",
        "git": "Git",
    }

    normalized = _normalize(skill)
    return known_names.get(normalized, str(skill).strip())


def _select_skill(
    matched_skills: List[str],
    missing_skills: List[str],
    responsibilities: List[str],
) -> str:
    """
    Select the most useful concept to test.

    Missing skills receive priority because they represent candidate-JD gaps.
    Otherwise, a matched skill is selected.
    """

    if missing_skills:
        return _clean_skill(missing_skills[0])

    if matched_skills:
        return _clean_skill(matched_skills[0])

    if responsibilities:
        return "backend system design"

    return "software development"


def generate_personalized_question(
    candidate_profile: Dict[str, object],
    jd_profile: Dict[str, object],
    interview_type: str = "technical",
    difficulty: str = "medium",
) -> str:
    """
    Generate one personalized interview question without using an LLM.

    The generator uses candidate/JD skill matching, interview type,
    difficulty, and job responsibilities to select and personalize
    a question template.
    """

    candidate_skills = candidate_profile.get("skills", [])
    required_skills = jd_profile.get("skills", [])
    responsibilities = jd_profile.get("responsibilities", [])

    match = calculate_skill_match(
        candidate_skills,
        required_skills,
    )

    matched_skills = match["matched_skills"]
    missing_skills = match["missing_skills"]

    interview_type = _normalize(interview_type)
    difficulty = _normalize(difficulty)

    if interview_type not in QUESTION_TEMPLATES:
        interview_type = "technical"

    if difficulty not in QUESTION_TEMPLATES[interview_type]:
        difficulty = "medium"

    skill = _select_skill(
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        responsibilities=responsibilities,
    )

    templates = QUESTION_TEMPLATES[interview_type][difficulty]

    # Deterministic template selection makes the MVP reproducible.
    template_index = (
        len(matched_skills) + len(missing_skills)
    ) % len(templates)

    return templates[template_index].format(skill=skill).strip()


def generate_question(
    candidate_profile: Dict[str, object],
    jd_profile: Dict[str, object],
    interview_type: str = "technical",
    difficulty: str = "medium",
) -> str:
    """
    Public question-generation interface.

    This deliberately contains no LLM dependency.
    """

    return generate_personalized_question(
        candidate_profile=candidate_profile,
        jd_profile=jd_profile,
        interview_type=interview_type,
        difficulty=difficulty,
    )
