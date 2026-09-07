from pathlib import Path
from src.ingestion.loader import load_document
from src.ingestion.parser import docx_to_sections

path = Path("documents/How-To_ Design an Asymmetric Spinning Weapon.docx")

print(load_document(path))
# sections = docx_to_sections(path)

# for section in sections:
#     print(section)