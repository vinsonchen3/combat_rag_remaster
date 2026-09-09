from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

project_root = Path(__file__).resolve().parent.parent.parent
db_path = project_root / "chroma_db"

client = chromadb.PersistentClient(path=str(db_path))

ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.get_or_create_collection(
    name="combat_robotics",
    metadata={"hnsw:space": "cosine"},
    embedding_function=ef,
)


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
