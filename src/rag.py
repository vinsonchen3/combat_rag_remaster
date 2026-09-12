from src.retrieval.retriever import Retriever
from src.llm.openai_client import generate_answer


def answer_question(
    question: str,
    retriever: Retriever,
    conversation_context: str | None = None,
) -> str:
    chunks = retriever.retrieve(question)

    return generate_answer(
        question=question,
        chunks=chunks,
        conversation_context=conversation_context,
    )
