import logging
import sys

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
        token = app.config.get("API_TOKEN", "")
        autodiscovery(app.config.get("APPS", []))
        self.instance = telegram.Bot(token=token)
        self.dispatcher = Dispatcher(self.instance, None, workers=0)
        for handler in get_handlers():
            self.dispatcher.add_handler(handler)
        # log all errors
        self.dispatcher.add_error_handler(self.error)
        self.setup_webook(app)

    def setup_webook(self, app):
        # setup webhook callback
        domain = app.config.get("WEBHOOK_DOMAIN")
        path = app.config.get("WEBHOOK_PATH")
        webhook_url = f"https://{domain}/{path}"
        try:
            success = self.instance.set_webhook(webhook_url)
        except Exception:
            logger.error("Unable to set telegram webhook", exc_info=1)
            sys.exit(1)
        if not success:
            logger.fatal(f"Unable to set telegram webhook, return: {success}")
            sys.exit(1)

    @staticmethod
    def error(bot, update, error):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, error)
