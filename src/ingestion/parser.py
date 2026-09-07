from pathlib import Path
from docx import Document


def docx_to_string(path: Path) -> str:
    doc = Document(path)

    return "\n".join(
        paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()
    )