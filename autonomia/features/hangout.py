import json
import logging
import os
import random
import string
from contextlib import contextmanager
from datetime import datetime

from googleapiclient import sample_tools
from telegram import ParseMode
from telegram.ext import CommandHandler

from autonomia.core import bot_handler
from autonomia.settings import GOOGLE_API_CONFIG, PROJECT_PATH

logger = logging.getLogger(__name__)


def random_id():
    return "".join(random.choice(string.ascii_lowercase) for _ in range(10))


@contextmanager
def generate_client_secrets():
    secrets_path = os.path.join(PROJECT_PATH, "features", "client_secrets.json")

    data = {
        "web": {
            "client_id": GOOGLE_API_CONFIG["client_id"],
            "project_id": GOOGLE_API_CONFIG["client_id"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://accounts.google.com/o/oauth2/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": GOOGLE_API_CONFIG["client_secret"],
            "redirect_uris": [
                "https://localhost:8080",
                "https://autonomiabot.herokuapp.com/googleauth/",
            ],
        }
    }
    with open(secrets_path, "w") as f:
        f.write(json.dumps(data))
    yield
    os.remove(secrets_path)


def get_hangout_link(name):
    # Authenticate and construct service.
    service, flags = sample_tools.init(
        [],
        "calendar",
        "v3",
        __doc__,
        __file__,
        scope="https://www.googleapis.com/auth/calendar",
    )
    event = {
        "summary": f"Hangout from telegram - by {name}",
        "start": {"dateTime": datetime.now().isoformat(), "timeZone": "Europe/Dublin"},
        "end": {"dateTime": datetime.now().isoformat(), "timeZone": "Europe/Dublin"},
        "conferenceData": {
            "createRequest": {
                "requestId": random_id(),
                "conferenceSolutionKey": {"type": "eventHangout"},
            }
        },
    }

    event = service.events().insert(
        calendarId="primary", conferenceDataVersion="1", body=event
    ).execute()
    return event.get("hangoutLink")


def cmd_hangout(bot, update):
    try:
        name = update.message.from_user.first_name
        with generate_client_secrets():
            hangout_link = get_hangout_link(name)
            msg = "Deu ruim!"
            if hangout_link:
                msg = f"Novo hangout criado: [hangout room]({hangout_link})"
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
    except Exception:
        logger.error("To sem saco!", exc_info=1)
        update.message.reply_text("To sem saco!")


@bot_handler
def hangout_factory():
    """
    /hangout - create a hangout room and return the link
    """
    return CommandHandler("hangout", cmd_hangout)
