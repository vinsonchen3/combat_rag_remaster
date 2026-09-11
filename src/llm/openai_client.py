import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = "gpt-5.6-luna"
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def build_context(chunks: list[dict]) -> str:
    """Format retrieved chunks into context for the LLM."""

    return "\n\n".join(
        f"Source: {chunk['metadata']['source']}\n"
        f"Heading: {chunk['metadata']['heading']}\n"
        f"{chunk['text']}"
        for chunk in chunks
    )


def generate_answer(question: str, chunks: list[dict]) -> str:
    """Generate an answer using the retrieved chunks as context."""

    context = build_context(chunks)

    response = client.responses.create(
        model=MODEL,
        instructions="You are a helpful assistant for Cornell Combat Robotics. "
        "Answer the user's question using only the provided context. "
        "If the context does not contain enough information to answer "
        "the question, say that you don't know based on the provided "
        "documents. Do not invent information.",
        input=(f"Context:\n{context}\n\n" f"Question:\n{question}"),
    )

    return response.output_text
