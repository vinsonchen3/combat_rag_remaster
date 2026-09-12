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
