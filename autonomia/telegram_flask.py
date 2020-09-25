import logging

import telegram
from telegram.ext import Dispatcher

from autonomia.core import autodiscovery, get_handlers

logger = logging.getLogger(__name__)


class TelegramFlask:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.create_bot(app)
        app.extensions["telegram"] = self

    def create_bot(self, app):
        token = app.config.get("API_TOKEN")
        autodiscovery(app.config.get("APPS", []))
        self.bot = telegram.Bot(token=token)
        self.dispatcher = Dispatcher(self.bot, None, workers=0, use_context=True)
        for handler in get_handlers():
            self.dispatcher.add_handler(handler)
        # log all errors
        self.dispatcher.add_error_handler(self.error)

    def setup_webhook(self, app):
        domain = app.config.get("WEBHOOK_DOMAIN")
        path = app.config.get("WEBHOOK_PATH")
        webhook_url = f"https://{domain}/{path}"
        try:
            response = self.bot.get_webhook_info()
        except Exception:
            return False, "Unable to get telegram webhook"

        if response.url == webhook_url:
            return False, f"Keeping the same webhook url: {webhook_url}"

        try:
            success = self.bot.set_webhook(webhook_url)
        except Exception:
            return False, "Unable to set telegram webhook"

        if not success:
            return False, f"Unable to set telegram webhook, return: {success}"

        return True, f"Change webhook to the new url: {webhook_url}"

    @staticmethod
    def error(bot, update, error):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, error)


# This instance should be used to access bot features directly.
# The attributes telegram_flask.bot and telegram_flask.dispatcher are available
telegram_flask = TelegramFlask()
