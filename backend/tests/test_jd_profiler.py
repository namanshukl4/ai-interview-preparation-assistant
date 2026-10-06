from app.services.profiling.jd_profiler import (
    build_jd_profile,
    extract_jd_sections,
    extract_responsibilities,
)


def test_extract_jd_sections():
    text = """
    Requirements
    Python, FastAPI, SQL

    Responsibilities
    - Build REST APIs
    - Design backend services
    """

    sections = extract_jd_sections(text)

    assert sections["requirements"] == "Python, FastAPI, SQL"
    assert "Build REST APIs" in sections["responsibilities"]


def test_extract_responsibilities():
    text = """
    Responsibilities
    - Build REST APIs
    - Design backend services
    - Write automated tests
    """

    responsibilities = extract_responsibilities(text)

    assert responsibilities == [
        "Build REST APIs",
        "Design backend services",
        "Write automated tests",
    ]


def test_build_jd_profile():
    text = """
    Requirements
    Python, FastAPI, SQL

    Responsibilities
    - Build REST APIs
    - Design backend services
    """

    profile = build_jd_profile(text)

    assert "python" in profile["skills"]
    assert "fastapi" in profile["skills"]
    assert "sql" in profile["skills"]

    assert profile["responsibilities"] == [
        "Build REST APIs",
        "Design backend services",
    ]

    assert "requirements" in profile["sections"]
    assert "responsibilities" in profile["sections"]
    assert profile["text_length"] == len(text)