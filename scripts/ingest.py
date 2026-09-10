from pathlib import Path

from src.ingestion.chunker import chunk_document
from src.ingestion.embedder import embed_chunks
from src.retrieval.vector_store import upsert_documents

DOCUMENTS_DIR = Path("documents")


def ingest_documents() -> None:
    for path in DOCUMENTS_DIR.glob("*.docx"):
        print(f"Ingesting {path.name}...")

        chunks = chunk_document(path)
        chunks = embed_chunks(chunks)

        ids = []
        documents = []
        embeddings = []

        for chunk in chunks:
            ids.append(chunk["id"])
            documents.append(chunk['text'])
            embeddings.append(chunk["embedding"])

        metadatas = [
            {"source": chunk["source"], "heading": chunk["heading"]} for chunk in chunks
        ]

        upsert_documents(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        print(f"Upserted {len(chunks)} chunks")


if __name__ == "__main__":
    ingest_documents()
