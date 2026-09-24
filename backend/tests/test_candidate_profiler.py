from app.services.profiling.candidate_profiler import (
    build_candidate_profile,
    extract_sections,
    extract_skills,
    normalize_text,
)


def test_normalize_text():
    text = "  Python   FASTAPI\nSQL  "

    assert normalize_text(text) == "python fastapi sql"


def test_extract_skills():
    text = """
    Skills
    Python, FastAPI, SQL, Docker

    Education
    B.Tech Computer Science
    """

    skills = extract_skills(text)

    assert "python" in skills
    assert "fastapi" in skills
    assert "sql" in skills
    assert "docker" in skills
    assert "c" not in skills


def test_extract_sections():
    text = """
    Skills
    Python, FastAPI, SQL

    Education
    B.Tech Computer Science

    Projects
    AI Interview Preparation System
    """

    sections = extract_sections(text)

    assert sections["skills"] == "Python, FastAPI, SQL"
    assert sections["education"] == "B.Tech Computer Science"
    assert sections["projects"] == "AI Interview Preparation System"


def test_build_candidate_profile():
    text = """
    Skills
    Python, FastAPI, SQL

    Education
    B.Tech Computer Science
    """

    profile = build_candidate_profile(text)

    assert profile["skills"] == ["python", "sql", "fastapi"]
    assert "skills" in profile["sections"]
    assert "education" in profile["sections"]
    assert profile["text_length"] == len(text)