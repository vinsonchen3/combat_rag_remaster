from pathlib import Path
import chromadb

project_root = Path(__file__).resolve().parent.parent.parent
db_path = project_root / "chroma_db"

client = chromadb.PersistentClient(path=str(db_path))

collection = client.get_or_create_collection(name="combat_robotics")


def upsert_documents(
    ids: list[str],
    documents: list[str],
    embeddings: list[list[float]],
    metadatas: list[dict],
):
    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )
