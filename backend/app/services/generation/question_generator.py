from typing import Dict, List

from app.services.generation.llm_interface import LLMInterface
from app.services.generation.prompts import build_question_prompt


def generate_question(
    llm: LLMInterface,
    candidate_profile: Dict[str, object],
    jd_profile: Dict[str, object],
    matched_skills: List[str],
    missing_skills: List[str],
    interview_type: str = "technical",
    difficulty: str = "medium",
) -> str:
    """
    Generate one personalized interview question using the configured LLM.
    """

    prompt = build_question_prompt(
        candidate_profile=candidate_profile,
        jd_profile=jd_profile,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        interview_type=interview_type,
        difficulty=difficulty,
    )

    response = llm.generate(prompt)

    return response.strip()