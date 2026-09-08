from pathlib import Path
from src.ingestion.chunker import chunk_document
from src.ingestion.embedder import embed_document
from src.ingestion.parser import docx_to_sections

path = Path("documents/How-To_ Design an Asymmetric Spinning Weapon.docx")

chunks = chunk_document(path)

chunks = embed_document(chunks)

for chunk in chunks:
    print(chunk["source"])
    print(chunk["heading"])
    print(len(chunk['embedding']))
    print()
# sections = docx_to_sections(path)

# for section in sections:
#     print(section)