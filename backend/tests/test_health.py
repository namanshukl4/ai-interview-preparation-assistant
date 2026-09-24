from pathlib import Path

import unittest
from importlib import import_module

from app.services.parsing.resume_parser import extract_resume_text


Document = import_module("docx").Document


def _write_test_pdf(path: Path) -> None:
    stream = b"BT\n/F1 12 Tf\n100 750 Td\n(Naman Shukla) Tj\n0 -20 Td\n(Python FastAPI SQL) Tj\nET\n"
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