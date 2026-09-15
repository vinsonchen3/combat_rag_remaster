import re

from slack_bolt import App

from src.rag import answer_question
from src.slack.context import (
    format_thread_messages,
    get_thread_messages,
)


def remove_bot_mention(text: str) -> str:
    """
    Remove Slack's <@USER_ID> mention syntax from a message.
    """

    return re.sub(r"<@[A-Z0-9]+>", "", text).strip()


def create_app_mention_handler(retriever):
    """
    Create a Slack app_mention handler with access to the retriever for dependency injection.
    """

    def handle_app_mention(body, client, logger):
        """Handle an app_mention event from Slack."""

        event = body["event"]

        # Ignore bot-generated events.
        if event.get("bot_id"):
            return

        channel_id = event["channel"]
        message_ts = event["ts"]
        thread_ts = event.get("thread_ts", message_ts)

        question = remove_bot_mention(event.get("text", ""))

        if not question:
            client.chat_postMessage(
                channel=channel_id,
                thread_ts=thread_ts,
                text="Ask me a question about the combat robotics documentation.",
            )
            return

        try:
            messages = get_thread_messages(
                client=client,
                channel=channel_id,
                thread_ts=thread_ts,
            )

            # Don't send the current question twice as conversational context.
            previous_messages = [
                message for message in messages if message["ts"] != message_ts
            ]

            conversation_context = format_thread_messages(previous_messages)

            answer = answer_question(
                question=question,
                retriever=retriever,
                conversation_context=conversation_context or None,
            )

            client.chat_postMessage(
                channel=channel_id,
                thread_ts=thread_ts,
                text=answer,
            )

        except Exception:
            logger.exception("Failed to process Slack mention")

            client.chat_postMessage(
                channel=channel_id,
                thread_ts=thread_ts,
                text=("Sorry, I ran into an error while processing that question."),
            )

    return handle_app_mention
