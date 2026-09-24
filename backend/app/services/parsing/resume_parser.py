from pathlib import Path
from importlib import import_module

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF resume."""
    try:
        pdf_module = import_module("pypdf")
    except ModuleNotFoundError:
        # Support environments where the older package name is installed.
        pdf_module = import_module("PyPDF2")

    PdfReader = pdf_module.PdfReader
    reader = PdfReader(file_path)

    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)

    return "\n".join(pages).strip()


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX resume."""
    Document = import_module("docx").Document
    document = Document(file_path)

    paragraphs = [
        paragraph.text.strip()
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs).strip()


def extract_resume_text(file_path: str) -> str:
    """
    Extract resume text based on the file extension.

    Supported formats:
    - PDF
    - DOCX
    """
    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    if extension == ".docx":
        return extract_text_from_docx(file_path)

    raise ValueError(
        f"Unsupported resume format: {extension}. "
        "Supported formats are .pdf and .docx."
    )