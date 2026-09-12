import os
from dotenv import load_dotenv

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from src.slack.context import (
    get_thread_messages,
    build_conversation_context,
)

load_dotenv()

app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
)


@app.event("app_mention")
def handle_mention(event, client, say):

    channel = event["channel"]

    # If this message is already inside a thread,
    # use the thread's root timestamp.
    #
    # Otherwise, this message starts a new thread.
    thread_ts = event.get("thread_ts", event["ts"])

    messages = get_thread_messages(
        client=client,
        channel=channel,
        thread_ts=thread_ts,
    )

    thread_context = build_conversation_context(messages)

    print("\n" + "=" * 50)
    print("THREAD CONTEXT")
    print("=" * 50)

    print(thread_context)

    print("=" * 50 + "\n")

    say(
        text="I successfully retrieved the thread. Check the terminal.",
        thread_ts=thread_ts,
    )


if __name__ == "__main__":
    handler = SocketModeHandler(
        app,
        os.environ["SLACK_APP_TOKEN"],
    )

    handler.start()
