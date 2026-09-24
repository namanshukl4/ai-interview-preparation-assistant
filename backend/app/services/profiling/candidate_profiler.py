import re
from typing import Dict, List


DEFAULT_SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "javascript",
    "typescript",
    "sql",
    "html",
    "css",
    "react",
    "next.js",
    "node.js",
    "fastapi",
    "flask",
    "django",
    "mongodb",
    "postgresql",
    "mysql",
    "git",
    "docker",
    "aws",
    "azure",
    "gcp",
    "machine learning",
    "deep learning",
    "natural language processing",
    "nlp",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "pandas",
    "numpy",
    "rest api",
    "rest apis",
    "data structures",
    "algorithms",
]


def normalize_text(text: str) -> str:
    """Normalize whitespace and casing for profiling."""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_skills(
    text: str,
    skill_taxonomy: List[str] | None = None,
) -> List[str]:
    """
    Extract skills from text using a configurable skill taxonomy.

    Matching is case-insensitive and returns each skill once.
    """
    if not text:
        return []

    taxonomy = skill_taxonomy or DEFAULT_SKILLS
    normalized_text = normalize_text(text)

    found_skills = []

    for skill in taxonomy:
        normalized_skill = normalize_text(skill)

        pattern = rf"(?<!\w){re.escape(normalized_skill)}(?!\w)"

        if re.search(pattern, normalized_text):
            found_skills.append(skill)

    return found_skills


def extract_sections(text: str) -> Dict[str, str]:
    """
    Extract common resume sections using section headings.

    This is intentionally lightweight. More advanced semantic
    extraction can be added later without changing the profiler API.
    """
    if not text:
        return {}

    section_names = [
        "summary",
        "objective",
        "education",
        "experience",
        "work experience",
        "projects",
        "skills",
        "certifications",
        "achievements",
    ]

    pattern = "|".join(
        re.escape(section)
        for section in sorted(section_names, key=len, reverse=True)
    )

    matches = list(
        re.finditer(
            rf"(?im)^\s*({pattern})\s*:?\s*$",
            text,
        )
    )

    sections: Dict[str, str] = {}

    for index, match in enumerate(matches):
        section_name = match.group(1).lower()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)

        content = text[start:end].strip()

        if section_name in sections and content:
            sections[section_name] += "\n" + content
        else:
            sections[section_name] = content

    return sections


def build_candidate_profile(resume_text: str) -> Dict[str, object]:
    """
    Build a structured candidate profile from extracted resume text.
    """
    return {
        "skills": extract_skills(resume_text),
        "sections": extract_sections(resume_text),
        "text_length": len(resume_text),
    }