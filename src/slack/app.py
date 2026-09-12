import os

from dotenv import load_dotenv
from slack_bolt import App

from src.ingestion.embedder import model
from src.retrieval.retriever import Retriever
from src.retrieval.vector_store import collection
from src.slack.handlers import create_app_mention_handler

load_dotenv()


def create_app() -> App:
    slack_app = App(
        token=os.environ["SLACK_BOT_TOKEN"],
        app_token=os.environ["SLACK_APP_TOKEN"],
    )

    retriever = Retriever(
        collection=collection,
        model=model,
        top_k=4,
    )

    handle_app_mention = create_app_mention_handler(retriever=retriever)
    slack_app.event("app_mention")(handle_app_mention)

    return slack_app
