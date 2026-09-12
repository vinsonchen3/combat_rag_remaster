import os

from slack_bolt.adapter.socket_mode import SocketModeHandler

from src.slack.app import create_app


def main() -> None:
    app = create_app()

    handler = SocketModeHandler(
        app,
        os.environ["SLACK_APP_TOKEN"],
    )

    handler.start()


if __name__ == "__main__":
    main()