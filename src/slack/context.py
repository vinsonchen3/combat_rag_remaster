def get_thread_messages(
    client,
    channel: str,
    thread_ts: str,
) -> list[dict]:
    response = client.conversations_replies(
        channel=channel,
        ts=thread_ts,
    )
    return response["messages"]


def build_thread_context(messages: list[dict]) -> str:
    lines = []

    for message in messages:
        user = message.get("user", "Unknown")
        text = message.get("text", "")

        lines.append(f"{user}: {text}")

    return "\n".join(lines)
