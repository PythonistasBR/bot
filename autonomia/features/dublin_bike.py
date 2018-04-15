import json
import logging
from urllib import parse, request

from telegram.ext import CommandHandler

from autonomia.core import bot_handler

logger = logging.getLogger(__name__)


DUBLIN_BIKE_URL = "https://api.citybik.es/dublinbikes.json"


def _get_bike_station_info(bike_station):
    result = request.urlopen(DUBLIN_BIKE_URL).read().decode("utf8")
    data = json.loads(result)
    msg = f"Dublin bike station {bike_station}:\n"
    for value in data:
        if str(value["number"]) == str(bike_station):
            msg += "    Bikes {bikes} \n    Free spaces {free}\n    Location {name}".format(
                bikes=value["bikes"], free=value["free"], name=value["name"]
            )
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
    except Exception as e:
        logger.error(e, "Oops de merda!", exc_info=1)
        update.message.reply_text("Oops de merda!")


@bot_handler
def dublin_bike_factory():
    """
    /bike <bike_station> - list the info from the bike station
    """
    return CommandHandler("bike", cmd_dublin_bike, pass_args=True)
