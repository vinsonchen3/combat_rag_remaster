from pathlib import Path
from src.ingestion.parser import docx_to_sections


def load_document(path: Path) -> list[dict]:
    sections = docx_to_sections(path)

    return [
        {
            "source": path.name,
            "heading": section["heading"],
            "text": "\n".join(section["content"])
        }
        for section in sections
    ]
