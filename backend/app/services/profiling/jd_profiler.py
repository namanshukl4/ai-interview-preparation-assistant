import re
from typing import Dict, List

from app.services.profiling.candidate_profiler import (
    extract_skills,
    normalize_text,
)


RESPONSIBILITY_HEADINGS = [
    "responsibilities",
    "key responsibilities",
    "what you will do",
    "what you'll do",
    "role and responsibilities",
    "duties",
]

REQUIREMENT_HEADINGS = [
    "requirements",
    "qualifications",
    "required qualifications",
    "basic qualifications",
    "preferred qualifications",
    "skills",
    "required skills",
]


def extract_jd_sections(text: str) -> Dict[str, str]:
    """Extract common job-description sections from plain text."""
    if not text:
        return {}

    section_names = (
        RESPONSIBILITY_HEADINGS
        + REQUIREMENT_HEADINGS
        + [
            "about the role",
            "about the job",
            "job description",
            "overview",
        ]
    )

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
        section_name = normalize_text(match.group(1))
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)

        content = text[start:end].strip()

        if content:
            sections[section_name] = content

    return sections


def extract_responsibilities(text: str) -> List[str]:
    """Extract bullet-style responsibilities from a JD."""
    sections = extract_jd_sections(text)

    responsibility_text = ""

    for heading in RESPONSIBILITY_HEADINGS:
        normalized_heading = normalize_text(heading)

        if normalized_heading in sections:
            responsibility_text += (
                sections[normalized_heading] + "\n"
            )

    if not responsibility_text:
        return []

    responsibilities = []

    for line in responsibility_text.splitlines():
        line = line.strip()

        if not line:
            continue

        line = re.sub(r"^[•*\-–—]\s*", "", line).strip()

        if line:
            responsibilities.append(line)

    return responsibilities


def build_jd_profile(jd_text: str) -> Dict[str, object]:
    """Build a structured job-description profile."""
    sections = extract_jd_sections(jd_text)

    return {
        "skills": extract_skills(jd_text),
        "responsibilities": extract_responsibilities(jd_text),
        "sections": sections,
        "text_length": len(jd_text),
    }