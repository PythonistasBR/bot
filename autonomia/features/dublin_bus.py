import json
import logging
from urllib import parse, request

from telegram.ext import CommandHandler

from autonomia.core import bot_handler

logger = logging.getLogger(__name__)


DUBLIN_BUS_URL = "https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?"


def _get_timetable(bus_stop):
    url = DUBLIN_BUS_URL + parse.urlencode({"stopid": bus_stop, "format": "json"})
    print("*" * 100)
    print(url)
    print("*" * 100)
    result = json.loads(request.urlopen(url).read().decode("utf8"))
    return result["results"]


def _format_timetable(bus_stop, data):
    msg = f"Bus stop {bus_stop}:\n"
    for time in data[:5]:
        msg += f"    {time['route']} - duetime: {time['duetime']}\n"
    return msg


def cmd_dublin_bus(bot, update, args):
    try:
        bus_stop = " ".join(args)
        if not bus_stop:
            update.message.reply_text("Use: /bus <bus stop number>")
            return

        bus_timetable = _get_timetable(bus_stop)
        msg = _format_timetable(bus_stop, bus_timetable)
        update.message.reply_text(msg)
    except Exception as e:
        logger.error(e, "To sem saco!", exc_info=1)
        update.message.reply_text("To sem saco!")


@bot_handler
def dublin_bus_factory():
    """
    /bus <bus_stop> - list the bus from the station
    """
    return CommandHandler("bus", cmd_dublin_bus, pass_args=True)
