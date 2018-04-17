import json
import logging
from urllib import request

from telegram.ext import CommandHandler

from autonomia.core import bot_handler

logger = logging.getLogger(__name__)


DUBLIN_BIKE_URL = "https://api.citybik.es/dublinbikes.json"


def _get_bike_station_info(bike_station):
    result = request.urlopen(DUBLIN_BIKE_URL).read().decode("utf8")
    list_station_info = json.loads(result)
    msg = f"Dublin bike station {bike_station}:\n"
    for station_info in list_station_info:
        if str(station_info["number"]) == str(bike_station):
            msg += f"    Bikes {station_info['bikes']}\n"
            msg += f"    Free spaces {station_info['free']}\n"
            msg += f"    Location {station_info['name']}\n"
            return msg

    return "deu merda!"


def cmd_dublin_bike(bot, update, args):
    try:
        bike_station = " ".join(args)
        if not bike_station:
            update.message.reply_text("Use: /bike <bike station number>")
            return

        bike_station_info = _get_bike_station_info(bike_station)
        update.message.reply_text(bike_station_info)
    except Exception:
        logger.error("Oops deu merda!", exc_info=1)
        update.message.reply_text("Oops deu merda!")


@bot_handler
def dublin_bike_factory():
    """
    /bike <bike_station> - list the info from the bike station
    """
    return CommandHandler("bike", cmd_dublin_bike, pass_args=True)
