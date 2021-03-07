import logging

import click
from flask import request
from telegram import Update

from autonomia import settings
from autonomia.app_factory import create_app
from autonomia.telegram_flask import telegram_flask

app = create_app()
logger = logging.getLogger(__name__)


@app.route(f"/{settings.WEBHOOK_PATH}", methods=["POST"])
def webhook_handler():
    try:
        telegram_flask.reload_state()
        update = Update.de_json(request.get_json(force=True), telegram_flask.bot)
        logger.debug("Received Update with ID %d on Webhook" % update.update_id)
        telegram_flask.dispatcher.process_update(update)
    except Exception:
        logger.error("Error in telegram webhook endpoint", exc_info=1)
        return "fail"

    return "ok"


@app.cli.command("update_webhook")
def update_webhook():
    updated, msg = telegram_flask.setup_webhook(app)
    if updated:
        click.secho(msg, fg="green")
    else:
        click.secho(msg, fg="yellow")
