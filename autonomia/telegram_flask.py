import logging
from collections import defaultdict

import telegram
from telegram.ext import ConversationHandler, Dispatcher

from autonomia.core import autodiscovery, get_handlers, setup_handlers

logger = logging.getLogger(__name__)


class TelegramFlask:
    def __init__(self, app=None, persistence=None):
        self.app = app
        self.persistence = persistence
        self.bot = None
        self.dispatcher = None
        if app is not None:
            self.init_app(app, persistence)

    def init_app(self, app, persistence=None):
        self.create_bot(app, persistence)
        app.extensions["telegram"] = self

    def create_bot(self, app, persistence):
        self.app = app
        self.persistence = persistence

        token = app.config.get("API_TOKEN")
        autodiscovery(app.config.get("APPS", []))
        self.bot = telegram.Bot(token=token)
        self.dispatcher = Dispatcher(
            self.bot, None, workers=0, use_context=True, persistence=self.persistence
        )
        setup_handlers(self.dispatcher)
        # log all errors
        self.dispatcher.add_error_handler(self.error)

    def reload_state(self):
        if self.persistence.store_user_data:
            self.dispatcher.user_data = self.persistence.get_user_data()
            if not isinstance(self.dispatcher.user_data, defaultdict):
                raise ValueError("user_data must be of type defaultdict")
        if self.persistence.store_chat_data:
            self.dispatcher.chat_data = self.persistence.get_chat_data()
            if not isinstance(self.dispatcher.chat_data, defaultdict):
                raise ValueError("chat_data must be of type defaultdict")
        if self.persistence.store_bot_data:
            self.dispatcher.bot_data = self.persistence.get_bot_data()
            if not isinstance(self.dispatcher.bot_data, dict):
                raise ValueError("bot_data must be of type dict")
        for handler in get_handlers():
            if isinstance(handler, ConversationHandler) and handler.persistent:
                a = self.persistence.get_conversations(handler.name)
                if not self.persistence:
                    raise ValueError(
                        "Conversationhandler {} can not be persistent if dispatcher "
                        "has no persistence".format(handler.name)
                    )
                handler.persistence = self.persistence
                handler.conversations = self.persistence.get_conversations(handler.name)

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
    def error(update, context):
        raise context.error


# This instance should be used to access bot features directly.
# The attributes telegram_flask.bot and telegram_flask.dispatcher are available
telegram_flask = TelegramFlask()
