from pathlib import Path
from importlib import import_module
from zipfile import ZipFile
from xml.etree import ElementTree


def _get_pdf_reader():
    """Return PdfReader without requiring pypdf when parsing other formats."""
    try:
        return import_module("pypdf").PdfReader
    except ModuleNotFoundError as error:
        raise RuntimeError(
            "PDF parsing requires the 'pypdf' package to be installed."
        ) from error


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF job description."""
    reader = _get_pdf_reader()(file_path)

    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)

    return "\n".join(pages).strip()


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX job description."""
    with ZipFile(file_path) as archive:
        document_xml = archive.read("word/document.xml")

    root = ElementTree.fromstring(document_xml)
    namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    paragraphs = []

    for paragraph in root.iter(f"{namespace}p"):
        text = "".join(
            node.text or ""
            for node in paragraph.iter(f"{namespace}t")
        ).strip()
        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs).strip()


def extract_text_from_txt(file_path: str) -> str:
    """Extract text from a plain-text job description."""
    return Path(file_path).read_text(encoding="utf-8").strip()


def extract_jd_text(file_path: str) -> str:
    """
    Extract job-description text based on the file extension.

    Supported formats:
    - PDF
    - DOCX
    - TXT
    """
    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    if extension == ".docx":
        return extract_text_from_docx(file_path)

    if extension == ".txt":
        return extract_text_from_txt(file_path)

    raise ValueError(
        f"Unsupported job description format: {extension}. "
        "Supported formats are .pdf, .docx, and .txt."
    )