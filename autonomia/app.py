import logging

from flask import Flask, request
from telegram import Update

from autonomia import settings
from autonomia.telegram_flask import TelegramFlask

app = Flask(__name__)
app.config.from_pyfile("settings.py")
telegram_flask = TelegramFlask()
bot = telegram_flask.init_app(app)

logger = logging.getLogger(__name__)


@app.route(f"/{settings.WEBHOOK_PATH}", methods=["POST"])
def webhook_handler():
    try:
        update = Update.de_json(request.get_json(force=True), bot.instance)
        bot.dispatcher.process_update(update)
    except Exception as e:
        logger.error(e, "Error in telegram webhook endpoint", exc_info=1)
        return "fail"

    return "ok"


@app.route(f"/{settings.WEBHOOK_SET_PATH}", methods=["GET", "POST"])
def set_webhook():
    webhook_url = f"https://{settings.WEBHOOK_DOMAIN}/{settings.WEBHOOK_PATH}"
    success = bot.instance.set_webhook(webhook_url)
    if success:
        return "webhook setup ok"

    return "webhook setup failed"
