from pathlib import Path

import unittest
from importlib import import_module

from app.services.parsing.resume_parser import extract_resume_text
from app.services.parsing.jd_parser import extract_jd_text


Document = import_module("docx").Document


def _write_test_pdf(
    path: Path,
    first_line: str = "Naman Shukla",
    second_line: str = "Python FastAPI SQL",
) -> None:
    stream = (
        f"BT\n/F1 12 Tf\n100 750 Td\n({first_line}) Tj\n"
        f"0 -20 Td\n({second_line}) Tj\nET\n"
    ).encode()
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"endstream",
    ]
    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for number, obj in enumerate(objects, 1):
        offsets.append(len(pdf))
        pdf.extend(f"{number} 0 obj\n".encode())
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")
    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode())
    pdf.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode()
    )
    path.write_bytes(pdf)


def test_extract_resume_text_from_pdf(tmp_path: Path):
    pdf_path = tmp_path / "resume.pdf"

    _write_test_pdf(pdf_path)

    text = extract_resume_text(str(pdf_path))

    assert "Naman Shukla" in text
    assert "Python FastAPI SQL" in text


def test_extract_resume_text_from_docx(tmp_path: Path):
    docx_path = tmp_path / "resume.docx"

    document = Document()
    document.add_paragraph("Naman Shukla")
    document.add_paragraph("Python FastAPI SQL")
    document.save(str(docx_path))

    text = extract_resume_text(str(docx_path))

    assert "Naman Shukla" in text
    assert "Python FastAPI SQL" in text


def test_unsupported_resume_format(tmp_path: Path):
    txt_path = tmp_path / "resume.txt"
    txt_path.write_text("Sample resume")

    with unittest.TestCase().assertRaisesRegex(
        ValueError, "Unsupported resume format"
    ):
        extract_resume_text(str(txt_path))

def test_extract_jd_text_from_pdf(tmp_path: Path):
    pdf_path = tmp_path / "job_description.pdf"

    _write_test_pdf(
        pdf_path,
        first_line="Software Engineer",
        second_line="Python FastAPI SQL REST APIs",
    )

    text = extract_jd_text(str(pdf_path))

    assert "Software Engineer" in text
    assert "Python FastAPI SQL REST APIs" in text


def test_extract_jd_text_from_docx(tmp_path: Path):
    docx_path = tmp_path / "job_description.docx"

    document = Document()
    document.add_paragraph("Software Engineer")
    document.add_paragraph("Python FastAPI SQL REST APIs")
    document.save(str(docx_path))

    text = extract_jd_text(str(docx_path))

    assert "Software Engineer" in text
    assert "Python FastAPI SQL REST APIs" in text


def test_extract_jd_text_from_txt(tmp_path: Path):
    txt_path = tmp_path / "job_description.txt"
    txt_path.write_text(
        "Software Engineer\nPython FastAPI SQL REST APIs",
        encoding="utf-8",
    )

    text = extract_jd_text(str(txt_path))

    assert "Software Engineer" in text
    assert "Python FastAPI SQL REST APIs" in text


def test_unsupported_jd_format(tmp_path: Path):
    file_path = tmp_path / "job_description.csv"
    file_path.write_text("role,skills")

    with unittest.TestCase().assertRaisesRegex(
        ValueError, "Unsupported job description format"
    ):
        extract_jd_text(str(file_path))