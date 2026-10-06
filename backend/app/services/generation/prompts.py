from typing import Dict, List


def build_question_prompt(
    candidate_profile: Dict[str, object],
    jd_profile: Dict[str, object],
    matched_skills: List[str],
    missing_skills: List[str],
    interview_type: str = "technical",
    difficulty: str = "medium",
) -> str:
    """Build a structured prompt for personalized interview-question generation."""

    candidate_skills = candidate_profile.get("skills", [])
    jd_skills = jd_profile.get("skills", [])
    responsibilities = jd_profile.get("responsibilities", [])

    return f"""
You are an AI interview preparation assistant.

Generate ONE personalized interview question.

Interview type: {interview_type}
Difficulty: {difficulty}

Candidate skills:
{candidate_skills}

Job-required skills:
{jd_skills}

Matched skills:
{matched_skills}

Missing or weaker skills:
{missing_skills}

Job responsibilities:
{responsibilities}

Rules:
1. Ask exactly one interview question.
2. Make the question relevant to the target role.
3. Use the candidate's background when possible.
4. Prefer testing one important skill or responsibility at a time.
5. If a missing skill is relevant, use it to identify a knowledge gap.
6. Do not provide the answer.
7. Do not include explanations or multiple questions.

Return only the interview question.
""".strip()