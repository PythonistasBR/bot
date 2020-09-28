import json
import logging
from urllib import parse, request

from telegram.ext import CallbackContext, CommandHandler
from telegram.update import Update

from autonomia.core import bot_handler

logger = logging.getLogger(__name__)


DUBLIN_BUS_URL = "https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?"


def _get_timetable(bus_stop):
    url = DUBLIN_BUS_URL + parse.urlencode({"stopid": bus_stop, "format": "json"})
    result = json.loads(request.urlopen(url).read().decode("utf8"))
    return result["results"]


def _format_timetable(bus_stop, data):
    if not data:
        return f"Não há informação para: {bus_stop}"

    msg = f"Bus stop {bus_stop}:\n"
    for time in data[:5]:
        msg += f"    {time['route']} - duetime: {time['duetime']}\n"
    return msg


def cmd_dublin_bus(update: Update, context: CallbackContext):
    try:
        bus_stop = " ".join(context.args)
        if not bus_stop:
            update.message.reply_text("Use: /bus <bus stop number>")
            return

        bus_timetable = _get_timetable(bus_stop)
        msg = _format_timetable(bus_stop, bus_timetable)
        update.message.reply_text(msg)
    except Exception:
        logger.error("To sem saco!", exc_info=1)
        update.message.reply_text("To sem saco!")


@bot_handler
def dublin_bus_factory():
    """
    /bus <bus_stop> - list the bus from the station
    """
    return CommandHandler("bus", cmd_dublin_bus, pass_args=True)
