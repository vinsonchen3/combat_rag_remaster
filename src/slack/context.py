from slack_sdk.web.client import WebClient


def get_thread_messages(
    client: WebClient,
    channel: str,
    thread_ts: str,
) -> list[dict]:
    response = client.conversations_replies(
        channel=channel,
        ts=thread_ts,
    )
    return [
        {
            "user": message.get("user", "unknown"),
            "text": message.get("text", ""),
            "ts": message.get("ts", ""),
        }
        for message in response.get("messages", [])
        if message.get("text")
    ]


def format_thread_messages(messages: list[dict]) -> str:
    """
    Convert structured Slack messages into plain text context
    for the LLM.
    """

    return "\n".join(f"{message['user']}: {message['text']}" for message in messages)
