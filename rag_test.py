import chromadb
from sentence_transformers import SentenceTransformer

from src.retrieval.retriever import Retriever
from src.rag import answer_question


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)

chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_collection(name="combat_robotics")

retriever = Retriever(
    collection=collection,
    model=model,
    top_k=3,
)


def test_rag():
    question = "What battery should we use?"

    answer = answer_question(
        question=question,
        retriever=retriever,
    )

    print(answer)


if __name__ == "__main__":
    test_rag()