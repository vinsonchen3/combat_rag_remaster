from pathlib import Path
from src.ingestion.parser import docx_to_sections


# don't need separate chunking algorithm apart from this since all the heading sections are small and don't need to be split up more.
def chunk_document(path: Path) -> list[dict]:
    sections = docx_to_sections(path)

    return [
        {
            "source": path.name,
            "heading": section["heading"],
            "text": "\n".join(section["content"]),
        }
        for section in sections
    ]
