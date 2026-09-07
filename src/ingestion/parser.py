from pathlib import Path
from docx import Document


def docx_to_sections(path: Path) -> list[dict]:
    doc = Document(path)

    sections = []
    current_section = None

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()

        if not text:
            continue

        style = paragraph.style.name

        if style.startswith("Heading"):
            # Save the previous section
            if current_section is not None:
                sections.append(current_section)

            current_section = {
                "heading": text,
                "content": [],
            }

        else:
            # Content belonging to the current heading
            if current_section is not None:
                current_section["content"].append(text)

    # Save the final section
    if current_section is not None:
        sections.append(current_section)

    return sections
