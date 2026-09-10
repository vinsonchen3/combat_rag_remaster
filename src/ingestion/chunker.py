from pathlib import Path
from src.ingestion.parser import docx_to_sections


def chunk_document(path: Path) -> list[dict]:
    sections = docx_to_sections(path)

    chunks = []

    for i, section in enumerate(sections):
        if not section["content"]:
            continue

        chunks.append(
            {
                "id": f"{path.name}:{i}",
                "source": path.name,
                "heading": section["heading"],
                "text": "\n".join(section["content"]),
            }
        )

    return chunks
