import logging

import telegram
from telegram.ext import Dispatcher

from autonomia.core import autodiscovery, get_handlers

logger = logging.getLogger(__name__)


class AutonomiaBot:

    def __init__(self, token):
        self.instance = telegram.Bot(token=token)
        self.dispatcher = Dispatcher(self.instance, None, workers=0)
        for handler in get_handlers():
            self.dispatcher.add_handler(handler)
        # log all errors
        self.dispatcher.add_error_handler(self.error)

    def error(self, bot, update, error):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, error)


class TelegramFlask:

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        token = app.config.get("API_TOKEN", "")
        autodiscovery(app.config.get("APPS", []))
        bot = AutonomiaBot(token)
        app.extensions["telegram"] = bot
        return bot
