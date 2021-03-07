import logging

import click
from flask import request

from autonomia import settings
from autonomia.app_factory import create_app
from autonomia.telegram_flask import telegram_flask

app = create_app()
logger = logging.getLogger(__name__)


@app.route(f"/{settings.WEBHOOK_PATH}", methods=["POST"])
def webhook_handler():
    try:
        telegram_flask.process_update(request)
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
