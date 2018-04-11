import json
import logging
from datetime import datetime
from urllib import parse, request

from telegram.ext import CommandHandler

from autonomia.core import bot_handler
from autonomia.settings import MEETUP_API_KEY

logger = logging.getLogger(__name__)
MEETUP_CALENDAR_URL = "https://api.meetup.com/self/calendar"


def _get_calendar_data():
    fields = [
        "name",
        "status",
        "rsvp_limit",
        "yes_rsvp_count",
        "local_date",
        "local_time",
        "venue",
        "link",
    ]

    query_string = parse.urlencode(
        {"only": ",".join(fields), "sign": "true", "key": MEETUP_API_KEY}
    )
    url = f"{MEETUP_CALENDAR_URL}?{query_string}"
    response = request.urlopen(url)
    signed_url = response.getheader("X-Meetup-Signed-URL")
    response = request.urlopen(signed_url)
    return json.loads(response.read())


def _format_events(data):
    out = ["Next meetups available:"]
    today = datetime.now().today()
    for e in data:
        date = datetime.strptime(e["local_date"], "%Y-%m-%d")
        days = (date - today).days
        if days > 30:
            break

        if e["status"] != "upcoming" or "venue" not in e:
            continue

        out.append("-" * 25)
        out.append(
            f"{e['name']} - [{e['yes_rsvp_count']}/{e.get('rsvp_limit', 'Unlimited')}]"
        )
        out.append(f"Date: {date.strftime('%d-%m-%Y')} {e['local_time']}")
        out.append(f"Venue: {e['venue']['name']} - {e['venue']['address_1']}")
        out.append(f"{e['link']}")
    return "\n".join(out)


def cmd_meetup(bot, update):
    try:
        data = _get_calendar_data()
        text = _format_events(data)
        user = update.message.from_user
        bot.send_message(user.id, text, disable_web_page_preview=True)
    except Exception as e:
        logger.error(e, "To sem saco!", exc_info=1)
        update.message.reply_text("To sem saco!")


@bot_handler
def meetup_factory():
    """
    /meetup - list meetup events for next 30 days
    """
    return CommandHandler("meetup", cmd_meetup)
