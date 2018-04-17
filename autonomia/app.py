import logging

import click
from flask import request
from telegram import Update

from autonomia import settings
from autonomia.app_factory import create_app
from autonomia.telegram_flask import TelegramFlask

app = create_app()
bot = TelegramFlask(app)
logger = logging.getLogger(__name__)


@app.route(f"/{settings.WEBHOOK_PATH}", methods=["POST"])
def webhook_handler():
    try:
        update = Update.de_json(request.get_json(force=True), bot.instance)
        bot.dispatcher.process_update(update)
    except Exception:
        logger.error("Error in telegram webhook endpoint", exc_info=1)
        return "fail"

    return "ok"


@app.cli.command()
def update_webhook():
    updated, msg = bot.setup_webhook(app)
    if updated:
        click.secho(msg, fg="green")
    else:
        click.secho(msg, fg="yellow")
