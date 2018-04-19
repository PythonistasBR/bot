
import logging

from flask import Blueprint, abort
from flask import current_app as app
from flask import request

from autonomia.telegram_flask import telegram_flask

logger = logging.getLogger(__name__)
github = Blueprint("github", __name__, url_prefix="/github")


class PullRequestWebhook:

    def __init__(self, data):
        self.data = data

    def get_message(self):
        return self.dispatcher()

    def dispatcher(self):
        message = ""
        if self.data["action"] == "opened":
            message = self.get_opened_message()
        return message

    def get_opened_message(self):
        url = self.data["pull_request"]["html_url"]
        user = self.data["pull_request"]["user"]["login"]
        message = f"New Pull Request from {user}\n"
        message += f"Please review it: {url}"
        return message


@github.route("/webhook", methods=["POST"])
def github_webhook():
    data = request.get_json(force=True)
    pull_request = PullRequestWebhook(data)
    try:
        message = pull_request.get_message()
        chat_id = app.config["CHAT_ID"]
        if message and chat_id:
            telegram_flask.bot.send_message(chat_id, message)
    except Exception as e:
        logger.error("Something went wrong", exc_info=1)
        abort(500)
    return "ok"
