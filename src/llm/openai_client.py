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


def build_conversation_context(messages: list[dict]) -> str:
    """Format Slack thread messages into conversational context."""
    lines = []

    for message in messages:
        user = message.get("user", "Unknown")
        text = message.get("text", "")

        lines.append(f"{user}: {text}")

    return "\n".join(lines)


def generate_answer(
    question: str,
    chunks: list[dict],
    conversation_context: str | None = None,
) -> str:
    """Generate an answer using the retrieved chunks as context."""

    chunk_context_section = build_context(chunks)
    conversation_context_section = ""

    if conversation_context:
        conversation_context = (
            "\n\nConversation history from the Slack thread:\n"
            f"{conversation_context}"
        )

    response = client.responses.create(
        model=MODEL,
        instructions=(
            "You are a helpful assistant for Cornell Combat Robotics. "
            "Answer the user's question using the provided documentation "
            "and, when useful, the Slack conversation history. "
            "The documentation is the authoritative source for technical facts. "
            "Use the conversation history only to understand references, "
            "previous discussion, or conversational context. "
            "If the documentation does not contain enough information to "
            "answer the question, say that you don't know based on the "
            "provided documents. Do not invent information."
        ),
        input=(
            f"Documentation context:\n{chunk_context_section}\n"
            f"{conversation_context_section}\n\n"
            f"Current question:\n{question}"
        ),
    )

    return response.output_text
