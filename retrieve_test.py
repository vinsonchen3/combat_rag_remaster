from sentence_transformers import SentenceTransformer
import chromadb

from src.retrieval.retriever import Retriever


def test_retrieve():
    client = chromadb.PersistentClient(path="chroma_db")
    collection = client.get_collection("combat_robotics")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    retriever = Retriever(
        collection=collection,
        model=model,
        top_k=3,
    )

    results = retriever.retrieve("How do I configure the motor controller?")

    print(results)

    assert len(results) == 3
    assert "text" in results[0]
    assert "metadata" in results[0]


if __name__ == "__main__":
    test_retrieve()