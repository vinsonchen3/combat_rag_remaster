import os
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = "gpt-5.6-luna"
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def build_document_context(chunks: list[dict]) -> str:
    """Format retrieved chunks into context for the LLM."""

    return "\n\n".join(
        f"Source: {chunk['metadata']['source']}\n"
        f"Heading: {chunk['metadata']['heading']}\n"
        f"{chunk['text']}"
        for chunk in chunks
    )


def build_source_list(
    chunks: list[dict],
    cited_numbers: set[int],
) -> str:
    """Format retrieved chunks into a numbered source list."""

    return "\n".join(
        f"[{i}] `{chunk['metadata']['source']}` — " f"{chunk['metadata']['heading']}"
        for i, chunk in enumerate(chunks, start=1)
        if i in cited_numbers
    )


def get_cited_source_numbers(answer: str) -> set[int]:
    """Return valid source numbers referenced in the generated answer."""

    cited_numbers = {int(num) for num in re.findall(r"\[(\d+)\]", answer)}

    return cited_numbers


def generate_answer(
    question: str,
    chunks: list[dict],
    conversation_context: str | None = None,
) -> str:
    """Generate an answer using the retrieved chunks as context."""

    chunk_context_section = build_document_context(chunks)
    conversation_context_section = ""

    if conversation_context:
        conversation_context_section = (
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
            "SOURCE CITATIONS:\n"
            "The documentation context contains numbered sources such as "
            "[1], [2], and [3]. "
            "When you make a factual claim that is supported by the "
            "documentation, cite the supporting source immediately after "
            "the sentence using its number, for example: "
            "'The motor requires a 12V supply.[1]' "
            "If a sentence is supported by multiple sources, cite all "
            "relevant sources, for example [1][3]. "
            "Only use citation numbers that appear in the provided "
            "documentation context. "
            "Do not create, modify, or guess source numbers. "
            "Do not put citations in a separate citation section; "
            "place them directly after the relevant sentence.\n\n"
            """
            Format your response for Slack using Slack-compatible mrkdwn.

            Use:
            - *bold* for emphasis
            - `code` for commands, filenames, or code
            - numbered lists for procedures
            - bullet lists for multiple items

            Do NOT use Markdown headings such as #, ##, or ###.
            Do NOT use Markdown bold syntax such as **bold**.
            Keep responses concise and easy to read in Slack.
            """
        ),
        input=(
            f"Documentation context:\n{chunk_context_section}\n"
            f"{conversation_context_section}\n\n"
            f"Current question:\n{question}"
        ),
    )

    answer = response.output_text
    cited_numbers = get_cited_source_numbers(answer)
    source_list = build_source_list(chunks, cited_numbers)
    if not source_list:
        return f"{answer}"
    return f"{answer}\n\n *Sources:*\n{source_list}"
