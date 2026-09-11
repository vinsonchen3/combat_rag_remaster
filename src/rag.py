from src.retrieval.retriever import Retriever
from src.llm.openai_client import generate_answer


def answer_question(
    question: str,
    retriever: Retriever,
) -> str:
    chunks = retriever.retrieve(question)

    return generate_answer(
        question=question,
        chunks=chunks,
    )
